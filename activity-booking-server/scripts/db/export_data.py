"""
数据导出脚本
将数据库数据导出为 JSON 格式
"""
import json
from datetime import datetime

from app.database import SessionLocal
from app.models import User, Activity, Booking


def export_data():
    """导出所有数据为 JSON"""
    db = SessionLocal()
    
    try:
        # 导出用户数据
        users = db.query(User).all()
        users_data = []
        for user in users:
            users_data.append({
                "id": user.id,
                "openid": user.openid,
                "nickname": user.nickname,
                "phone": user.phone,
                "created_at": user.created_at.isoformat()
            })
        
        # 导出活动数据
        activities = db.query(Activity).all()
        activities_data = []
        for activity in activities:
            activities_data.append({
                "id": activity.id,
                "title": activity.title,
                "description": activity.description,
                "location": activity.location,
                "organizer": activity.organizer,
                "start_time": activity.start_time.isoformat(),
                "end_time": activity.end_time.isoformat(),
                "price": float(activity.price),
                "max_participants": activity.max_participants,
                "booked_count": activity.booked_count,
                "is_active": activity.is_active,
                "created_at": activity.created_at.isoformat()
            })
        
        # 导出预约数据
        bookings = db.query(Booking).all()
        bookings_data = []
        for booking in bookings:
            bookings_data.append({
                "id": booking.id,
                "user_id": booking.user_id,
                "activity_id": booking.activity_id,
                "name": booking.name,
                "phone": booking.phone,
                "participants": booking.participants,
                "status": booking.status.value,
                "created_at": booking.created_at.isoformat()
            })
        
        # 合并所有数据
        export_data = {
            "export_time": datetime.now().isoformat(),
            "users": users_data,
            "activities": activities_data,
            "bookings": bookings_data
        }
        
        # 保存到文件
        filename = f"export_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        print(f"数据已导出到: {filename}")
        print(f"- 用户: {len(users_data)} 条")
        print(f"- 活动: {len(activities_data)} 条")
        print(f"- 预约: {len(bookings_data)} 条")
        
    except Exception as e:
        print(f"导出数据失败: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    export_data()
