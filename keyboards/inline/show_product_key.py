from aiogram.utils.keyboard import InlineKeyboardBuilder

def admin_category_list_kb(categories):
    builder = InlineKeyboardBuilder()
    for cat in categories:
        builder.button(text=f"📂 {cat['name']}", callback_data=f"admin_cat_{cat['id']}")
    
    builder.adjust(2)
    return builder.as_markup()


def back_to_categories_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Orqaga (Kategoriyalarga)", callback_data="back_to_admin_cats")
    return builder.as_markup()