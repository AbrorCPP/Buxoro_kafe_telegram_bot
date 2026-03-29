from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def show_category_keyboard(category: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for cat in category:
        # 'edit_cat_' emas, 'edit_all_' bo'lishi kerak
        builder.button(text=cat["name"], callback_data=f"show_cat_{cat['id']}")
    builder.adjust(2)
    return builder.as_markup()
