from typing import Optional
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, field_validator
from entities.roles import Roles


class TestUser(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str = Field(..., min_length=1, max_length=20, description="passwordRepeat должен вполностью совпадать с полем password")
    roles: List[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value

    class Config:
        use_enum_values = True
        json_encoders = {
            Roles: lambda v: v.value
        }
class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    verified: bool
    banned: Optional[bool] = Field(default=False, description="Статус бана пользователя")
    roles: List[Roles]
    createdAt: datetime = Field(description="Дата и время создания пользователя в формате ISO 8601")

class MovieResponse(BaseModel):

    id: int = Field(..., gt=0, description="идентификатор фильма")
    name: str = Field(..., min_length=1, max_length=255, description="Название фильма")
    price: float = Field(..., gt=0, description="Цена билета")
    description: str = Field(..., min_length=1, description="Описание фильма")
    imageUrl: Optional[str] = Field(None, description="URL изображения фильма")
    location: str = Field(..., pattern=r"^(MSK|SPB)$", description="Локация (MSK или SPB)")
    published: bool = Field(..., description="Опубликован ли фильм")
    genreId: int = Field(..., gt=0, description="ID жанра фильма")
    genre: dict = Field(..., description="Объект жанра с полем name")
    createdAt: datetime = Field(..., description="Дата создания в формате ISO 8601")
    rating: float = Field(..., ge=0, description="Рейтинг фильма (от 0 до 10)")


class MoviesListResponse(BaseModel):
    movies: List[MovieResponse] = Field(..., description="Список фильмов")
    count: int = Field(..., ge=0, description="Общее количество фильмов")
    page: int = Field(..., ge=0, description="Текущая страница")
    pageSize: int = Field(..., ge=0, description="Размер страницы")
    pageCount: int = Field(..., ge=0, description="Общее количество страниц")