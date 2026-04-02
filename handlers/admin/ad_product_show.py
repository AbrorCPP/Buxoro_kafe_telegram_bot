from aiogram import Router, F, types
from keyboards.inline.show_product_key import admin_category_list_kb,back_to_categories_kb 
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loader import db
from router import router

@router.message(F.text == "/show_products")
async def admin_show_categories(message: types.Message):
    categories = db.get_all_categories() # Barcha kategoriyalarni olamiz
    kb = admin_category_list_kb(categories)
    await message.answer("Mahsulotlarini ko'rmoqchi bo'lgan kategoriyani tanlang:", reply_markup=kb)


@router.callback_query(F.data.startswith("admin_cat_"))
async def admin_show_products(callback: types.CallbackQuery):
    cat_id = callback.data.split("_")[2]
    products = db.get_products_by_category(cat_id)
    
    if not products:
        await callback.message.edit_text(
        "Bu kategoriyada hali mahsulotlar yo'q.", 
        reply_markup=back_to_categories_kb())
        return


    await callback.message.delete()
    
    for prod in products:
        caption = (f" ID: {prod['id']}\n"
                f" Nomi: {prod['name']}\n"
                f" Narxi: {prod['price']} so'm\n"
                f" Tavsif: {prod['description']}")
    
        image_link = prod.get('image_id') 

        if image_link and image_link.strip() and image_link != "None":
            try:
                await callback.message.answer_photo(
                    photo=image_link,
                    caption=caption
                )
            except Exception as e:
                print(f"Rasm yuborishda xatolik (ID: {prod['id']}): {e}")
                await callback.message.answer(f"⚠️ Rasm yuklanmadi!\n\n{caption}")
            else:
                await callback.message.answer(caption)

        await callback.message.answer("Yuqoridagilar tanlangan kategoriya mahsulotlari:", 
                                    reply_markup=back_to_categories_kb())
        await callback.answer()


@router.callback_query(F.data == "back_to_admin_cats")
async def back_to_cats(callback: types.CallbackQuery):
    try:
        categories = db.get_all_categories()
        kb = admin_category_list_kb(categories)

        try:
            await callback.message.delete()
        except:
            pass

        await callback.bot.send_message(
            chat_id=callback.from_user.id,
            text="Kategoriyani tanlang:",
            reply_markup=kb
        )

        await callback.answer()

    except Exception as e:
        print(f"Orqaga qaytishda xatolik: {e}")
        await callback.answer("Xatolik yuz berdi!", show_alert=True)