from aiogram import Router, F
from aiogram.types import Message

from motor.core import AgnosticDatabase as MDB

from utils.funcs import get_schema

router = Router()
common_content_types = ["text"]
media_content_types = ["sticker", "photo", "video", "document", "voice", "audio"]


@router.edited_message()
async def editing_messages(message: Message, db: MDB) -> None:
    user = await db.users.find_one({"_id": message.from_user.id})
    if user["status"] == 2:
        if message.text:
            await message.bot.edit_message_text(
                message.text, user["interlocutor"], message.message_id + 1
            )
        elif message.caption:
            await message.bot.edit_message_caption(
                message.caption,
                user["interlocutor"],
                message.message_id + 1,
                caption_entities=message.caption_entities,
                parse_mode=None
            )


@router.message(F.content_type.in_(common_content_types + media_content_types))
async def echo(message: Message, db: MDB) -> None:
    user = await db.users.find_one({"_id": message.from_user.id})
    reply = None
    
    if user["status"] == 2:
        if message.reply_to_message:
            if message.reply_to_message.from_user.id == message.from_user.id:
                reply = message.reply_to_message.message_id + 1
            else:
                reply = message.reply_to_message.message_id - 1
        
        dump = message.model_dump()
        dump["chat_id"] = message.from_user.id
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