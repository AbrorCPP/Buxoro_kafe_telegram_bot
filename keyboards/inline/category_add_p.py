from aiogram.utils.keyboard import InlineKeyboardBuilder

async def category_keyboard(categories: list):
    builder = InlineKeyboardBuilder()
    for cat in categories:
        builder.button(text=cat["name"], callback_data=f"cat_{cat['id']}")
    builder.adjust(2) 
    return builder.as_markup()