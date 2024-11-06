from fastapi import FastAPI, Request
from llm_practice import get_response
from llm_practice import get_feedback
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse, description="메인 경로")
async def home(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/chatbot")
async def get_chatbot(query):
    response = get_response(query)
    feedback = get_feedback(query, response)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
