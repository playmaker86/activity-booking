"""
添加微信用户信息字段的数据库迁移脚本
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlalchemy import text
from app.core.db import engine


def upgrade():
    """升级数据库"""
    print("开始添加微信用户信息字段...")
    
    with engine.connect() as conn:
        try:
            # 添加新字段
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS unionid VARCHAR(100),
                ADD COLUMN IF NOT EXISTS gender INTEGER DEFAULT 0,
                ADD COLUMN IF NOT EXISTS country VARCHAR(50),
                ADD COLUMN IF NOT EXISTS province VARCHAR(50),
                ADD COLUMN IF NOT EXISTS city VARCHAR(50),
                ADD COLUMN IF NOT EXISTS language VARCHAR(20),
                ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE
            """))
            
            # 添加索引
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_users_unionid ON users(unionid)
            """))
            
            conn.commit()
            print("✅ 微信用户信息字段添加成功")
            
        except Exception as e:
            conn.rollback()
            print(f"❌ 添加字段失败: {e}")
            raise


def downgrade():
    """降级数据库"""
    print("开始移除微信用户信息字段...")
    
    with engine.connect() as conn:
        try:
            # 移除字段
            conn.execute(text("""
                ALTER TABLE users 
                DROP COLUMN IF EXISTS unionid,
                DROP COLUMN IF EXISTS gender,
                DROP COLUMN IF EXISTS country,
                DROP COLUMN IF EXISTS province,
                DROP COLUMN IF EXISTS city,
                DROP COLUMN IF EXISTS language,
                DROP COLUMN IF EXISTS is_active
            """))
            
            conn.commit()
            print("✅ 微信用户信息字段移除成功")
            
        except Exception as e:
            conn.rollback()
            print(f"❌ 移除字段失败: {e}")
            raise


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python add_wechat_fields.py [upgrade|downgrade]")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "upgrade":
        upgrade()
    elif action == "downgrade":
        downgrade()
    else:
        print("无效的操作，请使用 upgrade 或 downgrade")
        sys.exit(1)
