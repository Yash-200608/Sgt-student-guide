import re
from typing import Any

from fastapi import HTTPException, status

from app.config.database import get_collection
from app.utils.mongo import serialize_documents


def _regex_query(query: str, fields: list[str]) -> dict[str, Any]:
    pattern = re.escape(query)
    return {"$or": [{field: {"$regex": pattern, "$options": "i"}} for field in fields]}


async def _search_collection(
    collection_name: str,
    query: str,
    fields: list[str],
    result_type: str,
    limit: int = 10,
) -> list[dict[str, Any]]:
    cursor = get_collection(collection_name).find(_regex_query(query, fields)).limit(limit)
    documents = await cursor.to_list(length=limit)
    results = serialize_documents(documents)
    return [{"type": result_type, **document} for document in results]


async def global_search(query: str) -> dict[str, Any]:
    normalized_query = query.strip()
    if len(normalized_query) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Search query must be at least 2 characters.",
        )

    teachers = await _search_collection(
        "teachers",
        normalized_query,
        ["name", "department", "email", "cabin"],
        "teacher",
    )
    events = await _search_collection(
        "events",
        normalized_query,
        ["title", "location", "venue", "description", "category"],
        "event",
    )
    clubs = await _search_collection(
        "clubs",
        normalized_query,
        ["name", "description", "category", "coordinator", "meeting_time"],
        "club",
    )
    notices = await _search_collection(
        "notices",
        normalized_query,
        ["title", "content"],
        "notice",
    )
    timetable = await _search_collection(
        "timetable",
        normalized_query,
        ["course", "subject", "teacher", "room", "section", "department"],
        "timetable",
    )
    transport = await _search_collection(
        "transport",
        normalized_query,
        ["route", "name", "from", "to"],
        "transport",
    )
    locations = await _search_collection(
        "locations",
        normalized_query,
        ["name", "description", "block", "building"],
        "location",
    )
    syllabus = await _search_collection(
        "syllabus",
        normalized_query,
        ["name", "subject", "description", "code"],
        "syllabus",
    )

    grouped = {
        "teachers": teachers,
        "events": events,
        "clubs": clubs,
        "notices": notices,
        "timetable": timetable,
        "transport": transport,
        "locations": locations,
        "syllabus": syllabus,
    }

    return {
        "query": normalized_query,
        "results": grouped,
        "total": sum(len(items) for items in grouped.values()),
    }
