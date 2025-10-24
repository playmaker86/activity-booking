from typing import TypeVar, Generic, Optional, List, Dict, Any, Type

from sqlalchemy import select, func
from sqlalchemy.orm import Session

T = TypeVar('T')

class BaseRepository(Generic[T]):
    """基础 Repository 类，提供通用的数据访问方法"""
    
    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db
    
    def get_by_id(self, id: int) -> Optional[T]:
        """根据 ID 获取单个记录"""
        query = select(self.model).where(self.model.id == id)
        return self.db.scalar(query)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """获取所有记录（分页）"""
        query = select(self.model).offset(skip).limit(limit)
        result = self.db.scalars(query).all()
        return list(result)
    
    def count(self) -> int:
        """获取记录总数"""
        query = select(func.count()).select_from(self.model)
        return self.db.scalar(query)
    
    def create(self, obj_in: Dict[str, Any]) -> T:
        """创建新记录"""
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update(self, db_obj: T, obj_in: Dict[str, Any]) -> T:
        """更新记录"""
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, id: int) -> bool:
        """删除记录"""
        query = select(self.model).where(self.model.id == id)
        obj = self.db.scalar(query)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False
    
    def filter_by(self, **kwargs) -> List[T]:
        """根据条件过滤记录"""
        query = select(self.model).filter_by(**kwargs)
        result = self.db.scalars(query).all()
        return list(result)
    
    def filter_by_first(self, **kwargs) -> Optional[T]:
        """根据条件获取第一个记录"""
        query = select(self.model).filter_by(**kwargs)
        return self.db.scalar(query)
