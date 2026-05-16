from datetime import datetime, timezone
from typing import Any

from app.config.database import get_collection


async def get_admin_analytics() -> dict[str, Any]:
    users_collection = get_collection("users")
    events_collection = get_collection("events")
    attendance_collection = get_collection("attendance")

    total_users = await users_collection.count_documents({})
    active_events = await events_collection.count_documents(
        {"date": {"$gte": datetime.now(timezone.utc)}}
    )

    attendance_stats_cursor = attendance_collection.aggregate(
        [
            {
                "$group": {
                    "_id": None,
                    "average_percentage": {"$avg": "$percentage"},
                    "record_count": {"$sum": 1},
                }
            }
        ]
    )
    attendance_stats = await attendance_stats_cursor.to_list(length=1)

    department_metrics_cursor = users_collection.aggregate(
        [
            {"$match": {"department": {"$nin": [None, ""]}}},
            {
                "$group": {
                    "_id": "$department",
                    "total_users": {"$sum": 1},
                    "students": {
                        "$sum": {"$cond": [{"$eq": ["$role", "student"]}, 1, 0]}
                    },
                    "teachers": {
                        "$sum": {"$cond": [{"$eq": ["$role", "teacher"]}, 1, 0]}
                    },
                }
            },
            {"$sort": {"total_users": -1}},
        ]
    )
    department_metrics = await department_metrics_cursor.to_list(length=None)

    attendance_summary = attendance_stats[0] if attendance_stats else {}
    return {
        "total_users": total_users,
        "active_events": active_events,
        "attendance_statistics": {
            "average_percentage": round(
                attendance_summary.get("average_percentage") or 0,
                2,
            ),
            "record_count": attendance_summary.get("record_count", 0),
        },
        "department_metrics": [
            {
                "department": item["_id"],
                "total_users": item["total_users"],
                "students": item["students"],
                "teachers": item["teachers"],
            }
            for item in department_metrics
        ],
    }
