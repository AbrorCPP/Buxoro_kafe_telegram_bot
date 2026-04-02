from aiogram import Router, F, types
from keyboards.inline.delete_category_admin import admin_category_list_kb
from keyboards.inline.delete_product_key import delete_product_keyboard
from loader import db
from router import router
from keyboards.inline.delete_product_back_buttons import back_to_categories_kb

@router.message(F.text == "/delete_products")
async def admin_show_categories(message: types.Message):
    categories = db.get_all_categories() 
    kb = admin_category_list_kb(categories)
    await message.answer("🚫 Mahsulotlarini o'chirmoqchi bo'lgan kategoriyani tanlang:", 
                         reply_markup=kb
    )
@router.callback_query(F.data.startswith("adminforproduct_cat_"))
async def show_category_products(callback: types.CallbackQuery):
    category_id = int(callback.data.split("_")[-1])
    products = db.get_products_by_category(category_id)
    
    if not products:
        # Mahsulot yo'q bo'lsa, edit_text ishlaydi
        await callback.message.edit_text(
            "Bu kategoriyada hali mahsulotlar yo'q.", 
            reply_markup=back_to_categories_kb()
        )
        return
    
    kb = delete_product_keyboard(products)

    await callback.message.edit_text(
        "O'chirmoqchi bo'lgan mahsulotni tanlang:",
        reply_markup=kb
    )
    await callback.answer()


@router.callback_query(F.data.startswith("del_prod_"))
async def delete_product_handler(callback: types.CallbackQuery):
    product_id = int(callback.data.split("_")[2])

    try:
        db.delete_product(product_id)
        await callback.answer("Mahsulot muvaffaqiyatli o'chirildi!",show_alert=True)
    except Exception as e:
        print(f"DB Error: {e}")
        await callback.answer("Bazada xatolik texnik hodimga yuzlaning",show_alert=True)
        return
    
    categories = db.get_all_categories()
    kb = admin_category_list_kb(categories)

    await callback.message.edit_text(
        "🚫 Mahsulotlarini o'chirmoqchi bo'lgan kategoriyani tanlang:",
        reply_markup=kb)

@router.callback_query(F.data == "back_to_product_cats")
async def back_to_categories_handler(callback: types.CallbackQuery):
    categories = db.get_all_categories() 
    kb = admin_category_list_kb(categories)
    
    # Xabarni o'chirib o'tirmasdan, shunchaki tahrirlaymiz
    await callback.message.edit_text(
        "🚫 Mahsulotlarini o'chirmoqchi bo'lgan kategoriyani tanlang:",
        reply_markup=kb
    )
    await callback.answer()