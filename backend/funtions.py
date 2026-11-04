from sqlalchemy import Integer, String, Column, create_engine, DateTime
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime


DB_PATH = "tutoring.db"
engine = create_engine("sqlite:///{DB_PATH}")
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
    ratings = Column(Integer, nullable=True)


Base.metadata.create_all(engine)

def add_tutor(name, roll_no, subject, availability):
    with Session(engine) as session:
        new_tutor = tutors(name=name, roll_no=roll_no, subject=subject, availability=availability)
        session.add(new_tutor)
        session.commit()   

def get_tutors():
    session = Session(engine)
    return session.query(tutors).all()   

def get_all_tutors():
    session = Session(engine)
    return session.query(tutors).all()

def add_session(tutor_id, student_roll_no, topic, session_date):
    with Session(engine) as session:
        new_session = sessions(tutor_id=tutor_id, student_roll_no=student_roll_no, topic=topic, session_date=session_date)
        session.add(new_session)
        session.commit()

def get_sessions():
    session = Session(engine)
    return session.query(sessions).all()

def status():
    session = Session(engine)
    return session.query(sessions).all()

def add_rating(session_id, rating):
    with Session(engine) as session:
        session_to_update = session.query(sessions).filter(sessions.id == session_id).first()
        if session_to_update:
            session_to_update.ratings = rating
            session.commit()           


