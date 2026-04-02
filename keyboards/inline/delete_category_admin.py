from aiogram.utils.keyboard import InlineKeyboardBuilder

def admin_category_list_kb(categories):
    builder = InlineKeyboardBuilder()
    for cat in categories:
        builder.button(text=f"📂 {cat['name']}", callback_data=f"adminforproduct_cat_{cat['id']}")
    
    builder.adjust(2)
    return builder.as_markup()


