from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from agent import run_agent

class Question(BaseModel) :
    question : str
app = FastAPI()

@app.post("/ask")
def ask(request : Question):
    try : 
        return {"answer" : run_agent(request.question)}
    except Exception as e : 
        print(f"Error in /ask: {e}")
        raise HTTPException(status_code=500 , detail="there was an error occured")