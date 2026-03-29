from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def delete_admin_keyboard(admins: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for ad in admins:
        builder.button(text=ad["username"], callback_data=f"delete_ad_{ad['id']}")
    builder.adjust(2)
    return builder.as_markup()
