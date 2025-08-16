from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter
from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import asc

from base import ResponseModel, BaseFormatModel
from base import object_utils
from db import Session, get_session, Project
from datetime import datetime

# 项目管理

router = APIRouter()

class ProjectModel(BaseFormatModel):
    id: int
    name: str
    description: Optional[str] = None
    status: int
    icon_name: str
    create_time: datetime

class ProjectForm(BaseModel):
    id: Optional[int] = None
    icon_name: str
    name: str
    description: Optional[str] = None

@router.get("/list", response_model=ResponseModel[List[ProjectModel]])
async def lists(session: Session = Depends(get_session)):
    project_list = (session.query(Project)
                .order_by(asc(Project.id))
                .all())

    return ResponseModel.ok(project_list)

@router.get("/get/{id}", response_model=ResponseModel)
async def get(id: int, session: Session = Depends(get_session)):
    project = session.query(Project).get(id)
    if not project:
        return ResponseModel.error("项目信息不存在")
    else:
        project_model = ProjectModel.model_validate(project.__dict__)
        return ResponseModel.ok(project_model)

@router.post("/save", response_model=ResponseModel)
async def save(form: ProjectForm, session: Session = Depends(get_session)):
    id = form.id
    if id is None:
        # 新增
        project = Project(
            name=form.name,
            icon_name=form.icon_name,
            status=1, # 默认启用
            description=form.description
        )
        session.add(project)
    else:
        project = session.query(Project).get(id)
        if not project:
            return ResponseModel.error("项目信息不存在")
        else:
            object_utils.copy_properties(form, project)

    session.commit()
    return ResponseModel.ok()

@router.delete("/delete/{id}", response_model=ResponseModel)
async def delete(id: int, session: Session = Depends(get_session)):
    session.query(Project).where(
        Project.id == id,
    ).delete()

    session.commit()
    return ResponseModel.ok()

