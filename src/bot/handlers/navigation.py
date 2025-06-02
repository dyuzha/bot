from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.states import NavigationState
from bot.keyboards import back_button


router = Router()


@router.callback_query(F.data == "navigation_back")
async def back_handler(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    nav_data = user_data.get('navigation', {})

    if 'previous_state' in nav_data:
        await state.set_state(nav_data['previous_state'])
        await callback.message.edit_text(
            nav_data.get('previous_message', "Возврат"),
            reply_markup=back_button()  # Можно добавить дополнительные кнопки
        )
    else:
        await callback.answer("Нет истории для возврата")

    await callback.answer()
