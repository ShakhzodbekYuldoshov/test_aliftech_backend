from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/classify_gender/")
def classify_gender(
    age: int,
    height_cm: float,
    weight_kg: float,
    body_fat_percent: float,
    diastolic: float,
    systolic: float,
    grip_force: float,
    sit_and_bend_forward_cm: float,
    sit_ups_count: float,
    broad_jump_cm: float
):
    '''
    POST method used  for classifying gender

    '''

    return {"item_id": 'hello', "q": '1'}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, debug=True)
