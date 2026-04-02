from aiogram import Router, F, types
from keyboards.inline.show_product_key import admin_category_list_kb,back_to_categories_kb
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loader import db
from router import router

@router.message(F.text == "/show_products")
async def admin_show_categories(message: types.Message):
    categories = db.get_all_categories() # Barcha kategoriyalarni olamiz
    kb = admin_category_list_kb(categories)
    await message.answer("🚫 Mahsulotlarini o'chirmoqchi bo'lgan kategoriyani tanlang:", reply_markup=kb)

@router.callback_query(F.data.startwith("admin_cat_"))
async def show_category_products(callback:types.CallbackQuery):
    category_id = callback.data.split("_")[-2]
    products = db.get_products_by_category(category_id)
    
    if not products:
        await callback.message.edit_text(
        "Bu kategoriyada hali mahsulotlar yo'q.", 
        reply_markup=back_to_categories_kb())
        return
    
    await callback.message.delete()

    kb = await admin_category_list_kb(products)
    await callback.message.edit_text(
        "O'chirmoqchi bo'lgan mahsulotni tanlang: ",
        reply_markup=kb)

@router.callback_query(F.data.startwith("del_prod_"))
async def delete_product_handler(callback: types.CallbackQuery):
    product_id = int(callback.data.split("_")[2])

    try:
        await db.delete_product(product_id)
        await callback.answer("Mahsulot muvaffaqiyatli o'chirildi!",show_alert=True)
    except Exception as e:
        await callback.answer("Bazada xatolik texnik hodimga yuzlaning",show_alert=True)
    
    categories = await db.get_all_categories()
    kb = await admin_category_list_kb(categories)
    await callback.message.edit_text(
        "🚫 Mahsulotlarini o'chirmoqchi bo'lgan kategoriyani tanlang:",
        reply_markup=kb)

