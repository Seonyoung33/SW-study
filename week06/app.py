from fastapi import FastAPI, Request
from llm_practice import get_response
from llm_practice import get_feedback
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from ocr_practice import extraction_medicine
from pathlib import Path

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse, description="메인 경로")
async def home(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/feedback")
async def get_feedback_to_response(medicines, response):
    feedback = get_feedback(medicines, response)
    return feedback

@app.get("/analyzing_medicine")
async def get_medicine_analyzing(image_data):
    # image_path = Path("test.jpg")
    # if not image_path.is_file():
    #     return {"error": "이미지 파일이 존재하지 않습니다."}

    # # 이미지 파일을 바이너리 형식으로 읽기
    # with open(image_path, "rb") as image_file:
    #     image_data = image_file.read()

    founded_medicine = extraction_medicine(image_data=image_data) # 약품명 추출
    responses = get_response(founded_medicine)
    print("결과", responses)
    return responses

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
