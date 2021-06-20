from datetime import datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    user_id: int

    class Config:
        orm_mode = True


class QuizSchema(BaseModel):
    id: int
    title: str
    description: str
    is_free: bool
    price: float
    created_at: datetime

    class Config:
        orm_mode = True


class RelationSchema(BaseModel):
    quiz: QuizSchema
    user: UserSchema
