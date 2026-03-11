from pydantic import BaseModel,ConfigDict
from typing import Optional
from datetime import date as dt_date


# ---------- Exercises ----------

class ExerciseCreate(BaseModel):
    name: str
    difficulty: str
    muscle_group: str


class ExerciseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    difficulty: str
    muscle_group: str
    is_active: bool




# ---------- Workouts ----------

class WorkoutCreate(BaseModel):
    name: str
    description: Optional[str] = None


class WorkoutOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: Optional[str] = None
    is_active: bool



# ---------- Progress ----------

class ProgressCreate(BaseModel):
    exercise_id: int
    reps: int
    date: Optional[dt_date] = None


class ProgressOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    exercise_id: int
    reps: int
    date: dt_date



# ---------- Workout ↔ Exercise relation ----------

class WorkoutExerciseCreate(BaseModel):
    workout_id: int
    exercise_id: int


class WorkoutExerciseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    workout_id: int
    exercise_id: int
