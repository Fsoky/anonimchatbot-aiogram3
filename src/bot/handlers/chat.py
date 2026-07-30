from typing import Literal

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, StateFilter, or_f
from aiogram.fsm.scene import Scene, on
from aiogram.fsm.context import FSMContext

from fluentogram import TranslatorRunner

from src.bot.keyboards.builders import chat_markup
from src.bot.filters import FText
from src.bot.utils.funcs import get_schema

from src.db.repositories import UserRepository
from src.db.utils.enums import Status

common_content_types = {"text", "dice"}
media_content_types = {"sticker", "photo", "video", "document", "voice", "audio"}


async def _leave_from_dialog(
    message: Message,
    user_repo: UserRepository,
    state: FSMContext,
    i18n: TranslatorRunner
) -> None:
    user = await user_repo.one(_id=message.from_user.id)
    
    match user.status:
        case Status.CHATTING:
            if user.interlocutor_id is None:
                return None

            await message.reply(i18n.you_leave(), reply_markup=chat_markup(i18n))
            await message.bot.send_message(
                user.interlocutor_id, i18n.interlocutor_leave(), reply_markup=chat_markup(i18n)
            )

            await user_repo.update_many(
                [message.from_user.id, user.interlocutor_id],
                {"$set": {"status": 0, "interlocutor_id": None}}
            )
            
            await state.clear()
    
    return None


class Chat(Scene, state="chat"):
    
    @on.message.enter()
    async def on_enter(
        self,
        message: Message,
        state: FSMContext,
        user_repo: UserRepository,
        i18n: TranslatorRunner,
        _action: Literal["search"] | None = None
    ) -> None:
        match _action:
            case "search":
                pattern = {
                    "text": i18n.dialog_active(),
                    "reply_markup": chat_markup(i18n, 2)
                }
                
                user = await user_repo.one(_id=message.from_user.id)
                
                match user.status:
                    case Status.IDLE:
                        interlocutor = await user_repo.one(status=Status.SEARCHING)
                        await user_repo.update(user.id, {"$set": {"status": 1}})
                        
                        if not interlocutor:
                            pattern["text"] = i18n.search_started()
                            pattern["reply_markup"] = chat_markup(i18n, 3)
                        else:
                            pattern["text"] = i18n.interlocutor_found()
                            
                            await user_repo.update(
                                user.id, {"$set": {"status": 2, "interlocutor_id": interlocutor.id}}
                            )
                            await user_repo.update(
                                interlocutor.id, {"$set": {"status": 2, "interlocutor_id": user.id}}
                            )
                            
                            await message.bot.send_message(interlocutor.id, **pattern)
                    case Status.SEARCHING:
                        pattern["text"] = i18n.already_searching()
                        pattern["reply_markup"] = chat_markup(i18n, 3)

                await message.reply(**pattern)
            case _:
                searchers = await user_repo.count(status=Status.SEARCHING)
                await message.reply(
                    i18n.welcome(searchers=searchers), reply_markup=chat_markup(i18n)
                )
    
    @on.message(or_f(Command("search"), FText(equals="search")))
    async def search_dialog(self, message: Message, state: FSMContext) -> None:
        await self.wizard.retake(_action="search")
    
    @on.message(or_f(Command("cancel"), FText(equals="cancel")))
    async def cancel_dialog(
        self,
        message: Message,
        state: FSMContext,
        user_repo: UserRepository,
        i18n: TranslatorRunner
    ) -> None:
        user = await user_repo.one(_id=message.from_user.id)
        match user.status:
            case Status.SEARCHING:
                await user_repo.update(message.from_user.id, {"$set": {"status": 0}})
                await message.reply(i18n.no_search_now(), reply_markup=chat_markup(i18n))

    @on.message(or_f(Command("leave"), FText(equals="leave")))
    async def leave_dialog(
        self,
        message: Message,
        state: FSMContext,
        user_repo: UserRepository,
        i18n: TranslatorRunner
    ) -> None:
        await _leave_from_dialog(message, user_repo, state, i18n)

    @on.message(Command("next"))
    async def next_search(
        self,
        message: Message,
        state: FSMContext,
        user_repo: UserRepository,
        i18n: TranslatorRunner
    ) -> None:
        await _leave_from_dialog(message, user_repo, state, i18n)
        await self.wizard.retake(_action="search")

    @on.message(F.content_type.in_(common_content_types | media_content_types))
    async def echo(self, message: Message, state: FSMContext, user_repo: UserRepository) -> None:
        user = await user_repo.one(_id=message.from_user.id)
        reply = None
        
        if user.status == Status.CHATTING:
            if message.reply_to_message:
                if message.reply_to_message.from_user.id == message.from_user.id:
                    reply = message.reply_to_message.message_id + 1
                else:
                    reply = message.reply_to_message.message_id - 1
            
            dump = message.model_dump()
            dump["chat_id"] = user.interlocutor_id
            dump["parse_mode"] = None
            dump["reply_to_message_id"] = reply

            if message.content_type in media_content_types:
                attr = getattr(message, message.content_type)
                if isinstance(attr, list):
                    file_id = attr[-1].file_id
                else:
                    file_id = attr.file_id
                dump[message.content_type] = file_id

            schema = get_schema(message.content_type, dump)
            await message.bot(schema)


router = Router(name=__file__)
router.message.register(Chat.as_handler(), CommandStart())


@router.edited_message(StateFilter("chat"))
async def editing_messages(message: Message, state: FSMContext, user_repo: UserRepository) -> None:
    user = await user_repo.one(_id=message.from_user.id)
    if user.status == Status.CHATTING:
        if message.text:
            await message.bot.edit_message_text(
                text=message.text,
                chat_id=user.interlocutor_id,
                message_id=message.message_id + 1,
                parse_mode=None
            )
        elif message.caption:
            await message.bot.edit_message_caption(
                caption=message.caption,
                chat_id=user.interlocutor_id,
                message_id=message.message_id + 1,
                caption_entities=message.caption_entities,
                parse_mode=None
            )