from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_session
from app.models.post import Post
from app.models.tag import Tag
from app.schemas.post import PostCreate, PostRead
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=list[PostRead])
async def list_posts(
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(get_session)
):

   # paginaciOn
    # skip para saltar un numero x de registros 
    # limit PARA  devolver un numero x de registros
    result = await session.execute(
        select(Post)
        .where(Post.is_deleted == False)
        .order_by(Post.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

@router.post("/", response_model=PostRead)
async def create_post(
    post_in: PostCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    post = Post(
        title=post_in.title,
        content=post_in.content,
        owner_id=current_user.id,
    )

    if post_in.tags:
        tags = await session.execute(select(Tag).where(Tag.id.in_(post_in.tags)))
        post.tags = tags.scalars().all()

    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

@router.put("/{post_id}", response_model=PostRead)
async def update_post(
    post_id: int,
    post_in: PostCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post or post.is_deleted:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado para modificar este post")

    post.title = post_in.title
    post.content = post_in.content

    if post_in.tags:
        tags = await session.execute(select(Tag).where(Tag.id.in_(post_in.tags)))
        post.tags = tags.scalars().all()

    await session.commit()
    await session.refresh(post)
    return post

@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado para eliminar este post")

    post.is_deleted = True
    await session.commit()
    return {"message": f"Post {post.title} eliminado (soft delete)"}