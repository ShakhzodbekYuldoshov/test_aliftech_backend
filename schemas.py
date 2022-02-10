'''
SCHEMAS for models
'''

from pydantic import BaseModel
from typing import Optional


class PersonBase(BaseModel):
    age: int
    height_cm: float
    weight_kg: float
    body_fat_percent: float
    diastolic: float
    systolic: float
    grip_force: float
    sit_and_bend_forward_cm: float
    sit_ups_count: float
    broad_jump_cm: float
    gender: Optional[str] = None
    classification_probability: Optional[float] = None
