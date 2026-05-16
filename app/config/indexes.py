from motor.motor_asyncio import AsyncIOMotorDatabase


async def create_database_indexes(database: AsyncIOMotorDatabase) -> None:
    await database.users.create_index("email", unique=True)
    await database.users.create_index([("role", 1), ("department", 1), ("semester", 1)])

    await database.timetable.create_index([("section", 1), ("department", 1), ("semester", 1)])
    await database.timetable.create_index([("day", 1), ("time", 1)])
    await database.timetable.create_index(
        [("course", "text"), ("teacher", "text"), ("room", "text")]
    )

    await database.events.create_index("date")
    await database.events.create_index(
        [("title", "text"), ("location", "text"), ("description", "text")]
    )

    await database.notices.create_index([("is_global", 1), ("created_at", -1)])
    await database.notices.create_index("target_departments")
    await database.notices.create_index("target_semesters")

    await database.teachers.create_index([("department", 1), ("name", 1)])
    await database.teachers.create_index(
        [("name", "text"), ("department", "text"), ("email", "text")]
    )

    await database.clubs.create_index("name")
    await database.clubs.create_index([("name", "text"), ("description", "text")])

    await database.bookmarks.create_index([("user_id", 1), ("event_id", 1)], unique=True)
    await database.preferences.create_index("user_id", unique=True)

    await database.notifications.create_index([("user_id", 1), ("created_at", -1)])
    await database.notifications.create_index("target_roles")

    await database.attendance.create_index([("user_id", 1), ("course", 1)], unique=True)
    await database.attendance.create_index([("department", 1), ("semester", 1)])

    await database.bus_routes.create_index("route_number")
