import os
from pathlib import Path
from fastapi import Query, Request, Response, HTTPException, FastAPI
from fastapi.responses import StreamingResponse
from typing import List, Optional
import logging
import mimetypes

from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

VIDEO_PATH = "./static/videos"


app = FastAPI()
app.mount("/web", StaticFiles(directory="web/dist", html=True), name="web")

logger = logging.getLogger("uvicorn")



def get_mime_type(filename):
    mimetype, _ = mimetypes.guess_type(filename)
    return mimetype


def get_video_range(range_header: Optional[str], file_size: int):
    if not range_header:
        return 0, file_size - 1

    try:
        start, end = range_header.replace("bytes=", "").split("-")
        start = int(start) if start.strip() else 0
        end = int(end) if end.strip() else file_size - 1
    except ValueError:
        raise HTTPException(status_code=416, detail="Range Not Satisfiable")

    if start < 0 or end > file_size - 1:
        raise HTTPException(status_code=416, detail="Range Not Satisfiable")

    end = min(end, file_size - 1)
    content_length = end - start + 1
    return start, end, content_length

def stream_video_content_range(path, start, end):
    with open(path, 'rb') as file:
        file.seek(start)
        bytes_remaining = end - start + 1
        while bytes_remaining > 0:
            chunk = file.read(min(1024 * 8, bytes_remaining))
            if not chunk:
                break
            yield chunk
            bytes_remaining -= len(chunk)



@app.get("/")
def main():
    return {"message": "Hello FastAPI"}



@app.get("/video")
async def video_stream(request: Request, video_name: str = Query(...)):
    video =  VIDEO_PATH + "/" + video_name
    file_size = os.path.getsize(video)
    range_header = request.headers.get("Range")
    try:
        start, end, content_length = get_video_range(range_header, file_size)
    except HTTPException as e:
        return Response(status_code=e.status_code, headers={"Content-Type": "text/plain"}, content=e.detail)

    headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(content_length),
        "Content-Type": "video/mp4",
    }

    return StreamingResponse(
        stream_video_content_range(video, start, end),
        status_code=206,
        headers=headers,
    )



@app.get("/fileList")
async def read_files() -> List[str]:
    
    # 指定您想要列出文件夹的目录路径
    directory_path = Path(VIDEO_PATH)
    # 检查路径是否存在
    if not directory_path.exists():
        raise HTTPException(status_code=404, detail="Path not found")
    
    # 检查路径是否为目录
    if not directory_path.is_dir():
        raise HTTPException(status_code=400, detail="Path is not a directory")
    
    # 获取指定目录下的所有文件夹
    files_and_dirs = [entry.name for entry in directory_path.iterdir() if entry.is_file()]
    
    return files_and_dirs



# uvicorn main:app --reload --host "0.0.0.0" --port 38000