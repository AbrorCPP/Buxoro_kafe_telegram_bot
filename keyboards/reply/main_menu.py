from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_inline():
    kb = [
        [
            InlineKeyboardButton(text="🍴 Menyu", callback_data="open_menu"),
            InlineKeyboardButton(text="🛒 Savatcha", callback_data="show_cart")
        ],
        [
            InlineKeyboardButton(text="📦 Buyurtmalarim", callback_data="my_orders"),
            InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="settings")
        ],
        [
            InlineKeyboardButton(text="📞 Biz bilan aloqa", callback_data="contact_us")
        ]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard
