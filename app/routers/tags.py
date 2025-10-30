from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_session
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagRead
from app.core.auth import get_current_user

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.get("/", response_model=list[TagRead])
async def list_tags(
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(get_session)
):
    # paginaciOn
    # skip para saltar un numero x de registros 
    # limit PARA  devolver un numero x de registros
    result = await session.execute(
        select(Tag)
        .where(Tag.is_deleted == False)
        .order_by(Tag.name.asc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

@router.post("/", response_model=TagRead)
async def create_tag(
    tag_in: TagCreate,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    existing = await session.execute(select(Tag).where(Tag.name == tag_in.name))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Tag ya existe")

    tag = Tag(name=tag_in.name)
    session.add(tag)
    await session.commit()
    await session.refresh(tag)
    return tag