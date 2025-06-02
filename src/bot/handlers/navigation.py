from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.states import NavigationState
from bot.keyboards import back_button
import logging

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "navigation_back")
async def back_handler(callback: CallbackQuery, state: FSMContext):
    logger.debug("Back button pressed")
    user_data = await state.get_data()
    navigation_data = user_data.get('navigation_data', {})

    stack = navigation_data.get('stack', [])
    logger.debug(f"navigation_data: {navigation_data}")
    if not navigation_data.get('stack'):
        await callback.answer("История пуста")
        return

    if len(stack) <= 1:
        await callback.answer("Это начальный экран")
        return

    # Удаляем текущее состояние из стека
    stack.pop()

    # Устанавливаем предыдущее состояние
    previous_state = stack[-1]
    await state.set_state(previous_state["state"])
    logger.debug(f"previous_state: {previous_state}")

    await callback.message.edit_text(
        previous_state['message'],
        reply_markup=back_button()
    )
    logger.debug(f"Back to: {previous_state['state']}")

    await state.update_data(navigation_data={"stack": stack})
    await callback.answer()
