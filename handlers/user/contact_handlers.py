from aiogram import F
from aiogram.types import CallbackQuery
from router import router

@router.callback_query(F.data == "contact_us")
async def contact_us(call: CallbackQuery):
    text = (
        "📞 <b>Buxoro Kafe</b> bilan aloqa:\n\n"
        "📍 Manzil: Buxoro shahar, Mustaqillik ko'chasi 1-A uy.\n"
        "📱 Telefon: +998 90 123 45 67\n"
        "🕒 Ish vaqti: 08:00 dan 23:00 gacha\n"
    )
    from keyboards.reply.main_menu import main_menu_inline
    await call.message.delete()
    await call.message.answer(text, reply_markup=main_menu_inline(), parse_mode="HTML")
