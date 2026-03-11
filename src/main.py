from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text, select
from sqlalchemy.orm import Session

from src.db import engine, Base, SessionLocal

from src.models import Exercise, Workout, Progress, WorkoutExercise
from src.schemas import (
    ExerciseCreate, ExerciseOut,
    WorkoutCreate, WorkoutOut,
    ProgressCreate, ProgressOut,
    WorkoutExerciseCreate, WorkoutExerciseOut
)
from datetime import date as dt_date

app = FastAPI(title="Calisthenics Tracker API")

# Crée les tables au démarrage (simple pour débuter)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except:
        return {"status": "unhealthy", "database": "disconnected"}

# --- Exercises CRUD ---

@app.post("/exercises", response_model=ExerciseOut)
def create_exercise(payload: ExerciseCreate, db: Session = Depends(get_db)):
    ex = Exercise(
        name=payload.name.strip(),
        difficulty=payload.difficulty.strip().lower(),
        muscle_group=payload.muscle_group.strip().lower(),
    )
    db.add(ex)
    db.commit()
    db.refresh(ex)
    return ex

@app.get("/exercises", response_model=list[ExerciseOut])
def list_exercises(db: Session = Depends(get_db)):
    result = db.execute(select(Exercise).order_by(Exercise.id))
    return result.scalars().all()

@app.get("/exercises/{exercise_id}", response_model=ExerciseOut)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    ex = db.get(Exercise, exercise_id)
    if not ex:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return ex

@app.delete("/exercises/{exercise_id}")
def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    ex = db.get(Exercise, exercise_id)
    if not ex:
        raise HTTPException(status_code=404, detail="Exercise not found")
    db.delete(ex)
    db.commit()
    return {"message": "Exercise deleted"}

# --- Workouts CRUD ---

@app.post("/workouts", response_model=WorkoutOut)
def create_workout(payload: WorkoutCreate, db: Session = Depends(get_db)):
    workout = Workout(
        name=payload.name.strip(),
        description=payload.description.strip() if payload.description else None,
    )
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout

@app.get("/workouts", response_model=list[WorkoutOut])
def list_workouts(db: Session = Depends(get_db)):
    result = db.execute(select(Workout).order_by(Workout.id))
    return result.scalars().all()

@app.get("/workouts/{workout_id}", response_model=WorkoutOut)
def get_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.get(Workout, workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout

@app.delete("/workouts/{workout_id}")
def delete_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.get(Workout, workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    db.delete(workout)
    db.commit()
    return {"message": "Workout deleted"}
# --- Progress CRUD ---

@app.post("/progress", response_model=ProgressOut)
def create_progress(payload: ProgressCreate, db: Session = Depends(get_db)):
    exercise = db.get(Exercise, payload.exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    progress = Progress(
        exercise_id=payload.exercise_id,
        reps=payload.reps,
        date=payload.date if payload.date else dt_date.today()
    )
    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress

@app.get("/progress", response_model=list[ProgressOut])
def list_progress(db: Session = Depends(get_db)):
    result = db.execute(select(Progress).order_by(Progress.id))
    return result.scalars().all()

@app.get("/progress/{progress_id}", response_model=ProgressOut)
def get_progress(progress_id: int, db: Session = Depends(get_db)):
    progress = db.get(Progress, progress_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    return progress

@app.delete("/progress/{progress_id}")
def delete_progress(progress_id: int, db: Session = Depends(get_db)):
    progress = db.get(Progress, progress_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    db.delete(progress)
    db.commit()
    return {"message": "Progress deleted"}

# --- Workout <-> Exercise Link ---

@app.post("/workout-exercises", response_model=WorkoutExerciseOut)
def add_exercise_to_workout(payload: WorkoutExerciseCreate, db: Session = Depends(get_db)):
    workout = db.get(Workout, payload.workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    exercise = db.get(Exercise, payload.exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    link = WorkoutExercise(
        workout_id=payload.workout_id,
        exercise_id=payload.exercise_id
    )
    db.add(link)
    db.commit()
    db.refresh(link)
    return link

@app.get("/workout-exercises", response_model=list[WorkoutExerciseOut])
def list_workout_exercises(db: Session = Depends(get_db)):
    result = db.execute(select(WorkoutExercise).order_by(WorkoutExercise.id))
    return result.scalars().all()

@app.delete("/workout-exercises/{link_id}")
def delete_workout_exercise(link_id: int, db: Session = Depends(get_db)):
    link = db.get(WorkoutExercise, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    db.delete(link)
    db.commit()
    return {"message": "Workout-Exercise link deleted"}
