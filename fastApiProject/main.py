import uvicorn
import asyncio
import asyncpg
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.asyncio import engine
from sqlalchemy.ext.asyncio.session import AsyncSession

from core.check import check_email, check_login, check_phone

from db.pg_insert import save_data
from db.pg_insert import check_user

engine = engine.create_async_engine('postgresql+asyncpg://postgres:password@localhost/raw_data',
                                    echo=False,
                                    pool_size=10,
                                    future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000)


# async def get_session() -> AsyncSession


@app.post('/check')
async def check(body: dict = Body(...)):
    phone = email = login = None
    print(body)
    async with async_session() as session:
        try:
            phone = await check_phone(body['phone'])
            email = await check_email(body['email'])
            login = await check_login(body['login'])

            if (phone and email and login) is not None:
                await save_data(session, phone, email, login)
                return JSONResponse(content={"message": f"{phone}, {email}, {login}"}, status_code=200)
            else:
                # if phone == None:
                #     return JSONResponse(content={"message": "phone not valid"}, status_code=200)
                return JSONResponse(content={"message": f"data not valid {phone} {email} {login}"}, status_code=400)

        except Exception as ex:
            return JSONResponse(content={"message": f"error {ex}"}, status_code=400)


@app.get('/users/{user_id}')
async def user(user_id: int):
    async with async_session() as session:
        try:
            exist = await check_user(session, user_id)

            if exist is not None:
                return JSONResponse(content={"message": f"user {exist}"}, status_code=200)
            else:
                return JSONResponse(content={"message": f"user {user_id} not found"}, status_code=400)
        except Exception as ex:
            return JSONResponse(content={"message": f"error {ex}"}, status_code=400)


if __name__ == '__main__':
    uvicorn.run('main:app', port=8080, host='0.0.0.0', reload=True)
