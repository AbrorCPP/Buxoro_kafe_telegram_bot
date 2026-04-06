from aiogram import F
from aiogram.types import CallbackQuery
from router import router

@router.callback_query(F.data == "settings")
async def process_settings(call: CallbackQuery):
    text = (
        "⚙️ Sozlamalar bo'limi tez orada ishga tushadi...\n"
        "Ushbu bo'limda siz telefon raqamingizni va joylashuvingizni o'zgartirishingiz mumkin bo'ladi."
    )
    from keyboards.reply.main_menu import main_menu_inline
    await call.message.delete()
    await call.message.answer(text, reply_markup=main_menu_inline())
