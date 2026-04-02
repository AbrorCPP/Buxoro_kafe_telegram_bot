from aiogram.utils.keyboard import InlineKeyboardBuilder

def back_to_categories_kb():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="⬅️ Orqaga (Kategoriyalarga)", 
        callback_data="back_to_product_cats"
    )
    return builder.as_markup()