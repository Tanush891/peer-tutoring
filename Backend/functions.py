from sqlalchemy import Integer, String, Column, create_engine, DateTime, inspect, text
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime


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
    session_date = Column(DateTime, default=datetime)
    status = Column(String, default="requested", nullable=False)
    ratings = Column(Integer, nullable=True)


Base.metadata.create_all(engine)


def add_tutor(name, roll_no, subject, availability="available"):
    with Session(engine) as session:
        new_tutor = tutors(name=name, roll_no=roll_no, subject=subject, availability=availability)
        session.add(new_tutor)
        session.commit()

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

def get_all_tutors(subject):
    session = Session(engine)
    return session.query(tutors).all()

def get_tutor_by_roll_subject(roll_no, subject):
    with Session(engine) as session:
        return session.query(tutors).filter(
            tutors.roll_no == roll_no,
            tutors.subject == subject
        ).first()

def add_session(tutor_id, student_roll_no, topic, session_date):
    with Session(engine) as session:
        new_session = sessions(tutor_id=tutor_id, student_roll_no=student_roll_no, topic=topic, session_date=session_date)
        session.add(new_session)
        session.commit()

        return new_session.id

def get_sessions():
    session = Session(engine)
    return session.query(sessions).all()

def get_session(id):
    with Session(engine) as session:
        return session.query(sessions).filter(sessions.id == id).first()

def complete_session(session_id):
    with Session(engine) as session:
        session_record = session.query(sessions).filter(sessions.id == session_id).first()
        if session_record is None:
            return None

        session_record.status = "completed"
        session.commit()
        return {
            "id": session_record.id,
            "status": session_record.status,
        }

def update_session_status(session_id, new_status):
    with Session(engine) as session:
        session_record = session.query(sessions).filter(sessions.id == session_id).first()
        if session_record is None:
            return None

        session_record.status = new_status
        session.commit()
        return {
            "id": session_record.id,
            "status": session_record.status,
        }

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
    session = Session(engine)
    return session.query(sessions).all()

def add_rating(session_id, rating):
    with Session(engine) as session:
        session_to_update = session.query(sessions).filter(sessions.id == session_id).first()
        if session_to_update:
            session_to_update.ratings = rating
            session.commit()
