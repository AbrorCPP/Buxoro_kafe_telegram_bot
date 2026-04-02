from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def delete_product_keyboard(products):
    builder = InlineKeyboardBuilder()
    
    for product in products:
        builder.button(
            text=f"❌ {product.get('name')}", 
            callback_data=f"del_prod_{product.get('id')}"
        )
    
    builder.adjust(1)
    
    # MANA SHU QATORNI QO'SHING:
    builder.row(InlineKeyboardButton(
        text="⬅️ Kategoriyalarga qaytish", 
        callback_data="back_to_product_cats")
    )
    
    return builder.as_markup()