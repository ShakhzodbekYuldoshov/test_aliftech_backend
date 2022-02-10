import xgboost as xgb
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from schemas import PersonBase
import uvicorn
import pandas as pd
from sqlalchemy.orm import Session
import crud
import models
from database import SessionLocal, engine


# load model
model = xgb.XGBClassifier()
model.load_model('./models/best_gc.json')

app = FastAPI()
# create database
models.Base.metadata.create_all(bind=engine)

# clients who could send request to backend without cors error
origins = [
    "http://localhost:8000",
]

# adding middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# used for getting dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/get_people_info/")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    '''
    GET method used for get info about all people
    '''
    people = crud.get_people(db, skip=skip, limit=limit)
    return people


@app.post("/classify_gender/")
def classify_gender(person: PersonBase, db: Session = Depends(get_db)):
    '''
    POST method used  for classifying gender

    '''
    # prepare dataframe for prediction of the model
    col_names = ['age', 'height_cm', 'weight_kg', 'body fat_%', 'diastolic', 'systolic',
                 'gripForce', 'sit and bend forward_cm', 'sit-ups counts', 'broad jump_cm']

    data_list = [person.age, person.height_cm, person.weight_kg, person.body_fat_percent, person.diastolic, person.systolic,
                 person.grip_force, person.sit_and_bend_forward_cm, person.sit_ups_count, person.broad_jump_cm]

    df = pd.DataFrame(dict(zip(col_names, data_list)), index=[0])

    # run model
    prediction = model.predict(df)
    probability = model.predict_proba(df)[0]

    # make classification according to prediction result
    if prediction[0] == 0:
        person.gender = 'Female'
        person.classification_probability = probability[0]
    elif prediction[0] == 1:
        person.gender = 'Male'
        person.classification_probability = probability[1]

    # create person object inside database
    crud.create_person(db=db, person=person)

    return {"classification": str(person.gender), "probability": str(person.classification_probability)}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, debug=True)
