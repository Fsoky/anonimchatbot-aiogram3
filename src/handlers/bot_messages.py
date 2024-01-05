from aiogram import Router, F
from aiogram.types import Message

from motor.core import AgnosticDatabase as MDB

router = Router()


@router.edited_message()
async def editing_messages(message: Message, db: MDB) -> None:
    user = await db.users.find_one({"_id": message.from_user.id})
    if user["status"] == 2:
        await message.bot.edit_message_text(
            message.text, user["interlocutor"], message.message_id + 1
        )


@router.message(
    F.content_type.in_(
        [
            "text", "audio", "voice",
            "sticker", "document", "photo",
            "video", "video_note", "animation"
        ]
    )
)
async def echo(message: Message, db: MDB) -> None:
    user = await db.users.find_one({"_id": message.from_user.id})
    
    if user["status"] == 2:
        if message.content_type == "text":
            reply = None
            if message.reply_to_message:
                if message.reply_to_message.from_user.id == message.from_user.id:
                    reply = message.reply_to_message.message_id + 1
                else:
                    reply = message.reply_to_message.message_id - 1

            await message.bot.send_message(
                user["interlocutor"],
                message.text,
                entities=message.entities,
                reply_to_message_id=reply,
                parse_mode=None
            )
        if message.content_type == "photo":
            await message.bot.send_photo(
                user["interlocutor"],
                message.photo[-1].file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                parse_mode=None
            )
        if message.content_type == "audio":
            await message.bot.send_audio(
                user["interlocutor"],
                message.audio.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                parse_mode=None
            )
        if message.content_type == "voice":
            await message.bot.send_voice(
                user["interlocutor"],
                message.voice.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                parse_mode=None
            )
        if message.content_type == "document":
            await message.bot.send_document(
                user["interlocutor"],
                message.document.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                parse_mode=None
            )
        if message.content_type == "sticker":
            await message.bot.send_sticker(
                user["interlocutor"],
                message.sticker.file_id
            )
        if message.content_type == "video":
            await message.bot.send_video(
                user["interlocutor"],
                message.video.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                parse_mode=None
            )
        if message.content_type == "video_note":
            await message.bot.send_video_note(
                user["interlocutor"],
                message.video_note.file_id
            )
        if message.content_type == "animation":
            await message.bot.send_animation(
                user["interlocutor"],
                message.video_note.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                parse_mode=None
            )