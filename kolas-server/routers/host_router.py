from __future__ import annotations


from fastapi import APIRouter
from pydantic import BaseModel
from base import ResponseModel
from db import Session, get_session
from fastapi import Depends
from db import Host
from typing import List, Optional
from sqlalchemy import and_, desc, text
from host import SshClient
from base import object_utils, str_utils

# 主机管理

router = APIRouter()

class HostModel(BaseModel):
    id: int
    project_id: int
    name: str
    ip: str
    port: int
    username: str
    password: str
    status: str
    description: Optional[str] = None

class SetDefaultEnvForm(BaseModel):
    workspace_id: int
    env_id: int

class HostForm(BaseModel):
    id: Optional[int] = None
    project_id: int
    name: str
    ip: str
    port: int
    username: str
    password: str
    status: str
    description: Optional[str] = None

class HostTestConnectionForm(BaseModel):
    ip: str
    port: int
    username: str
    password: str

@router.get("/list/{project_id}", response_model=ResponseModel[List[HostModel]])
async def lists(project_id: int, session: Session = Depends(get_session)):
    host_list = (session.query(Host)
                .where(Host.project_id == project_id)
                .order_by(desc(Host.id))
                .all())

    return ResponseModel.ok(host_list)

@router.get("/get/{id}", response_model=ResponseModel)
async def get(id: int, session: Session = Depends(get_session)):
    host = session.query(Host).get(id)
    if not host:
        return ResponseModel.error("主机不存在")
    else:
        host_model = HostModel.model_validate(host.__dict__)
        host_model.password = str_utils.to_base64(host_model.password)
        return ResponseModel.ok(host_model)

@router.post("/save", response_model=ResponseModel)
async def add_host(form: HostForm, session: Session = Depends(get_session)):
    id = form.id
    if id is None:
        # 新增
        host = Host(
            project_id=form.project_id,
            name=form.name,
            ip=form.ip,
            port=form.port,
            username=form.username,
            password=form.password,
            status=form.status,
            description=form.description
        )
        session.add(host)
    else:
        host = session.query(Host).get(id)
        if not host:
            return ResponseModel.error("主机不存在")
        else:
            object_utils.copy_properties(form, host)

    session.commit()
    return ResponseModel.ok()

@router.post("/test_connection", response_model=ResponseModel)
async def test_connection(form: HostTestConnectionForm):
    ssh_client = SshClient(
        ip=form.ip,
        port=form.port,
        username=form.username,
        password=form.password
    )
    return ResponseModel.ok(ssh_client.test_ssh_connection())

@router.delete("/delete/{id}", response_model=ResponseModel)
async def delete(id: int, session: Session = Depends(get_session)):
    session.query(Host).where(
        Host.id == id,
    ).delete()

    session.commit()
    return ResponseModel.ok()

