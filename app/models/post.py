from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.mixins.timestamps import TimestampMixin
from app.mixins.soft_delete import SoftDeleteMixin
from app.models.post_tag import post_tag

class Post(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User", back_populates="posts")
    tags = relationship("Tag", secondary=post_tag, back_populates="posts")
