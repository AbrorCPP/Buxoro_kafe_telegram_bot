from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from router import router
from states.add_product_state import ProductAdd
from keyboards.inline.category_add_p import category_keyboard
from loader import db

@router.message(F.text == "/add_product")
async def start_add_product(message: Message, state: FSMContext):
    categories = db.execute("SELECT id, name FROM categories", fetchall=True)
    kb = await category_keyboard(categories)
    await message.answer(
        "🛍 <b>Yangi mahsulot qo'shish</b>\n"
        "━━━━━━━━━━━━━━━━━\n\n"
        "Mahsulot qaysi kategoriyaga tegishli?",
        reply_markup=kb,
        parse_mode="HTML"
    )
    await state.set_state(ProductAdd.waiting_for_category)

@router.callback_query(ProductAdd.waiting_for_category, F.data.startswith("cat_"))
async def process_category(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.split("_")[1])
    await state.update_data(category_id=category_id)
    await callback.message.edit_text(
        "✏️ <b>Mahsulot nomi</b>\n\n"
        "Mahsulot nomini kiriting:",
        parse_mode="HTML"
    )
    await state.set_state(ProductAdd.waiting_for_name)
    await callback.answer()

@router.message(ProductAdd.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        "📝 <b>Tavsif</b>\n\n"
        "Mahsulot tavsifini kiriting:",
        parse_mode="HTML"
    )
    await state.set_state(ProductAdd.waiting_for_description)

@router.message(ProductAdd.waiting_for_description)
async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(
        "💰 <b>Narx</b>\n\n"
        "Narxni kiriting (faqat raqam, so'mda):\n"
        "<i>Masalan: 25000</i>",
        parse_mode="HTML"
    )
    await state.set_state(ProductAdd.waiting_for_price)

@router.message(ProductAdd.waiting_for_price)
async def process_price(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer(
            "❌ <b>Noto'g'ri format!</b>\n\n"
            "Faqat raqam kiriting. Masalan: <code>25000</code>",
            parse_mode="HTML"
        )
    await state.update_data(price=int(message.text))
    await message.answer(
        "🖼 <b>Rasm</b>\n\n"
        "Mahsulot rasmini yuboring yoki rasm file_id sini kiriting:",
        parse_mode="HTML"
    )
    await state.set_state(ProductAdd.waiting_for_photo)

@router.message(ProductAdd.waiting_for_photo, F.text)
async def process_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.text)
    data = await state.get_data()

    success = db.add_new_product(
        category_id=data['category_id'],
        name=data['name'],
        description=data['description'],
        price=data['price'],
        image_id=data['photo']
    )

    if success:
        await message.answer(
            f"✅ <b>Mahsulot muvaffaqiyatli qo'shildi!</b>\n\n"
            f"🏷 <b>Nomi:</b> {data['name']}\n"
            f"💰 <b>Narxi:</b> {data['price']:,} so'm".replace(",", " "),
            parse_mode="HTML"
        )
    else:
        await message.answer(
            "❌ <b>Xatolik yuz berdi!</b>\n\n"
            "<i>Iltimos, qayta urinib ko'ring.</i>",
            parse_mode="HTML"
        )

    await state.clear()