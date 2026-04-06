from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loader import db, bot
from router import router

@router.callback_query(F.data.startswith("volunteer_"))
async def volunteer_order(call: CallbackQuery):
    courier_id = str(call.from_user.id)
    order_id = call.data.split("_")[1]
    
    # check if order is still pending
    order = db.get_order(order_id)
    if order and order['courier_id']:
        return await call.answer("Bu buyurtma allaqachon biriktirilgan!", show_alert=True)
    
    # Check if courier is valid
    courier = db.detect_courier(courier_id)
    if not courier:
        return await call.answer("Siz kuryer emassiz!", show_alert=True)
        
    db.add_order_bid(order_id, courier_id)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(f"Talabingiz adminga yuborildi. Kuting! #{order_id}")
    
    from config import S_ADMIN
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Shuni Tayinlash", callback_data=f"assign_{order_id}_{courier_id}")]
    ])
    try:
        await bot.send_message(
            S_ADMIN,
            f"🔔 NOMZOD KURYER:\nIsmi: {courier['username']}\nTelefon: {courier['phone']}\nBuyurtma Raqami: #{order_id}\n",
            reply_markup=kb
        )
    except:
        pass

@router.callback_query(F.data.startswith("status_"))
async def change_order_status(call: CallbackQuery):
    data = call.data.split("_")
    action = data[1]
    order_id = data[2]
    
    status_map = {
        "prep": ("Tayyorlanmoqda 🧑‍🍳", "Sizning buyurtmangiz tayyorlanmoqda 🧑‍🍳"),
        "ready": ("Tayyor 🍱", "Buyurtmangiz tayyor! 🍱"),
        "road": ("Yo'lda 🚙", "Kuryer buyurtmani sizga yubordi, u yo'lda! 🚙"),
        "done": ("Yetkazib berildi ✅", "Buyurtmangiz muvaffaqiyatli yetkazib berildi! Yoqimli ishtaha! ✅")
    }
    
    new_status, user_msg = status_map.get(action)
    db.update_order_status(order_id, new_status)
    
    order = db.get_order(order_id)
    try:
        await bot.send_message(order['user_id'], user_msg)
    except:
        pass
        
    await call.answer(f"Holat: {new_status} ga o'zgartirildi", show_alert=True)
