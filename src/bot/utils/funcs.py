from typing import Any
from aiogram.methods import (
    SendMessage, SendPhoto, SendAudio, SendVoice, SendDocument, SendSticker, SendVideo, SendDice
)

Schema = (
    SendMessage
    | SendPhoto
    | SendAudio
    | SendVoice
    | SendDocument
    | SendSticker
    | SendVideo
    | SendDice
)


def get_schema(content_type: str, dump: dict[str, Any]) -> Schema:
    factories = {
        "text": lambda: SendMessage.model_validate(dump),
        "photo": lambda: SendPhoto.model_validate(dump),
        "video": lambda: SendVideo.model_validate(dump),
        "audio": lambda: SendAudio.model_validate(dump),
        "voice": lambda: SendVoice.model_validate(dump),
        "document": lambda: SendDocument.model_validate(dump),
        "sticker": lambda: SendSticker.model_validate(dump),
        "dice": lambda: SendDice.model_validate(dump) # incorrect values for interlocutor
    }

    try:
        return factories[content_type]()
    except Exception as e:
        raise Exception("Schema validation error", e)