from aiogram import F
from aiogram.types import CallbackQuery
from router import router
from loader import db

@router.callback_query(F.data == "my_orders")
async def show_orders(call: CallbackQuery):
    telegram_id = str(call.from_user.id)
    sql = "SELECT id, total_price, delivery_price, status, created_at FROM orders WHERE user_id = %s ORDER BY id DESC LIMIT 5"
    orders = db.execute(sql, (telegram_id,), fetchall=True)
    if not orders:
        await call.answer("Hozircha buyurtmalaringiz yo'q 📭", show_alert=True)
        return

    status_icons = {
        "pending":              "⏳ Kutilmoqda",
        "accepted_by_courier":  "🚴 Kuryer qabul qildi",
        "Tayyorlanmoqda 🧑‍🍳":   "🧑‍🍳 Tayyorlanmoqda",
        "Tayyor 🍱":            "🍱 Tayyor",
        "Yo'lda 🚙":            "🚙 Yo'lda",
        "Yetkazib berildi ✅":   "✅ Yetkazib berildi",
    }

    text = (
        "📦 <b>Oxirgi buyurtmalaringiz</b>\n"
        "━━━━━━━━━━━━━━━━━\n\n"
    )
    for order in orders:
        status_label = status_icons.get(order['status'], f"🔹 {order['status']}")
        delivery = order.get('delivery_price') or 0
        total = float(order['total_price']) + float(delivery)
        text += (
            f"🧾 <b>#{order['id']}</b>  —  {status_label}\n"
            f"   💰 Ovqat: {order['total_price']:,} so'm\n".replace(",", " ") +
            f"   🚚 Yetkazish: {int(delivery):,} so'm\n".replace(",", " ") +
            f"   📊 Jami: {total:,.0f} so'm\n\n".replace(",", " ")
        )

    await call.answer()
    from keyboards.reply.main_menu import main_menu_inline
    await call.message.delete()
    await call.message.answer(text, reply_markup=main_menu_inline(), parse_mode="HTML")
