"""
Alembic 迁移示例

这个文件展示了如何创建不同类型的数据库迁移。
注意：这是一个示例文件，实际使用时请删除此文件。
"""

# 示例 1: 添加新字段
def example_add_column():
    """
    添加新字段的迁移示例
    假设我们要为用户表添加头像字段
    """
    from alembic import op
    import sqlalchemy as sa
    
    # 添加列
    op.add_column('users', sa.Column('avatar', sa.String(500), nullable=True))
    
    # 添加索引（可选）
    op.create_index('ix_users_avatar', 'users', ['avatar'])
    
    # 回滚操作
    # op.drop_index('ix_users_avatar', table_name='users')
    # op.drop_column('users', 'avatar')


# 示例 2: 修改字段类型
def example_change_column_type():
    """
    修改字段类型的迁移示例
    假设我们要将价格字段从 Float 改为 Integer（以分为单位）
    """
    from alembic import op
    import sqlalchemy as sa
    
    # 添加新列
    op.add_column('activities', sa.Column('price_cents', sa.Integer(), nullable=True))
    
    # 数据迁移：将价格从元转换为分
    connection = op.get_bind()
    connection.execute(
        "UPDATE activities SET price_cents = ROUND(price * 100) WHERE price IS NOT NULL"
    )
    
    # 删除旧列
    op.drop_column('activities', 'price')
    
    # 重命名新列
    op.alter_column('activities', 'price_cents', new_column_name='price')
    
    # 回滚操作
    # op.alter_column('activities', 'price', new_column_name='price_cents')
    # op.add_column('activities', sa.Column('price', sa.Float(), nullable=True))
    # connection = op.get_bind()
    # connection.execute("UPDATE activities SET price = price_cents / 100.0")
    # op.drop_column('activities', 'price_cents')


# 示例 3: 创建表
def example_create_table():
    """
    创建新表的迁移示例
    假设我们要创建一个活动分类表
    """
    from alembic import op
    import sqlalchemy as sa
    
    # 创建表
    op.create_table(
        'activity_categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建索引
    op.create_index('ix_activity_categories_name', 'activity_categories', ['name'])
    
    # 插入初始数据
    connection = op.get_bind()
    connection.execute(
        sa.text("""
            INSERT INTO activity_categories (name, description, created_at) VALUES
            ('户外运动', '爬山、徒步、骑行等户外活动', NOW()),
            ('文化娱乐', '读书会、音乐会、展览等文化活动', NOW()),
            ('教育培训', '技能培训、讲座、工作坊等', NOW()),
            ('社交聚会', '聚餐、聚会、联谊等社交活动', NOW())
        """)
    )
    
    # 回滚操作
    # op.drop_index('ix_activity_categories_name', table_name='activity_categories')
    # op.drop_table('activity_categories')


# 示例 4: 创建外键关系
def example_add_foreign_key():
    """
    添加外键关系的迁移示例
    假设我们要为活动表添加分类外键
    """
    from alembic import op
    import sqlalchemy as sa
    
    # 添加外键列
    op.add_column('activities', sa.Column('category_id', sa.Integer(), nullable=True))
    
    # 创建外键约束
    op.create_foreign_key(
        'fk_activities_category_id',
        'activities', 'activity_categories',
        ['category_id'], ['id']
    )
    
    # 创建索引
    op.create_index('ix_activities_category_id', 'activities', ['category_id'])
    
    # 回滚操作
    # op.drop_index('ix_activities_category_id', table_name='activities')
    # op.drop_constraint('fk_activities_category_id', 'activities', type_='foreignkey')
    # op.drop_column('activities', 'category_id')


# 示例 5: 数据清理迁移
def example_data_cleanup():
    """
    数据清理的迁移示例
    假设我们要清理无效的预约记录
    """
    from alembic import op
    import sqlalchemy as sa
    
    connection = op.get_bind()
    
    # 删除过期的预约记录（超过30天且未确认）
    connection.execute(
        sa.text("""
            DELETE FROM bookings 
            WHERE status = 'pending' 
            AND created_at < NOW() - INTERVAL '30 days'
        """)
    )
    
    # 更新用户昵称，移除特殊字符
    connection.execute(
        sa.text("""
            UPDATE users 
            SET nickname = REGEXP_REPLACE(nickname, '[^a-zA-Z0-9\u4e00-\u9fa5]', '', 'g')
            WHERE nickname IS NOT NULL
        """)
    )
    
    # 回滚操作：数据清理通常不可逆
    # 如果需要回滚，应该事先备份数据


# 示例 6: 批量数据迁移
def example_batch_data_migration():
    """
    批量数据迁移示例
    假设我们要为所有用户生成默认头像
    """
    from alembic import op
    import sqlalchemy as sa
    
    connection = op.get_bind()
    
    # 分批处理用户数据
    batch_size = 100
    offset = 0
    
    while True:
        # 获取一批用户
        result = connection.execute(
            sa.text(f"""
                SELECT id FROM users 
                WHERE avatar IS NULL 
                LIMIT {batch_size} OFFSET {offset}
            """)
        )
        
        users = result.fetchall()
        if not users:
            break
        
        # 为这批用户生成默认头像
        for user in users:
            user_id = user[0]
            default_avatar = f"https://api.dicebear.com/7.x/avataaars/svg?seed={user_id}"
            
            connection.execute(
                sa.text("UPDATE users SET avatar = :avatar WHERE id = :id"),
                {"avatar": default_avatar, "id": user_id}
            )
        
        offset += batch_size
        print(f"Processed {offset} users...")


# 完整的迁移文件示例
"""
这是一个完整的 Alembic 迁移文件示例：

'''add user avatar field

Revision ID: abc123def456
Revises: xyz789uvw012
Create Date: 2024-01-15 10:30:00.000000

'''
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'abc123def456'
down_revision: Union[str, None] = 'xyz789uvw012'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 添加头像字段
    op.add_column('users', sa.Column('avatar', sa.String(500), nullable=True))
    
    # 添加索引
    op.create_index('ix_users_avatar', 'users', ['avatar'])
    
    # 数据迁移：为现有用户设置默认头像
    connection = op.get_bind()
    connection.execute(
        sa.text("""
            UPDATE users 
            SET avatar = 'https://api.dicebear.com/7.x/avataaars/svg?seed=' || id
            WHERE avatar IS NULL
        """)
    )


def downgrade() -> None:
    # 删除索引
    op.drop_index('ix_users_avatar', table_name='users')
    
    # 删除字段
    op.drop_column('users', 'avatar')
"""
