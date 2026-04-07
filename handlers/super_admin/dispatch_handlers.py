from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loader import db, bot
from router import router
from config import S_ADMIN


async def is_admin_or_superadmin(call: CallbackQuery) -> bool:
    user_id = str(call.from_user.id)
    if user_id == str(S_ADMIN):
        return True
    admin = db.detect_admin(user_id)
    return bool(admin)


@router.callback_query(F.data.startswith("assign_"), is_admin_or_superadmin)
async def assign_order_admin(call: CallbackQuery):
    data = call.data.split("_")
    order_id = data[1]
    courier_id = data[2]

    order = db.get_order(order_id)
    if order and order['courier_id']:
        return await call.answer("❌ Bu buyurtma allaqachon biriktirilgan!", show_alert=True)

    success = db.assign_courier(order_id, courier_id)
    if not success:
        return await call.answer("⚠️ Qandaydir xato yuz berdi.", show_alert=True)

    assigner_name = call.from_user.full_name or call.from_user.username or str(call.from_user.id)
    await call.message.edit_text(
        call.message.text + f"\n\n✅ <b>{assigner_name}</b> tomonidan tayinlandi",
        parse_mode="HTML"
    )

    user_id = order['user_id']
    user = db.detect_user(user_id)
    items_txt = db.get_order_items_text(order_id)

    courier_text = (
        f"🎯 <b>Siz buyurtmaga tayinlandingiz!</b>\n"
        f"━━━━━━━━━━━━━━━━━\n\n"
        f"🧾 <b>Buyurtma:</b> #{order_id}\n\n"
        f"👤 <b>Xaridor:</b> {user.get('username')}\n"
        f"📞 <b>Telefon:</b> {user.get('phone_number')}\n"
        f"📍 <b>Manzil:</b> {user.get('coordinates')}\n\n"
        f"🛒 <b>Buyurtma tarkibi:</b>\n{items_txt}\n"
        f"━━━━━━━━━━━━━━━━━\n"
        f"💰 Ovqat narxi: <b>{order['total_price']:,} so'm</b>\n".replace(",", " ") +
        f"🚚 Yetkazish narxi: <b>{order['delivery_price']:,} so'm</b>\n\n".replace(",", " ") +
        f"<i>Holatni yangilash uchun tugmalardan foydalaning 👇</i>"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧑‍🍳 Tayyorlanmoqda", callback_data=f"status_prep_{order_id}")],
        [InlineKeyboardButton(text="🍱 Tayyor",          callback_data=f"status_ready_{order_id}")],
        [InlineKeyboardButton(text="🚙 Yo'lda",          callback_data=f"status_road_{order_id}")],
        [InlineKeyboardButton(text="✅ Yetkazildi",       callback_data=f"status_done_{order_id}")],
    ])

    try:
        await bot.send_message(courier_id, courier_text, reply_markup=kb, parse_mode="HTML")
    except:
        pass

    courier = db.detect_courier(courier_id)
    distance = float(order.get('distance_km') or 0)
    eta = int(distance * 3) + 15

    try:
        await bot.send_message(
            user_id,
            f"🚀 <b>Kuryer tayinlandi!</b>\n"
            f"━━━━━━━━━━━━━━━━━\n\n"
            f"👤 <b>Kuryer:</b> {courier['username']}\n"
            f"📞 <b>Telefon:</b> {courier['phone']}\n\n"
            f"⏳ <b>Taxminiy yetib borish:</b> ~{eta} daqiqa\n\n"
            f"<i>Buyurtmangiz yo'lda! 🚙</i>",
            parse_mode="HTML"
        )
    except:
        pass
