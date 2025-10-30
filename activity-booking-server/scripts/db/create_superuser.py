"""
创建超级用户脚本
用于创建管理员账户
"""
from app.core.db import SessionLocal
from app.models.user import User


def create_superuser():
    """创建超级用户"""
    db = SessionLocal()
    
    try:
        # 检查是否已存在超级用户
        existing_user = db.query(User).filter(User.openid == "admin").first()
        if existing_user:
            print("超级用户已存在")
            return
        
        # 创建超级用户
        admin_user = User(
            openid="admin",
            nickname="系统管理员",
            phone="13800000000"
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print(f"成功创建超级用户: {admin_user.nickname} (ID: {admin_user.id})")
        
    except Exception as e:
        print(f"创建超级用户失败: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("创建超级用户...")
    create_superuser()
    print("完成！")
