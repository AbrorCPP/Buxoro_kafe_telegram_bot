from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def admin_product_list_kb(products):
    builder = InlineKeyboardBuilder()
    for product in products:
        # callback_data ga o'chirish uchun maxsus prefiks beramiz, masalan: "del_prod_12"
        builder.button(
            text=f"❌ {product.name}", 
            callback_data=f"del_prod_{product.id}"
        )
    builder.adjust(1) # Tugmalarni ustunma-ustun taxlash
    builder.row(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin_categories"))
    return builder.as_markup()
