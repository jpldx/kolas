from __future__ import annotations

from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field
from datetime import datetime

T = TypeVar('T', bound=object)
OK = 0
ERROR = -1

# 通用响应模型
class ResponseModel(BaseModel, Generic[T]):
    code: int = Field(..., description="响应码")
    msg: str = Field(..., description="响应信息")
    data: Optional[T] = Field(None, description="响应数据")

    @classmethod
    def ok(cls, data: Optional[T] = None, msg: str = "ok") -> ResponseModel[T]:
        return cls(code=OK, msg=msg, data=data)

    @classmethod
    def error(cls, msg: str = "error") -> ResponseModel:
        return cls(code=ERROR, msg=msg)

# 格式化的BaseModel
class FormatBaseModel(BaseModel):
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

if __name__ == '__main__':
    print(ResponseModel.ok(data={"key": "value"}, msg="okk"))
    print(ResponseModel.error(msg="oops~"))


