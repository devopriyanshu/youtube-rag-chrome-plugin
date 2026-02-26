from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "FastAPI is running 🚀"}


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}