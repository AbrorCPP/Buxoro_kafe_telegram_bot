from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loader import db
from router import router

@router.callback_query(F.data == "open_menu")
async def show_categories(call: CallbackQuery):
    categories = db.get_all_categories()
    builder = InlineKeyboardBuilder()
    if categories:
        for cat in categories:
            builder.button(text=cat['name'], callback_data=f"cat_{cat['id']}")
    builder.adjust(2)
    builder.row(InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main"))
    await call.message.delete()
    await call.message.answer(
        "🍽 <b>Menyu</b>\n"
        "━━━━━━━━━━━━━━━━━\n\n"
        "Qaysi kategoriyadan buyurtma berasiz?",
        reply_markup=builder.as_markup(),
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

    builder = InlineKeyboardBuilder()
    for prod in products:
        builder.button(text=prod['name'], callback_data=f"prod_{prod['id']}")
    builder.adjust(2)
    builder.row(InlineKeyboardButton(text="🔙 Kategoriyalarga", callback_data="open_menu"))

    caption = (
        f"🍽 <b>{category['name']}</b>\n"
        f"━━━━━━━━━━━━━━━━━\n\n"
        f"{category.get('description', '')}\n\n"
        f"🛍 <b>Mahsulotlar</b>\n"
        f"Kerakli mahsulotni tanlang 👇"
    )

    if category and category.get('image_id'):
        try:
            await call.message.answer_photo(
                photo=category['image_id'],
                caption=caption,
                reply_markup=builder.as_markup(),
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"Kategoriya rasm yuborishda xatolik: {e}")
            await call.message.answer(caption, reply_markup=builder.as_markup(), parse_mode="HTML")
    else:
        await call.message.answer(caption, reply_markup=builder.as_markup(), parse_mode="HTML")

@router.callback_query(F.data.startswith("prod_"))
async def show_product_detail(call: CallbackQuery):
    try:
        prod_id = call.data.split("_")[1]
        product = db.get_product(prod_id)

        if not product:
            await call.answer("Mahsulot topilmadi 😔", show_alert=True)
            return

        text = (
            f"🍽 <b>{product['name']}</b>\n"
            f"━━━━━━━━━━━━━━━━━\n\n"
            f"📝 <b>Tavsif:</b>\n"
            f"<i>{product['description']}</i>\n\n"
            f"💰 <b>Narxi:</b> {product['price']:,} so'm".replace(",", " ")
        )

        builder = InlineKeyboardBuilder()
        builder.button(text="🛒 Savatga qo'shish", callback_data=f"addcart_{product['id']}")
        builder.button(text="🔙 Orqaga", callback_data=f"cat_{product['category_id']}")
        builder.adjust(1)

        await call.message.delete()
        if product.get('image_id'):
            try:
                await call.message.answer_photo(
                    photo=product['image_id'],
                    caption=text,
                    reply_markup=builder.as_markup(),
                    parse_mode="HTML"
                )
            except Exception as e:
                print(f"Rasm yuborishda xatolik: {e}")
                await call.message.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")
        else:
            await call.message.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    except Exception as e:
        print(f"Mahsulot ko'rsatishda xatolik: {e}")
        await call.answer("Xatolik yuz berdi 😔", show_alert=True)

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
