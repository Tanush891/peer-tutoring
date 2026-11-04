from fastapi import FastAPI, HTTPException 
import functions
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
@app.get("/")
def hello():
    return {"message": "App running sucessfully"}

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)



@app.get("/tutors")
def get_tutors(subject=None):

    if subject:
        if subject not in ["maths", "physics", "chemistry", "programming", "electronics"]:
            raise HTTPException(status_code=422, detail="Invalid subject.")

    return functions.get_all_tutors(subject)


@app.get("/tutors/{tutor_id}")
def get_tutor(tutor_id: int):
    tutor = functions.get_tutor(id=tutor_id)
    if tutor is None:
        raise HTTPException(status_code=404, detail="Tutor not found.")

    return {
        "id": tutor.id,
        "name": tutor.name,
        "roll_no": tutor.roll_no,
        "subject": tutor.subject,
        "availability": tutor.availability,
    }


@app.post("/tutors")
def add_tutor(roll_no, name, subject):

    if not roll_no:
        raise HTTPException(status_code=422, detail="Roll number is required.")

    if not name:
        raise HTTPException(status_code=422, detail="Name is required.")

    if not subject:
        raise HTTPException(status_code=422, detail="Subject is required.")

    if subject not in ["maths", "physics", "chemistry", "programming", "electronics"]:
        raise HTTPException(status_code=422, detail="Invalid subject.")

    if functions.get_tutor_by_roll_subject(roll_no=roll_no, subject=subject) is not None:
        raise HTTPException(status_code=400, detail="Already registered for this subject.")

    return functions.add_tutor(
        roll_no=roll_no,
        name=name,
        subject=subject
    )

@app.patch("/tutors/{tutor_id}")
def update_availability(tutor_id, available):

    if not tutor_id:
        raise HTTPException(status_code=422, detail="Tutor ID is required.")

    if available not in [0, 1]:
        raise HTTPException(status_code=422, detail="Availability must be 0 or 1.")

    Tutor = functions.get_tutor(id=tutor_id)

    if Tutor is None:
        raise HTTPException(status_code=404, detail="Tutor not found.")

    return functions.update_availability(tutor_id=tutor_id, available=available)

@app.get("/tutors/{tutor_id}/requests")
def get_tutor_requests(tutor_id):

    if not tutor_id:
        raise HTTPException(status_code=422, detail="Tutor ID is required.")

    if functions.get_tutor(id=tutor_id) is None:
        raise HTTPException(status_code=404, detail="Tutor not found.")

    return functions.get_tutor_requests(tutor_id=tutor_id)


@app.get("/students/sessions")
def get_student_sessions(roll_no):

    if not roll_no:
        raise HTTPException(status_code=422, detail="Roll number is required.")

    return functions.get_student_sessions(roll_no=roll_no)
@app.patch("/sessions/{session_id}/complete")
def complete_session(session_id):

    if not session_id:
        raise HTTPException(status_code=422, detail="Session ID is required.")

    Session = functions.get_session(id=session_id)

    if Session is None:
        raise HTTPException(status_code=404, detail="Session not found.")

    if Session["status"] != "accepted":
        raise HTTPException(status_code=400, detail="This session is not accepted.")

    if Session["session_date"] > str(date.today()):
        raise HTTPException(status_code=400, detail="Session date has not arrived yet.")

    return functions.complete_session(session_id=session_id)


