from pydantic import BaseModel, ConfigDict


def to_camel(string: str) -> str:
    """将蛇形命名转换为驼峰命名"""
    components = string.split('_')
    return components[0] + ''.join(x.capitalize() for x in components[1:])


class CamelCaseModel(BaseModel):
    """
    驼峰命名基类
    自动将蛇形命名的字段转换为驼峰命名返回给前端
    """
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,  # 允许使用原始字段名或别名
        from_attributes=True,   # 允许从 ORM 模型创建
    )
