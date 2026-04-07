from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from router import router
from loader import db

@router.callback_query(F.data == "show_cart")
async def show_cart_items(call: CallbackQuery):
    telegram_id = str(call.from_user.id)
    cart_items = db.get_cart(telegram_id)
    if not cart_items:
        await call.answer("Savatingiz bo'sh 🛒", show_alert=True)
        return

    text = (
        "🛒 <b>Savatchangiz</b>\n"
        "━━━━━━━━━━━━━━━━━\n\n"
    )
    total_price = 0
    builder = InlineKeyboardBuilder()

    for item in cart_items:
        price = item['price'] * item['quantity']
        total_price += price
        text += f"▫️ <b>{item['name']}</b> × {item['quantity']} = <b>{price:,} so'm</b>\n".replace(",", " ")

    text += f"\n━━━━━━━━━━━━━━━━━\n💰 <b>Jami: {total_price:,} so'm</b>".replace(",", " ")

    builder.button(text="✅ Buyurtma berish", callback_data="checkout")
    builder.button(text="🗑 Tozalash", callback_data="clear_cart")
    builder.button(text="🔙 Orqaga", callback_data="back_main")
    builder.adjust(1)

    await call.message.delete()
    await call.message.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")

@router.callback_query(F.data == "clear_cart")
async def process_clear_cart(call: CallbackQuery):
    telegram_id = str(call.from_user.id)
    db.clear_cart(telegram_id)
    from keyboards.reply.main_menu import main_menu_inline
    await call.message.delete()
    await call.message.answer(
        "🗑 <b>Savat tozalandi!</b>\n\n"
        "<i>Yangi buyurtma bermoqchimisiz? Menyuga kiring 👇</i>",
        reply_markup=main_menu_inline(),
        parse_mode="HTML"
    )

from aiogram.fsm.context import FSMContext
from states.checkout_state import CheckoutState
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, LabeledPrice, PreCheckoutQuery, ReplyKeyboardRemove
from config import PAYMENT_TOKEN

@router.callback_query(F.data == "checkout")
async def process_checkout(call: CallbackQuery, state: FSMContext):
    telegram_id = str(call.from_user.id)
    cart_items = db.get_cart(telegram_id)
    if not cart_items:
        await call.answer("Savatingiz bo'sh 🛒", show_alert=True)
        return

    await state.set_state(CheckoutState.location)
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📍 Joylashuvni yuborish", request_location=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await call.message.delete()
    await call.message.answer(
        "📍 <b>Yetkazib berish manzili</b>\n"
        "━━━━━━━━━━━━━━━━━\n\n"
        "Pastdagi tugma orqali joylashuvingizni yuboring.\n"
        "<i>Bu yetkazib berish narxini hisoblash uchun kerak.</i>",
        reply_markup=kb,
        parse_mode="HTML"
    )

@router.message(CheckoutState.location)
async def process_checkout_location(message: Message, state: FSMContext):
    from utils.math_utils import haversine
    # New Location: 87XQ+J64, Amir Temur Avenue, Tashkent
    KAFE_LAT, KAFE_LON = 41.314681, 69.243562

    if message.location:
        loc = f"{message.location.latitude},{message.location.longitude}"
        user_lat = message.location.latitude
        user_lon = message.location.longitude
    else:
        loc = message.text
        user_lat, user_lon = KAFE_LAT, KAFE_LON

    await state.update_data(location=loc)

    telegram_id = str(message.from_user.id)
    cart_items = db.get_cart(telegram_id)
    if not cart_items:
        await message.answer("Savatingiz bo'sh.")
        await state.clear()
        return

    db.execute("UPDATE users SET coordinates=%s WHERE telegram_id=%s", (loc, telegram_id), commit=True)

    distance = haversine(KAFE_LAT, KAFE_LON, user_lat, user_lon)
    delivery_price = 5000 + int(distance * 2000)

    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    items = [{'product_id': i['product_id'], 'quantity': i['quantity'], 'price': i['price']} for i in cart_items]
    order_id = db.create_order(telegram_id, items, total_price, delivery_price, distance)

    db.clear_cart(telegram_id)
    await state.clear()

    prices = [
        LabeledPrice(label=f"Buyurtma #{order_id}", amount=int(total_price * 100)),
        LabeledPrice(label=f"Yetkazib berish ({distance:.1f} km)", amount=int(delivery_price * 100))
    ]

    try:
        from loader import bot
        await message.answer(
            f"📍 <b>Joylashuv qabul qilindi!</b>\n\n"
            f"📏 Masofa: <b>{distance:.1f} km</b>\n"
            f"🚚 Yetkazish narxi: <b>{delivery_price:,} so'm</b>\n\n".replace(",", " ") +
            f"<i>To'lovni amalga oshiring 👇</i>",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="HTML"
        )
        await bot.send_invoice(
            chat_id=message.chat.id,
            title=f"🍽 Buxoro Kafe — Buyurtma #{order_id}",
            description=f"Ovqat: {total_price:,} so'm | Yetkazish ({distance:.1f} km): {delivery_price:,} so'm".replace(",", " "),
            payload=f"order_{order_id}",
            provider_token=PAYMENT_TOKEN,
            currency="UZS",
            prices=prices,
            start_parameter="buxoro_kafe_order"
        )
    except Exception as e:
        print(f"Invoice error: {e}")
        from keyboards.reply.main_menu import main_menu_inline
        from loader import bot
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        await message.answer(
            f"✅ <b>Buyurtmangiz qabul qilindi!</b>\n\n"
            f"🧾 Buyurtma raqami: <b>#{order_id}</b>\n"
            f"📏 Masofa: {distance:.1f} km\n"
            f"💰 Ovqat: {total_price:,} so'm\n".replace(",", " ") +
            f"🚚 Yetkazish: {delivery_price:,} so'm\n".replace(",", " ") +
            f"\n<i>Kuryer tez orada siz bilan bog'lanadi!</i>",
            reply_markup=main_menu_inline(),
            parse_mode="HTML"
        )
        couriers = db.get_all_couriers()
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🙋 Men yetkazaman!", callback_data=f"volunteer_{order_id}")]
        ])
        for c in couriers:
            try:
                await bot.send_message(
                    c['telegram_id'],
                    f"🔔 <b>Yangi buyurtma!</b>\n\n"
                    f"🧾 Buyurtma: <b>#{order_id}</b>\n"
                    f"📏 Masofa: {distance:.1f} km\n"
                    f"🚚 Yetkazish haqqi: {delivery_price:,} so'm\n\n".replace(",", " ") +
                    f"<i>Qabul qilasizmi?</i>",
                    reply_markup=kb,
                    parse_mode="HTML"
                )
            except Exception as ce:
                pass

@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    from loader import bot
    from keyboards.reply.main_menu import main_menu_inline
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    payload = message.successful_payment.invoice_payload
    if payload and payload.startswith("order_"):
        order_id = payload.split("_")[1]

        couriers = db.get_all_couriers()
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🙋 Men yetkazaman!", callback_data=f"volunteer_{order_id}")]
        ])
        for c in couriers:
            try:
                await bot.send_message(
                    c['telegram_id'],
                    f"💳 <b>TO'LOV QILINGAN — Yangi Buyurtma!</b>\n\n"
                    f"🧾 Buyurtma: <b>#{order_id}</b>\n\n"
                    f"<i>Yetkazib berasizmi?</i>",
                    reply_markup=kb,
                    parse_mode="HTML"
                )
            except:
                pass

    await message.answer(
        "🎉 <b>To'lov muvaffaqiyatli qabul qilindi!</b>\n\n"
        "🧑‍🍳 Oshpazlar buyurtmangizni tayyorlashni boshladi.\n"
        "📱 Kuryer tayinlanganda sizga xabar yuboriladi.\n\n"
        "<i>Yoqimli ishtaha! 🍽</i>",
        reply_markup=main_menu_inline(),
        parse_mode="HTML"
    )
