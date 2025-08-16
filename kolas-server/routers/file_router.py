from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse

from base import ResponseModel, id_utils, BaseFormatModel
from base.pagination import PageQuery, PageResult, paginate
from db import Session, get_session, File as SysFile
from pathlib import Path
import shutil
from pydantic import BaseModel
from sqlalchemy import select, desc
from datetime import datetime
import os
from typing import List, Optional

# 文件上传
router = APIRouter()

MAX_FILE_SIZE = 5 * 1024 * 1024 # 5MB
FILE_UPLOAD_DIR = "files"

class UploadResult(BaseModel):
   id: int
   filename: str

class FilePageQuery(PageQuery):
   project_id: int
   file_original_name: Optional[str] = None

class FileInfo(BaseFormatModel):
   id: int
   project_id: int
   file_name: str
   file_original_name: str
   file_size: int
   file_ext: str
   type: str
   create_time: datetime

def get_file_by_id(id: int, session: Session) -> File:
   return session.query(SysFile).get(id)

# 文件上传
@router.post("/upload", response_model=ResponseModel[UploadResult])
async def upload(file: UploadFile = File(...),
                 project_id: int = Form(None, description="项目ID"),
                 type: str = Form(..., description="类型（icon/图标 attachment/附件）"),
                 session: Session = Depends(get_session)):
   filename = file.filename
   file_size = file.size

   # 检查文件大小
   if file_size > MAX_FILE_SIZE:
      return ResponseModel.error(f"文件大小超出限制({MAX_FILE_SIZE / 1024 / 1024}MB)")

   # 保存文件
   file_ext = Path(filename).suffix
   filename_new = f"{id_utils.get_uuid()}{file_ext}"
   upload_dir = Path(FILE_UPLOAD_DIR)
   upload_dir.mkdir(exist_ok=True)

   file_path = upload_dir / filename_new
   with file_path.open("wb") as buffer:
      shutil.copyfileobj(file.file, buffer)

   # 保存数据库
   sys_file = SysFile(
      project_id=project_id,
      file_name=filename_new,
      file_original_name=filename,
      file_size=file_size,
      file_ext=file_ext,
      type=type
   )
   session.add(sys_file)
   session.commit()

   return ResponseModel.ok(UploadResult(
      id=sys_file.id,
      filename=sys_file.file_name
   ))

# 文件下载
@router.get("/download/{id}")
async def download(id: int, session: Session = Depends(get_session)):
   file = get_file_by_id(id, session)
   if not file:
      return ResponseModel.error("文件不存在")

   file_path = f"{FILE_UPLOAD_DIR}/{file.file_name}"
   if not os.path.exists(file_path):
      return ResponseModel.error("文件不存在")

   return FileResponse(
      path=file_path,
      filename=file.file_original_name,  # 设置下载时的文件名
      media_type="application/octet-stream"  # 通用二进制流类型
   )

# 图片预览
@router.get("/image/preview/{image_name}", response_class=FileResponse)
async def preview_image(image_name: str):
   # 构建完整的图片路径
   full_path = os.path.join(FILE_UPLOAD_DIR, image_name)

   # 检查文件是否存在
   if not os.path.exists(full_path):
      raise HTTPException(status_code=404, detail="图片文件不存在")

   # 检查是否是文件
   if not os.path.isfile(full_path):
      raise HTTPException(status_code=400, detail="路径不是有效的文件")

   # 获取文件扩展名以确定MIME类型
   _, ext = os.path.splitext(full_path)
   ext = ext.lower()

   # 常见图片MIME类型映射
   mime_types = {
      '.jpg': 'image/jpeg',
      '.jpeg': 'image/jpeg',
      '.png': 'image/png',
      '.gif': 'image/gif',
      '.bmp': 'image/bmp',
      '.svg': 'image/svg+xml',
      '.webp': 'image/webp'
   }

   # 获取对应的MIME类型，如果没有则使用默认
   media_type = mime_types.get(ext, 'application/octet-stream')

   # 构建响应头，明确指定inline表示在浏览器中显示
   headers = {
      "Content-Disposition": f"inline; filename=\"{image_name}\""
   }

   # 返回图片文件，浏览器会自动预览
   return FileResponse(
      path=full_path,
      media_type=media_type,
      headers=headers
   )


# 文件分页列表
@router.get("/list", response_model=ResponseModel[PageResult])
async def lists(query: FilePageQuery = Depends(), session: Session = Depends(get_session)):
   project_id = query.project_id
   file_original_name = query.file_original_name

   stmt = select(SysFile).filter(
      SysFile.project_id == project_id,
      SysFile.del_flag == 0
   ).order_by(desc(SysFile.id))
   if file_original_name:
      stmt = stmt.filter(SysFile.file_original_name.like(f"%{file_original_name}%"))

   page_result = paginate(session, stmt, page_no=query.page_no, page_size=query.page_size)

   pydantic_records = []
   for record in page_result.records:
      file_info = FileInfo.model_validate(record.__dict__)
      pydantic_records.append(file_info)
   page_result.records = pydantic_records
   return ResponseModel.ok(page_result)

# 文件查询
@router.get("/get/{id}", response_model=ResponseModel[FileInfo])
async def get(id: int, session: Session = Depends(get_session)):
   file = get_file_by_id(id, session)
   if not file:
      return ResponseModel.error("文件不存在")
   return ResponseModel.ok(FileInfo.model_validate(file.__dict__))


# 文件批量删除
@router.post("/delete", response_model=ResponseModel)
async def delete(ids: List[int], session: Session = Depends(get_session)):
   files = session.query(SysFile).filter(
      SysFile.id.in_(ids),
      SysFile.del_flag == 0
   ).all()
   effect = 0
   if files:
      for file in files:
         file.del_flag = 1
         effect += 1
      session.commit()
   return ResponseModel.ok(effect)
