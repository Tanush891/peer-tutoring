from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    create_engine,
    inspect,
    text,
)
from sqlalchemy.orm import Session, declarative_base

DB_PATH = "tutoring.db"
engine = create_engine(f"sqlite:///{DB_PATH}")

Base = declarative_base()


class tutors(Base):
    __tablename__ = "tutors"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    roll_no = Column(Integer)
    subject = Column(String)
    availability = Column(String)


class sessions(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    tutor_id = Column(Integer)
    student_roll_no = Column(Integer)
    topic = Column(String)
    session_date = Column(DateTime, default=datetime.now)
    status = Column(String, default="requested", nullable=False)
    ratings = Column(Integer, nullable=True)


Base.metadata.create_all(engine)


def _migrate_session_status():
    if "status" not in {
        column["name"] for column in inspect(engine).get_columns("sessions")
    }:
        with engine.begin() as connection:
            connection.execute(
                text(
                    "ALTER TABLE sessions "
                    "ADD COLUMN status VARCHAR NOT NULL DEFAULT 'requested'"
                )
            )


_migrate_session_status()


def add_tutor(name, roll_no, subject, availability="available"):
    with Session(engine) as session:
        tutor = tutors(
            name=name,
            roll_no=roll_no,
            subject=subject,
            availability=availability,
        )
        session.add(tutor)
        session.commit()
        return "Tutor added successfully"


def get_tutors(subject=None):
    with Session(engine) as session:
        query = session.query(tutors)
        if subject:
            query = query.filter(tutors.subject == subject)
        return query.all()


def get_tutor(id):
    with Session(engine) as session:
        return session.query(tutors).filter(tutors.id == id).first()


def update_availability(tutor_id, available):
    with Session(engine) as session:
        tutor = session.query(tutors).filter(tutors.id == tutor_id).first()
        if tutor is None:
            return None

        tutor.availability = "available" if available == 1 else "unavailable"
        session.commit()
        return {
            "id": tutor.id,
            "availability": tutor.availability,
        }


def get_all_tutors(subject=None):
    return get_tutors(subject)


def get_tutor_by_roll_subject(roll_no, subject):
    with Session(engine) as session:
        return (
            session.query(tutors)
            .filter(tutors.roll_no == roll_no, tutors.subject == subject)
            .first()
        )


def add_session(tutor_id, student_roll_no, topic, session_date):
    with Session(engine) as session:
        new_session = sessions(
            tutor_id=tutor_id,
            student_roll_no=student_roll_no,
            topic=topic,
            session_date=session_date,
        )
        session.add(new_session)
        session.commit()
        return "Session created successfully"


def get_sessions():
    with Session(engine) as session:
        return session.query(sessions).all()


def get_tutor_requests(tutor_id):
    with Session(engine) as session:
        return (
            session.query(sessions)
            .filter(
                sessions.tutor_id == tutor_id,
                sessions.status == "requested",
            )
            .order_by(sessions.session_date.asc(), sessions.id.asc())
            .all()
        )


def get_student_sessions(roll_no):
    with Session(engine) as session:
        student_sessions = (
            session.query(sessions, tutors.name, tutors.subject)
            .join(tutors, sessions.tutor_id == tutors.id)
            .filter(sessions.student_roll_no == roll_no)
            .order_by(sessions.session_date.asc(), sessions.id.asc())
            .all()
        )
        return [
            {
                "id": student_session.id,
                "tutor_id": student_session.tutor_id,
                "student_roll_no": student_session.student_roll_no,
                "topic": student_session.topic,
                "session_date": student_session.session_date,
                "status": student_session.status,
                "ratings": student_session.ratings,
                "tutor_name": tutor_name,
                "subject": subject,
            }
            for student_session, tutor_name, subject in student_sessions
        ]


def status():
    return get_sessions()


def add_rating(session_id, rating):
    with Session(engine) as session:
        session_data = (
            session.query(sessions).filter(sessions.id == session_id).first()
        )
        if session_data is None:
            return "Session not found"

        session_data.ratings = rating
        session.commit()
        return "Rating added successfully"
