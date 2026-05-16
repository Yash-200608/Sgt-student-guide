from typing import Any

from app.config.database import get_collection
from app.schemas.preference import PreferenceOut, PreferenceUpdate
from app.utils.mongo import serialize_document

COLLECTION_NAME = "preferences"

DEFAULT_PREFERENCES = {
    "theme": "system",
    "notifications_enabled": True,
    "default_dashboard_view": "overview",
    "favorite_clubs": [],
}


def _collection():
    return get_collection(COLLECTION_NAME)


def _format_preferences(document: dict[str, Any] | None, user_id: str) -> dict[str, Any]:
    if document is None:
        data = {"id": "", "user_id": user_id, **DEFAULT_PREFERENCES}
    else:
        data = serialize_document(document) or {"id": "", "user_id": user_id}
        data = {**DEFAULT_PREFERENCES, **data}

    return PreferenceOut.model_validate(data).model_dump(mode="json")


async def get_preferences(user_id: str) -> dict[str, Any]:
    document = await _collection().find_one({"user_id": user_id})
    return _format_preferences(document, user_id)


async def update_preferences(user_id: str, payload: PreferenceUpdate) -> dict[str, Any]:
    update_data = payload.model_dump(mode="python", exclude_unset=True)
    base_data = {"user_id": user_id, **DEFAULT_PREFERENCES}
    await _collection().update_one(
        {"user_id": user_id},
        {"$setOnInsert": base_data, "$set": update_data},
        upsert=True,
    )
    document = await _collection().find_one({"user_id": user_id})
    return _format_preferences(document, user_id)
