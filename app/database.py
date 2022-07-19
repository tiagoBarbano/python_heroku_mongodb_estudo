import motor.motor_asyncio

MONGO_DETAILS = "mongodb+srv://tiagoventura:jQG08nXHDLPADWGz@cluster0.1du3xts.mongodb.net/?retryWrites=true&w=majority"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.ESTUDO

user_collection = database.get_collection("users")

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "nome": user["nome"],
        "idade": user["idade"],
        "email": user["email"],
    }