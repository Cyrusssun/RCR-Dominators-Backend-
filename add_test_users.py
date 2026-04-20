#!/usr/bin/env python
from __init__ import app, db
from model.railroad_user import RailroadUser

def add_test_users():
    with app.app_context():
        # 添加多个测试用户
        test_users = [
            {'name': 'Admin User', 'email': 'admin@example.com', 'password': 'admin123'},
            {'name': 'John Smith', 'email': 'john@example.com', 'password': 'john123'},
            {'name': 'Jane Doe', 'email': 'jane@example.com', 'password': 'jane123'},
            {'name': 'Bob Wilson', 'email': 'bob@example.com', 'password': 'bob123'},
            {'name': 'Alice Brown', 'email': 'alice@example.com', 'password': 'alice123'},
        ]
        
        added = 0
        for u in test_users:
            existing = RailroadUser.query.filter_by(email=u['email']).first()
            if not existing:
                user = RailroadUser(name=u['name'], email=u['email'], password=u['password'])
                result = user.create()
                if result:
                    print(f"✅ 添加用户: {u['email']} / {u['password']}")
                    added += 1
                else:
                    print(f"❌ 添加失败: {u['email']}")
            else:
                print(f"⏭️ 用户已存在: {u['email']}")
        
        # 统计
        total = RailroadUser.query.count()
        print(f"\n📊 总用户数: {total}")
        print(f"✅ 新添加用户数: {added}")

if __name__ == '__main__':
    add_test_users()
