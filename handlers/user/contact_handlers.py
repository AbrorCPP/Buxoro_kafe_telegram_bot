from aiogram import F
from aiogram.types import CallbackQuery
from router import router

@router.callback_query(F.data == "contact_us")
async def contact_us(call: CallbackQuery):
    text = (
        "📞 <b>Biz bilan bog'lanish</b>\n"
        "━━━━━━━━━━━━━━━━━\n\n"
        "🏪 <b>Buxoro Kafe</b>\n\n"
        "📍 <b>Manzil:</b>\n"
        "   Buxoro shahar, Mustaqillik ko'chasi 1-A\n\n"
        "📱 <b>Telefon:</b>\n"
        "   <a href='tel:+998901234567'>+998 90 123 45 67</a>\n\n"
        "🕐 <b>Ish vaqti:</b>\n"
        "   Har kuni: 08:00 — 23:00\n\n"
        "━━━━━━━━━━━━━━━━━\n"
        "💬 Savollaringiz bo'lsa bemalol yozing!"
    )
    from keyboards.reply.main_menu import main_menu_inline
    await call.message.delete()
    await call.message.answer(text, reply_markup=main_menu_inline(), parse_mode="HTML")
