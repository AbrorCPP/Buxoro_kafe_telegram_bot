from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loader import db
from router import router

@router.callback_query(F.data == "open_menu")
async def show_categories(call: CallbackQuery):
    categories = db.get_all_categories()
    if not categories:
        await call.answer("Kategoriyalar yo'q 🙁", show_alert=True)
        return

    await call.message.delete()

    # Send each category as a card
    for cat in categories:
        text = (
            f"🍽 <b>{cat['name']}</b>\n"
            f"━━━━━━━━━━━━━━━━━\n\n"
            f"{cat.get('description', '')}"
        )

        builder = InlineKeyboardBuilder()
        builder.button(text="📂 Mahsulotlarni ko'rish", callback_data=f"cat_{cat['id']}")
        builder.adjust(1)

        if cat.get('image_id'):
            try:
                await call.message.answer_photo(
                    photo=cat['image_id'],
                    caption=text,
                    reply_markup=builder.as_markup(),
                    parse_mode="HTML"
                )
            except Exception as e:
                print(f"Kategoriya rasm yuborishda xatolik: {e}")
                await call.message.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")
        else:
            await call.message.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")

    # Back button at the end
    back_builder = InlineKeyboardBuilder()
    back_builder.button(text="🔙 Asosiy menyu", callback_data="back_main")
    await call.message.answer(
        "Barcha kategoriyalar ko'rsatildi. Kerakli kategoriyani tanlang 👆",
        reply_markup=back_builder.as_markup(),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("cat_"))
async def show_products(call: CallbackQuery):
    cat_id = call.data.split("_")[1]
    category = db.get_category(cat_id)
    products = db.get_products_by_category(cat_id)
    if not products:
        await call.answer("Bu kategoriyada mahsulotlar yo'q 🙁", show_alert=True)
        return

    await call.message.delete()

    # Send category image if exists
    if category and category.get('image_id'):
        try:
            await call.message.answer_photo(
                photo=category['image_id'],
                caption=f"🍽 <b>{category['name']}</b>\n━━━━━━━━━━━━━━━━━\n\n{category.get('description', '')}",
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"Kategoriya rasm yuborishda xatolik: {e}")

    # Send each product as a card
    for prod in products:
        text = (
            f"🍽 <b>{prod['name']}</b>\n"
            f"━━━━━━━━━━━━━━━━━\n\n"
            f"📝 <b>Tavsif:</b>\n"
            f"<i>{prod['description']}</i>\n\n"
            f"💰 <b>Narxi:</b> {prod['price']:,} so'm".replace(",", " ")
        )

        builder = InlineKeyboardBuilder()
        builder.button(text="🛒 Savatga qo'shish", callback_data=f"addcart_{prod['id']}")
        builder.adjust(1)

        if prod.get('image_id'):
            try:
                await call.message.answer_photo(
                    photo=prod['image_id'],
                    caption=text,
                    reply_markup=builder.as_markup(),
                    parse_mode="HTML"
                )
            except Exception as e:
                print(f"Mahsulot rasm yuborishda xatolik: {e}")
                await call.message.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")
        else:
            await call.message.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")

    # Back button at the end
    back_builder = InlineKeyboardBuilder()
    back_builder.button(text="🔙 Kategoriyalarga", callback_data="open_menu")
    await call.message.answer(
        "Barcha mahsulotlar ko'rsatildi. Kerakli bo'limni tanlang 👆",
        reply_markup=back_builder.as_markup(),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("addcart_"))
async def process_add_cart(call: CallbackQuery):
    prod_id = call.data.split("_")[1]
    telegram_id = str(call.from_user.id)
    db.add_to_cart(telegram_id, prod_id, 1)
    await call.answer("✅ Mahsulot savatga qo'shildi!", show_alert=True)

@router.callback_query(F.data == "back_main")
async def back_to_main(call: CallbackQuery):
    from keyboards.reply.main_menu import main_menu_inline
    await call.message.delete()
    await call.message.answer(
        "🏠 <b>Asosiy menyu</b>\n\n"
        "<i>Kerakli bo'limni tanlang 👇</i>",
        reply_markup=main_menu_inline(),
        parse_mode="HTML"
    )
