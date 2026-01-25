import datetime
from uuid import UUID


def get_uuidv7_from_timestamp(time_str: str, is_end=False) -> UUID:
    is_date_only = len(time_str) == 10

    try:
        dt = datetime.datetime.fromisoformat(time_str)
    except ValueError as e:
        raise ValueError(f"Invalid time format: {time_str}") from e

    if is_date_only:
        target_time = datetime.time.max if is_end else datetime.time.min
        dt = datetime.datetime.combine(dt.date(), target_time)

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    else:
        dt = dt.astimezone(datetime.timezone.utc)

    timestamp_ms = int(dt.timestamp() * 1000)

    uuid_int = (timestamp_ms & 0xFFFFFFFFFFFF) << 80

    uuid_int |= 0x7 << 76  # Set version to 7

    uuid_int |= 0x2 << 62  # Set variant to RFC 4122

    if is_end:
        uuid_int |= 0x000000000FFF3FFFFFFFFFFFFFFF

    return UUID(int=uuid_int)
