import xgboost as xgb
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import pandas as pd


# load model
model = xgb.XGBClassifier()
model.load_model('./models/best_gc.json')

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
    # prepare dataframe for prediction of the model
    col_names = ['age', 'height_cm', 'weight_kg', 'body fat_%', 'diastolic', 'systolic',
                 'gripForce', 'sit and bend forward_cm', 'sit-ups counts', 'broad jump_cm']

    data_list = [age, height_cm, weight_kg, body_fat_percent, diastolic, systolic,
                 grip_force, sit_and_bend_forward_cm, sit_ups_count, broad_jump_cm]

    df = pd.DataFrame(dict(zip(col_names, data_list)), index=[0])

    # run model
    prediction = model.predict(df)
    probability = model.predict_proba(df)[0]

    # make classification according to prediction result
    if prediction[0] == 0:
        classification = 'Female'
        probability = probability[0]
    elif prediction[0] == 1:
        classification = 'Male'
        probability = probability[1]

    return {"classification": str(classification), "probability": str(probability)}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, debug=True)
