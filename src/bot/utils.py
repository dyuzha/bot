
from typing import Optional
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup


async def push_to_stack(fsm: FSMContext, text: str, keyboard: Optional[InlineKeyboardMarkup] = None):
    user_data = await fsm.get_data()
    navigation_data = user_data.get("navigation_data", {"stack": []})

    navigation_data["stack"].append({
        "state": await fsm.get_state(),
        "message": text,
        "keyboard": keyboard.model_dump() if keyboard else None
    })

    if len(navigation_data["stack"]) > 10:
        navigation_data["stack"] = navigation_data["stack"][-10:]

    await fsm.update_data(navigation_data=navigation_data)
