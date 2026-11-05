from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base, Session
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
    session_date = Column(DateTime, default=datetime.now)
    ratings = Column(Integer, nullable=True)


Base.metadata.create_all(engine)


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

        if subject:
            return session.query(tutors).filter(
                tutors.subject == subject
            ).all()

        return session.query(tutors).all()


def get_tutor(tutor_id):
    with Session(engine) as session:
        return session.query(tutors).filter(
            tutors.id == tutor_id
        ).first()


def get_all_tutors(subject=None):
    return get_tutors(subject)


def get_tutor_by_roll_subject(roll_no, subject):
    with Session(engine) as session:
        return session.query(tutors).filter(
            tutors.roll_no == roll_no,
            tutors.subject == subject
        ).first()


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


def status():
    return get_sessions()


def add_rating(session_id, rating):
    with Session(engine) as session:

        session_data = session.query(sessions).filter(
            sessions.id == session_id
        ).first()

        if session_data is None:
            return "Session not found"

        session_data.ratings = rating

        session.commit()

        return "Rating added successfully"


