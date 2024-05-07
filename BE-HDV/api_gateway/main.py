import json

from fastapi import FastAPI, File, UploadFile, Form, Body
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uvicorn
from aiohttp import ClientSession, FormData


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # cho phep tat ca cac nguon goc
    allow_credentials=True,
    allow_methods=[""],  # cho phep tat ca cac phuong thuc GET, POST, PUT
    allow_headers=["*"]  # Cho phep tat ca cac header
)


@app.get("/api/{path:path}")
async def forward_get_requests(path: str):
    async with httpx.AsyncClient() as client:
        if path.startswith("googlemeet/get_participants"):
            response = await client.get(f"http://localhost:5000/api/{path}")
        else:
            response = await client.get(f"http://localhost:8002/api/{path}")
    return response.json()

@app.post("/api/{path:path}")
async def forward_post_requests(path: str, file: UploadFile = File(None), data = Form({})):
    #data: list = Body(None), file_name: str = None

    async with ClientSession() as session:
        if path.startswith("application/to_json"):
            form_data = FormData()
            if file is None:
                return {"error": "File upload failed"}

            file_contents = await file.read()

            form_data.add_field("file", file_contents, filename=file.filename, content_type=file.content_type)
            response = await session.post(f"http://localhost:8002/api/{path}", data=form_data)
            return await response.json()
        elif path.startswith("convert/excel_to_json"):
            form_data = FormData()
            if file is None:
                return {"error": "File upload failed"}

            file_contents = await file.read()

            form_data.add_field("file", file_contents, filename=file.filename, content_type=file.content_type)
            response = await session.post(f"http://localhost:8001/api/{path}", data=form_data)
            return await response.json()
        elif path.startswith("application/create_meet"):
            response = await session.post(f"http://localhost:8002/api/{path}", data=None)
            return await response.json()
        elif path.startswith("googlemeet/create_meet"):
            response = await session.post(f"http://localhost:5000/api/{path}", data=None)
            return await response.json()
        elif path.startswith("convert/json_to_excel"):
            data_json = json.loads(data)
            data = {
                "data": data_json["data"],
                "file_name": data_json["file_name"]
            }
            response = await session.post(f"http://localhost:8001/api/{path}?file_name={data_json['file_name']}", data=data_json["data"])

            return response

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8888)