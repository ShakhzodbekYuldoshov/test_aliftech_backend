from sqlalchemy.orm import Session

import models
import schemas


def get_people(db: Session, skip: int = 0, limit: int = 100):
    '''
    function to get all people from database
    '''
    return db.query(models.Person).offset(skip).limit(limit).all()


def create_person(db: Session, person: schemas.PersonBase):
    '''
    function to create person in database table
    '''
    db_person = models.Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person
