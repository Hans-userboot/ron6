from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_URL

mongo_client = AsyncIOMotorClient(MONGO_URL)
mongodb = mongo_client.fsub

usersdb = mongodb.user
fsubdb = mongodb.fsub

#fsub
async def is_fsub(channel_id):
    fsub = await fsubdb.find_one({"channel_id": channel_id})
    if not fsub:
        return False
    return True


async def get_fsub() -> list:
    fsub_list = []
    async for channel in fsubdb.find({"channel_id": {"$gt": 0}}):
        fsub_list.append(channel_id)
    return fsub_list


async def add_fsub(channel_id):
    is_fsub = await is_fsub(channel_id)
    if is_fsub:
        return
    return await fsubdb.insert_one({"channel_id": channel_id})


async def remove_fsub(channel_id):
    async for channel in fsubdb.find({"channel_id": {"$gt": 0}}):
        if channel_id in channel:
            await fsubdb.delete_one({"channel_id": channel_id})

#user
async def is_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True


async def get_served_users() -> list:
    users_list = []
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list


async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"user_id": user_id})
