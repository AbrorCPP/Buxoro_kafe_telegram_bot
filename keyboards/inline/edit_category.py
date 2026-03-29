from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def edit_category_keyboard(category: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for cat in category:
        # 'edit_cat_' emas, 'edit_all_' bo'lishi kerak
        builder.button(text=cat["name"], callback_data=f"edit_all_{cat['id']}")
    builder.adjust(2)
    return builder.as_markup()

