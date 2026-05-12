import asyncio
from uuid import uuid4
from sqlalchemy import select
from fitlife.database import new_session
from fitlife.admin.models import AdminModel
from fitlife.security import Security
from fitlife.schemas import UserRoles


async def create_admin(first_name, last_name, phone_number, email, password):
    async with new_session() as session:
        # Check if admin already exists
        stmt = select(AdminModel).where(AdminModel.phone_number == phone_number)
        result = await session.execute(stmt)
        if result.scalar_one_or_none():
            print(f"Admin with phone {phone_number} already exists")
            return

        hashed_password = Security.hash_password(password)
        admin = AdminModel(
            id=uuid4(),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            password=hashed_password,
            role=UserRoles.ADMIN.value,
        )
        session.add(admin)
        await session.commit()
        print(f"Admin {first_name} {last_name} created successfully")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 6:
        print(
            "Usage: python create_admin.py <first_name> <last_name> <phone_number> <email> <password>"
        )
    else:
        asyncio.run(
            create_admin(
                sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
            )
        )
