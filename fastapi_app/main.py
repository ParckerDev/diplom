from fastapi import FastAPI, APIRouter
from api import router as api_router


app = FastAPI()

app.include_router(api_router)


@app.get("/")
async def index():
    return {"message": "api rental equipments"}


if __name__=='__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)