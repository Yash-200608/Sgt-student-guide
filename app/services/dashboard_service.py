from typing import Any

from app.services import bookmark_service, notice_service, preference_service, timetable_service


async def get_personal_dashboard(user: dict[str, Any]) -> dict[str, Any]:
    user_id = user["id"]
    timetable = await timetable_service.get_personalized_timetable(user)
    notices = await notice_service.get_personalized_notices(user)
    bookmarked_events = await bookmark_service.get_bookmarked_events(user_id)
    preferences = await preference_service.get_preferences(user_id)

    return {
        "profile": user,
        "timetable": timetable,
        "notices": notices,
        "bookmarked_events": bookmarked_events,
        "preferences": preferences,
        "summary": {
            "timetable_count": len(timetable),
            "notice_count": len(notices),
            "bookmark_count": len(bookmarked_events),
        },
    }
