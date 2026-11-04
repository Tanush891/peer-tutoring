# peer-tutoring


Problem statement

Students often need help with a subject but may not know which senior students can tutor them or how to arrange a session. At the same time, senior students need a simple way to offer subject support and manage requests around their availability. Our project provides a  platform where students can find tutors, request and track sessions, and rate completed tutoring. Tutors can manage their availability and accept or reject requests. The app uses roll numbers to identify students and tutors and does not require logins.


Role assigned:


Day1 : backend API 
Files required Main.py , functions.py , tutors.db libraries needed: FastAPI +SQLite
Tanush.k : last 5 end points
Abrar : first 5 end points 
Tables : Tutors, sessions
subject must be one of: maths, physics, chemistry, programming, electronics. status is one of: requested, accepted, rejected, completed.
Day2: Frontend 
FindTutor.jsx, MySession.jsx, Tutordesk.jsx in src/components and app.jsx in src 
Abrar: FindTutor.jsx and app.jsx
Tanush.k:  Mysession.jsx Tutordesk.jsx




API endpoints:

E1:  Get all the tutors. Can be filtered by subject. Each one includes its average rating and number of completed sessions.
Method:  GET
Path:  tutors
Request body: Subject = maths 
Success code:  200 (Tutors retrieved successfully )
 Error code:   422 (Invalid subject filter)


E2:  Get one tutor by its id, with their accepted sessions that are today or later.
Method: GET
Path:  tutors/ {tutors_id}
Request body:  None
Success code: 200 (Tutor retrieved successfully )
 Error code:  404 (Tutor not found. )


E3 : Sign up as a tutor: roll number, name and subject. It starts available.
Method:  Post
Path : tutors
Request body : {“roll_no”: “S001, “name”: “Asha”, “subject” : “maths”}
Success code:  201 (Tutor signed up successfully. )
Error code: 400 422  (This roll number is already registered for this subject.) 



E4 : Mark a tutor available or away.
Method : PATCH
Path : tutors/{tutor_id}/availability 
Request body: Available, set to true or false. 
Success code: 200  (Tutor availability updated successfully. )
Error code:  404 422 (Tutor not found. )



E5:  Request a session: tutor, student's 
roll number, topic and date. It starts as requested.
Method: POST
Path : sessions 
Request body: tutor_id, student_roll, topic, and session_date. 
Success code : 201 (Session requested successfully. )
Error code : 400 404   422  (This tutor is away right now. )


E6:  Get one tutor's requests that are still requested, oldest first.
Method: GET
Path : tutors/{tutor_id}/sessions/requests  
Request body : none
Success code : 200   (Pending requests retrieved successfully. )
Error code : 404  (Tutor not found.) 


E7 : Accept or reject a request.
Method: PATCH
Path: Sessions/{session_id}/decision 
Request body: status, set to accepted or rejected. 
Success code: 200 (Session request updated successfully. )
Error code: 400 404 422  (This session is no longer awaiting a decision. )



E8: Mark a session completed.
Method:  PATCH
Path: sessions/{session_id}/complete 
Request body: None. 
Success code: 200 (Session marked as completed successfully. )
Error code: 400 404 (Only accepted sessions on or after their scheduled date can be completed. )


E9: Rate a completed session from 1 to 5, with the student's roll number.
Method: PATCH
Path: sessions/{session_id}/rating 
Request body: student_roll and rating, from 1 to 5 .
Success code: 200 (Session rated successfully. )
Error code: 400 403 404 422  (You are not allowed to rate this session. )




E10: Get one student's sessions, by roll number. Each one includes the tutor's name and subject.
Method: GET
Path: students/{student_roll}/sessions
Request body: None. 
Success code: 200 (Student sessions retrieved successfully. )
Error code : 422  (Student roll number is required. )
