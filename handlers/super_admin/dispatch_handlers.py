from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loader import db, bot
from router import router
from config import S_ADMIN

@router.callback_query(F.data.startswith("assign_"), F.from_user.id.in_({int(S_ADMIN)}))
async def assign_order_admin(call: CallbackQuery):
    data = call.data.split("_")
    order_id = data[1]
    courier_id = data[2]
    
    order = db.get_order(order_id)
    if order and order['courier_id']:
        return await call.answer("Bu buyurtma allaqachon biriktirilgan!", show_alert=True)
        
    success = db.assign_courier(order_id, courier_id)
    if not success:
        return await call.answer("Qandaydir xato yuz berdi.", show_alert=True)
        
    await call.message.edit_text(call.message.text + "\n\n✅ BU KURYERGA TAYINLANDI")
    
    # Notify Courier
    user_id = order['user_id']
    user = db.detect_user(user_id)
    items_txt = db.get_order_items_text(order_id)
    
    text = (
        f"✅ ADMIN TOMONIDAN TAYINLANDINGIZ!\n"
        f"📦 Buyurtma #{order_id}\n\n"
        f"👤 Xaridor nomi: {user.get('username')}\n"
        f"📞 Telefon: {user.get('phone_number')}\n"
        f"📍 Joylashuv: {user.get('coordinates')}\n\n"
        f"🛒 Mahsulotlar:\n{items_txt}\n"
        f"💰 Ovqat narxi: {order['total_price']} so'm\n"
        f"🚚 Yetkazish narxi: {order['delivery_price']} so'm\n\n"
        "Holatni o'zgartirish uchun pastdagi tugmalardan foydalaning:"
    )
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧑‍🍳 Tayyorlanmoqda", callback_data=f"status_prep_{order_id}")],
        [InlineKeyboardButton(text="🍱 Tayyor", callback_data=f"status_ready_{order_id}")],
        [InlineKeyboardButton(text="🚙 Yo'lda", callback_data=f"status_road_{order_id}")],
        [InlineKeyboardButton(text="✅ Yetib kelindi", callback_data=f"status_done_{order_id}")]
    ])
    
    try:
        await bot.send_message(courier_id, text, reply_markup=kb)
    except:
        pass
        
    # Notify User
    courier = db.detect_courier(courier_id)
    distance = float(order['distance_km'])
    # Estimate ETA: ~ 3 mins per km + 10 mins prep
    eta = int(distance * 3) + 15
    try:
        await bot.send_message(
            user_id, 
            f"🚀 Sizga kuryer tayinlandi!\n\nKuryer nomi: {courier['username']}\nTelefon: {courier['phone']}\n\n⏳ Taxminiy yetib borish vaqti: {eta} daqiqa."
        )
    except:
        pass
