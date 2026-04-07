from aiogram import F
from aiogram.types import CallbackQuery
from router import router

@router.callback_query(F.data == "settings")
async def process_settings(call: CallbackQuery):
    text = (
        "⚙️ <b>Sozlamalar</b>\n"
        "━━━━━━━━━━━━━━━━━\n\n"
        "🔧 Ushbu bo'lim tez orada faollashadi.\n\n"
        "📋 <b>Kelgusida qo'shiladi:</b>\n"
        "   • 📱 Telefon raqamini o'zgartirish\n"
        "   • 📍 Manzilni yangilash\n"
        "   • 🔔 Bildirishnomalar sozlamalari\n\n"
        "<i>Yangilanishlarni kuzatib boring!</i>"
    )
    from keyboards.reply.main_menu import main_menu_inline
    await call.message.delete()
    await call.message.answer(text, reply_markup=main_menu_inline(), parse_mode="HTML")
