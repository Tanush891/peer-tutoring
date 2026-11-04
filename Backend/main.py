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

    return functions.get_all_tutors(subject=subject)


@app.get("/tutors/{tutor_id}")
def get_tutor(tutor_id: int):

    response = functions.get_tutor(id=tutor_id)
    code = response["code"]

    if code == 200:
        return response["tutor"]

    raise HTTPException(status_code=code, detail=response["msg"])


