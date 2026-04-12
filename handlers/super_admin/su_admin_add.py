from aiogram import types
from aiogram.fsm.context import FSMContext
from loader import s_id, db, bot
from router import router
from states.add_admin_state import AdminRegistrationForm

db = db

@router.message(lambda message: message.text == "/add_admin")
async def add_admin(message: types.Message, state: FSMContext):
    if not str(message.from_user.id) == str(s_id):
        await message.answer(
            "🚫 <b>Ruxsat yo'q!</b>\n\n"
            "<i>Faqat Super Admin ushbu amalni bajarishi mumkin.</i>",
            parse_mode="HTML"
        )
        return
    await state.clear()
    sent_msg = await bot.send_message(
        message.chat.id,
        "👤 <b>Yangi Admin qo'shish</b>\n"
        "━━━━━━━━━━━━━━━━━\n\n"
        "Adminning to'liq ismini kiriting:",
        parse_mode="HTML"
    )
    await state.set_state(AdminRegistrationForm.username)
    await state.update_data(message_ids=[sent_msg.message_id])


@router.message(AdminRegistrationForm.username)
async def add_admin_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    sent_msg = await bot.send_message(
        message.chat.id,
        f"✅ Ism qabul qilindi: <b>{message.text}</b>\n\n"
        f"🆔 Adminning Telegram ID sini kiriting:\n"
        f"<i>(ID ni bilish uchun @userinfobot dan foydalaning)</i>",
        parse_mode="HTML"
    )
    data = await state.get_data()
    message_ids = data.get('message_ids', [])
    message_ids.append(sent_msg.message_id)
    await state.update_data(message_ids=message_ids)
    await state.set_state(AdminRegistrationForm.telegram_id)


@router.message(AdminRegistrationForm.telegram_id)
async def add_admin_telegram_id(message: types.Message, state: FSMContext):
    if message.text and message.text.isdigit():
        await state.update_data(telegram_id=message.text)
        sent_msg = await bot.send_message(
            message.chat.id,
            f"✅ Telegram ID qabul qilindi: <code>{message.text}</code>\n\n"
            f"📱 Telefon raqamini kiriting:\n"
            f"<i>Masalan: +998901234567</i>",
            parse_mode="HTML"
        )
        data = await state.get_data()
        message_ids = data.get('message_ids', [])
        message_ids.append(sent_msg.message_id)
        await state.update_data(message_ids=message_ids)
        await state.set_state(AdminRegistrationForm.phone)
    else:
        sent_msg = await bot.send_message(
            message.chat.id,
            "❌ <b>Noto'g'ri format!</b>\n\n"
            "Telegram ID faqat raqamlardan iborat bo'lishi kerak.\n"
            "<i>Masalan: 123456789</i>",
            parse_mode="HTML"
        )
        data = await state.get_data()
        message_ids = data.get('message_ids', [])
        message_ids.append(sent_msg.message_id)
        await state.update_data(message_ids=message_ids)


@router.message(AdminRegistrationForm.phone)
async def add_admin_phone(message: types.Message, state: FSMContext):
    if message.text and (message.text.isdigit() or message.text.startswith('+')):
        await state.update_data(phone=message.text)
        data = await state.get_data()

        try:
            db.add_admin(data["telegram_id"], data["username"], data["phone"])
            success_msg = await bot.send_message(
                message.chat.id,
                f"✅ <b>Admin muvaffaqiyatli qo'shildi!</b>\n"
                f"━━━━━━━━━━━━━━━━━\n\n"
                f"👤 <b>Ismi:</b> {data['username']}\n"
                f"🆔 <b>Telegram ID:</b> <code>{data['telegram_id']}</code>\n"
                f"📱 <b>Telefon:</b> {data['phone']}",
                parse_mode="HTML"
            )
            # Delete previous
            message_ids = data.get('message_ids', [])
            for msg_id in message_ids:
                try:
                    await bot.delete_message(message.chat.id, msg_id)
                except Exception as e:
                    print(f"Failed to delete message {msg_id}: {e}")
            await state.clear()
        except Exception as e:
            print(f"DB Error: {e}")
            error_msg = await bot.send_message(
                message.chat.id,
                "❌ <b>Xatolik yuz berdi!</b>\n\n"
                "<i>Balki bu Telegram ID allaqachon ro'yxatda bor. Qayta urinib ko'ring.</i>",
                parse_mode="HTML"
            )
            # Delete previous, keep error
            message_ids = data.get('message_ids', [])
            for msg_id in message_ids:
                try:
                    await bot.delete_message(message.chat.id, msg_id)
                except Exception as e:
                    print(f"Failed to delete message {msg_id}: {e}")
            await state.clear()
    else:
        sent_msg = await bot.send_message(
            message.chat.id,
            "❌ <b>Noto'g'ri format!</b>\n\n"
            "Telefon raqam <b>+</b> bilan yoki faqat raqamlar bo'lishi kerak.\n"
            "<i>Masalan: +998901234567</i>",
            parse_mode="HTML"
        )
        data = await state.get_data()
        message_ids = data.get('message_ids', [])
        message_ids.append(sent_msg.message_id)
        await state.update_data(message_ids=message_ids)