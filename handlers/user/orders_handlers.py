from aiogram import F
from aiogram.types import CallbackQuery
from router import router
from loader import db

@router.callback_query(F.data == "my_orders")
async def show_orders(call: CallbackQuery):
    telegram_id = str(call.from_user.id)
    sql = "SELECT id, total_price, status FROM orders WHERE user_id = %s ORDER BY id DESC LIMIT 5"
    orders = db.execute(sql, (telegram_id,), fetchall=True)
    if not orders:
        await call.answer("Sizda hali buyurtmalar yo'q.", show_alert=True)
        return
        
    text = "Sizning oxirgi 5 ta buyurtmangiz:\n\n"
    for order in orders:
        text += f"🧾 Buyurtma #{order['id']} - {order['total_price']} so'm ({order['status']})\n"
        
    await call.answer()
    from keyboards.reply.main_menu import main_menu_inline
    await call.message.delete()
    await call.message.answer(text, reply_markup=main_menu_inline())
