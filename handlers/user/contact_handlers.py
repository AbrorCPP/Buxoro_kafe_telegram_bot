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
        "   Toshkent shahri, Amir Temur shoh ko'chasi\n\n"
        "📱 <b>Telefon:</b>\n"
        "   <a href='tel:+998901234567'>+998 90 123 45 67</a>\n\n"
        "🕐 <b>Ish vaqti:</b>\n"
        "   Har kuni: 08:00 — 23:00\n\n"
        "━━━━━━━━━━━━━━━━━\n"
        "💬 Savollaringiz bo'lsa bemalol yozing!"
    )
    from keyboards.reply.main_menu import main_menu_inline
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    kb = main_menu_inline()
    # Add a specific location button to this message as well
    location_btn = InlineKeyboardButton(text="📍 Joylashuvni ko'rish", callback_data="restaurant_location")
    kb.inline_keyboard.insert(0, [location_btn])
    
    await call.message.delete()
    await call.message.answer(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data == "restaurant_location")
async def show_restaurant_location(call: CallbackQuery):
    from keyboards.reply.main_menu import main_menu_inline
    
    # Coordinates for 87XQ+J64, Amir Temur Avenue, Tashkent
    LAT, LON = 41.314681, 69.243562
    
    await call.message.delete()
    await call.message.answer_location(latitude=LAT, longitude=LON)
    await call.message.answer(
        "📍 <b>Bizning manzil:</b>\n"
        "Toshkent shahri, Amir Temur shoh ko'chasi\n"
        "<i>(Mo'ljal: Oloy bozori yaqinida)</i>",
        reply_markup=main_menu_inline(),
        parse_mode="HTML"
    )
