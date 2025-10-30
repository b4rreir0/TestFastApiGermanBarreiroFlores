from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from app.mixins.timestamps import TimestampMixin
from app.mixins.soft_delete import SoftDeleteMixin
from app.models.post_tag import post_tag

class Tag(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)

    posts = relationship("Post", secondary=post_tag, back_populates="tags")
