from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession


async def check_user(session: AsyncSession, user_id):
    query = text(f"""
        select user_id
        from users
        where user_id = :user_id
        limit 1
    """)

    data = await session.execute(query, {"user_id": user_id})
    data = data.fetchone()
    await session.commit()
    if data not in ([], None):
        return True
    else:
        return False


async def save_data(session: AsyncSession, user_id, phone, email, login):
    query = text(f"""
        insert into users(user_id, phone, email, login) 
        values (:user_id, :phone, :email, :login)
        """)

    await session.execute(query, {"user_id": user_id,
                                  "phone": phone,
                                  "email": email,
                                  "login": login})

    await session.commit()
