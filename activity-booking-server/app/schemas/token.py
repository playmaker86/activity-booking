from app.schemas.base import CamelCaseModel


class Token(CamelCaseModel):
    """Token模型"""
    token: str
    token_type: str = "bearer"


class TokenData(CamelCaseModel):
    """Token数据模型"""
    user_id: int

