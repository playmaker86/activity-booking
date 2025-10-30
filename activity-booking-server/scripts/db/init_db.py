"""
初始化数据库脚本
创建一些示例数据
"""
from datetime import datetime, timedelta

from app.core.db import SessionLocal, engine, Base
from app.models.activity import Activity

# 创建所有表
Base.metadata.create_all(bind=engine)

def init_sample_data():
    """初始化示例数据"""
    db = SessionLocal()
    
    try:
        # 检查是否已有数据
        count = db.query(Activity).count()
        if count > 0:
            print("数据库已有数据，跳过初始化")
            return
        
        # 创建示例活动
        activities = [
            Activity(
                title="周末徒步活动",
                description="一起去爬山，享受大自然的美好。活动包含专业领队带领，提供午餐和保险。",
                cover_image="/static/images/placeholder.jpg",
                location="香山公园",
                organizer="户外运动协会",
                start_time=datetime.now() + timedelta(days=7),
                end_time=datetime.now() + timedelta(days=7, hours=6),
                price=50.0,
                max_participants=30,
                booked_count=0,
                is_active=True
            ),
            Activity(
                title="编程技术分享会",
                description="本期主题：Python Web开发最佳实践。适合有一定编程基础的开发者参加。",
                cover_image="/static/images/placeholder.jpg",
                location="科技园会议室A",
                organizer="技术交流社",
                start_time=datetime.now() + timedelta(days=3),
                end_time=datetime.now() + timedelta(days=3, hours=3),
                price=0.0,
                max_participants=50,
                booked_count=15,
                is_active=True
            ),
            Activity(
                title="瑜伽体验课",
                description="适合初学者的瑜伽体验课程，专业教练指导，提供瑜伽垫。",
                cover_image="/static/images/placeholder.jpg",
                location="健身中心三楼",
                organizer="健康生活馆",
                start_time=datetime.now() + timedelta(days=2),
                end_time=datetime.now() + timedelta(days=2, hours=2),
                price=30.0,
                max_participants=20,
                booked_count=8,
                is_active=True
            ),
            Activity(
                title="摄影外拍活动",
                description="一起去拍摄秋天的美景，会有专业摄影师指导构图和拍摄技巧。",
                cover_image="/static/images/placeholder.jpg",
                location="植物园",
                organizer="摄影爱好者协会",
                start_time=datetime.now() + timedelta(days=5),
                end_time=datetime.now() + timedelta(days=5, hours=4),
                price=80.0,
                max_participants=15,
                booked_count=10,
                is_active=True
            ),
            Activity(
                title="读书分享会",
                description="本期分享书籍：《人类简史》。欢迎爱读书的朋友一起交流探讨。",
                cover_image="/static/images/placeholder.jpg",
                location="咖啡书屋",
                organizer="读书会",
                start_time=datetime.now() + timedelta(days=1),
                end_time=datetime.now() + timedelta(days=1, hours=2),
                price=0.0,
                max_participants=25,
                booked_count=12,
                is_active=True
            )
        ]
        
        db.add_all(activities)
        db.commit()
        print(f"成功创建 {len(activities)} 个示例活动")
        
    except Exception as e:
        print(f"初始化数据失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("开始初始化数据库...")
    init_sample_data()
    print("数据库初始化完成！")

