from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy import Select
from db import Session
from typing import Any, Sequence, Optional

DEFAULT_PAGE_NO = 1
DEFAULT_PAGE_SIZE = 10

# 分页查询对象
class PageQuery(BaseModel):
    page_no: Optional[int] = DEFAULT_PAGE_NO
    page_size: Optional[int] = DEFAULT_PAGE_SIZE

# 分页元数据
class Pagination(BaseModel):
    page_no: int
    page_size: int
    total: int

# 分页返回对象
class PageResult(BaseModel):
    records: Sequence[Any]
    pagination: Pagination

def paginate(session: Session,
             query: Select[Any],
             page_no: int = DEFAULT_PAGE_NO,
             page_size: int = DEFAULT_PAGE_SIZE) -> PageResult:

    limit, offset = compute_limit_and_offset(page_no, page_size)

    # 获取总记录数
    total = session.scalar(select(func.count()).select_from(query.subquery()))

    # 分页查询
    page_query = query.limit(limit).offset(offset)
    records = session.execute(page_query).scalars().all()
    # records = session.execute(page_query).all()

    return PageResult(
        records=records,
        pagination=Pagination(page_no=page_no, page_size=page_size, total=total)
    )

def compute_limit_and_offset(page_no: int, page_size: int) -> (int, int):
    if page_no < 1:
        page_no = DEFAULT_PAGE_NO
    if page_size < 1:
        page_size = DEFAULT_PAGE_SIZE

    # 计算偏移量
    offset = (page_no - 1) * page_size
    return page_size, offset


def paginate_query(query, page: int, page_size: int):
    """
    封装分页逻辑的方法
    :param query: 原始查询对象
    :param page: 页码
    :param page_size: 每页记录数
    :return: 分页后的查询结果、总记录数、总页数
    """
    # 计算总记录数
    if page < 1:
        page = DEFAULT_PAGE_NO
    if page_size < 1:
        page_size = DEFAULT_PAGE_SIZE

    total_count = query.count()
    # 计算总页数
    total_pages = (total_count + page_size - 1) // page_size
    # 计算偏移量
    offset = (page - 1) * page_size
    # 应用分页
    paginated_query = query.offset(offset).limit(page_size)
    # 执行查询
    results = paginated_query.all()
    return results, total_count, total_pages