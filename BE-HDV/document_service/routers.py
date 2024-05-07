import io
import os

import uvicorn
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.params import File, Body
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from worker import public
from convert import Convert

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Địa chỉ nguồn gốc của trình duyệt
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Cho phép tất cả các header
)

port = 5000
convert = Convert()
@app.post('/api/convert/excel_to_json')
def excel_to_json(file: UploadFile = File(...) ):
    public("(document-service) Convert Excel to Json .....")
    return convert.excel_to_json(file)

@app.post('/api/convert/json_to_excel')
def json_to_excel(data: list = Body(...), file_name: str = None):
    public("(document-service) Convert Json to Excel ......")

    if file_name is None:
        file_name = "DanhSachDiemDanh.xlsx"

    file_bytes = convert.json_to_excel(data, file_name)
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Convert Failed")

    return FileResponse(file_name, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=file_name)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)



