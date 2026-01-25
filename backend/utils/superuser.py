from config.db import Session
import asyncio
from sqlalchemy import text
from models.user import User
from getpass import getpass
import bcrypt


async def create_superuser():
    print("Create Superuser Account")
    username = input("Username: ")
    password = getpass("Password: ")
    confirm_password = getpass("Confirm Password: ")

    if password != confirm_password:
        print("Error: Passwords do not match.")
        return

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    async with Session() as session:
        async with session.begin():
            existing_user = await session.execute(
                text("SELECT * FROM users WHERE username = :username"),
                {"username": username},
            )
            if existing_user.first():
                print("Error: Username already exists.")
                return

            new_user = User(
                username=username,
                password_hash=hashed_password.decode("utf-8"),
                is_superuser=True,
            )
            session.add(new_user)
            await session.commit()

    print(f"Superuser '{username}' created successfully.")


if __name__ == "__main__":
    asyncio.run(create_superuser())
