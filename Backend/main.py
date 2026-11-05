from datetime import date, datetime

from fastapi import FastAPI, HTTPException 
import functions
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
@app.get("/")
def hello():
    return {"message": "App running sucessfully"}

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http ://localhost:5173", "http://127.0.0.1:5173"],
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
def get_tutor(tutor_id):
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


@app.post("/sessions")
def request_session(
    tutor_id: int,
    student_roll_no: int,
    topic: str,
    session_date: date
):
    if not topic.strip():
        raise HTTPException(
            status_code=422,
            detail="Topic is required."
        )

    if session_date < date.today():
        raise HTTPException(
            status_code=422,
            detail="Session date cannot be in the past."
        )

    tutor = functions.get_tutor(id=tutor_id)
    if tutor is None:
        raise HTTPException(status_code=404, detail="Tutor not found.")

    if tutor.availability != "available":
        raise HTTPException(
            status_code=400,
            detail="This tutor is away right now."
        )

    if tutor.roll_no == student_roll_no:
        raise HTTPException(
            status_code=400,
            detail="You cannot request a session with yourself."
        )

    for existing_session in functions.get_sessions():
        if (
            existing_session.tutor_id == tutor_id
            and existing_session.student_roll_no == student_roll_no
            and existing_session.status in ["requested", "accepted"]
        ):
            raise HTTPException(
                status_code=400,
                detail="You already have a requested or accepted session with this tutor."
            )

    session_datetime = datetime.combine(session_date, datetime.min.time())

    new_session_id = functions.add_session(
        tutor_id=tutor_id,
        student_roll_no=student_roll_no,
        topic=topic,
        session_date=session_datetime
    )

    return {
        "message": "Session requested successfully.",
        "id": new_session_id,
        "status": "requested"
    }


@app.patch("/sessions/{session_id}/decision")
def decide_session(session_id: int, status: str):
    if status not in ["accepted", "rejected"]:
        raise HTTPException(
            status_code=422,
            detail="Status must be accepted or rejected."
        )

    session_record = functions.get_session(id=session_id)
    if session_record is None:
        raise HTTPException(status_code=404, detail="Session not found.")

    if session_record.status != "requested":
        raise HTTPException(
            status_code=400,
            detail="This session is no longer awaiting a decision."
        )

    if status == "accepted":
        accepted_on_date = [
            item for item in functions.get_sessions()
            if item.tutor_id == session_record.tutor_id
            and item.session_date.date() == session_record.session_date.date()
            and item.status == "accepted"
        ]

        if len(accepted_on_date) >= 3:
            raise HTTPException(
                status_code=400,
                detail="Tutor already has three accepted sessions on that date."
            )

    return functions.update_session_status(
        session_id=session_id,
        new_status=status
    )


@app.patch("/tutors/{tutor_id}")
def update_availability(tutor_id: int, available: int):

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





