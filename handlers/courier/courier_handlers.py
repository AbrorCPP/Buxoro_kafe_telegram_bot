from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loader import db, bot
from router import router


@router.callback_query(F.data.startswith("volunteer_"))
async def volunteer_order(call: CallbackQuery):
    courier_id = str(call.from_user.id)
    order_id = call.data.split("_")[1]

    order = db.get_order(order_id)
    if order and order['courier_id']:
        return await call.answer("❌ Bu buyurtma allaqachon biriktirilgan!", show_alert=True)

    courier = db.detect_courier(courier_id)
    if not courier:
        return await call.answer("🚫 Siz kuryer emassiz!", show_alert=True)

    db.add_order_bid(order_id, courier_id)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(
        f"✅ <b>Talab yuborildi!</b>\n\n"
        f"🧾 Buyurtma: <b>#{order_id}</b>\n"
        f"<i>Admin tasdiqlashini kuting...</i>",
        parse_mode="HTML"
    )

    from config import S_ADMIN
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Tayinlash", callback_data=f"assign_{order_id}_{courier_id}")]
    ])
    notification_text = (
        f"🔔 <b>Yangi nomzod kuryer!</b>\n"
        f"━━━━━━━━━━━━━━━━━\n\n"
        f"👤 <b>Ismi:</b> {courier['username']}\n"
        f"📞 <b>Telefon:</b> {courier['phone']}\n"
        f"🧾 <b>Buyurtma:</b> #{order_id}\n\n"
        f"<i>Tayinlamoqchimisiz?</i>"
    )

    notified_ids = set()
    try:
        await bot.send_message(S_ADMIN, notification_text, reply_markup=kb, parse_mode="HTML")
        notified_ids.add(str(S_ADMIN))
    except:
        pass

    admin_ids = db.get_all_admin_ids()
    for admin in (admin_ids or []):
        admin_tg_id = str(admin.get('telegram_id', ''))
        if admin_tg_id and admin_tg_id not in notified_ids:
            try:
                await bot.send_message(admin_tg_id, notification_text, reply_markup=kb, parse_mode="HTML")
                notified_ids.add(admin_tg_id)
            except:
                pass


@router.callback_query(F.data.startswith("status_"))
async def change_order_status(call: CallbackQuery):
    data = call.data.split("_")
    action = data[1]
    order_id = data[2]

    status_map = {
        "prep":  ("Tayyorlanmoqda 🧑‍🍳",  "🧑‍🍳 <b>Buyurtmangiz tayyorlanmoqda!</b>\n\nOshpazlar ishlayapti, biroz sabr qiling 😊"),
        "ready": ("Tayyor 🍱",             "🍱 <b>Buyurtmangiz tayyor!</b>\n\nKuryer tez orada sizga yo'l oladi!"),
        "road":  ("Yo'lda 🚙",             "🚙 <b>Kuryer yo'lda!</b>\n\nBuyurtmangiz sizga kelmoqda, biroz kuting."),
        "done":  ("Yetkazib berildi ✅",   "✅ <b>Buyurtmangiz yetkazib berildi!</b>\n\n🍽 Yoqimli ishtaha!\n<i>E'tiboringiz uchun rahmat! 🙏</i>"),
    }

    new_status, user_msg = status_map.get(action, (None, None))
    if not new_status:
        return await call.answer("Noto'g'ri holat!", show_alert=True)

    db.update_order_status(order_id, new_status)

    order = db.get_order(order_id)
    try:
        await bot.send_message(order['user_id'], user_msg, parse_mode="HTML")
    except:
        pass

    await call.answer(f"✅ Holat: {new_status}", show_alert=True)
