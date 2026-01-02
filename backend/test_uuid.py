import uuid
import datetime
from zoneinfo import ZoneInfo

uuid_7 = uuid.uuid7()
specific_date = "2026-01-01 16:20:00"
current = datetime.datetime.now()
specific_timestamp = int(datetime.datetime.fromisoformat(specific_date).replace(tzinfo=datetime.timezone.utc).timestamp() * 1000)

start_date = "2026-01-01 09:00:00"
end_date = "2026-01-02 18:00:00"

dt_start = datetime.datetime.combine(datetime.datetime.fromisoformat(start_date), datetime.time.min, tzinfo=datetime.timezone.utc)
dt_end = datetime.datetime.combine(datetime.datetime.fromisoformat(end_date), datetime.time.max, tzinfo=datetime.timezone.utc)

print(f"Generated UUID v7: {uuid_7}")
print(f"Current datetime: {current}")
print(f"UUID v7 from timestamp: {uuid.UUID(int=(int(current.timestamp() * 1000) << 80))}")
print(f"UUID v7 from specific date ({specific_date}): {uuid.UUID(int=(specific_timestamp << 80))}")

# uuid_7 = "019b77b1-b630-7316-8b80-bea033bd405d"

# uuid_to_string = str(uuid_7)

# string_to_uuid = uuid.UUID(uuid_to_string)

# uuid_to_timestamp = string_to_uuid.time

# # assert uuid_7 == string_to_uuid

# print(f"UUID v7: {uuid_7}")
# print(f"String representation: {uuid_to_string}")
# print(f"Converted back to UUID: {string_to_uuid}")
# print(f"Timestamp from UUID v7: {uuid_to_timestamp}")
# print(f"UUID time monotonic (ms since epoch): {string_to_uuid.int}")
# print(f"Current datetime: {datetime.datetime.now()}")
# print(f"Unix timestamp: {int(datetime.datetime.now().timestamp())}")

# to_date = datetime.datetime.fromtimestamp(
#     uuid_to_timestamp / 1000, tz=datetime.timezone.utc
# )

# print(f"Date from UUID timestamp: {to_date}")
# print(f"ISO format: {to_date.isoformat()}")

# # Timestamp in UUID v7 is in milliseconds since Unix epoch
# print(f"Formatted date: {to_date.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")

# # Convert back to UUID v7 from timestamp

# reconstructed_uuid = uuid.UUID(
#     int=(uuid_to_timestamp << 80) | (string_to_uuid.int & ((1 << 80) - 1))
# )