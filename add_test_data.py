#!/usr/bin/env python
# add_test_data.py - Add test reservations to database

from __init__ import app, db
from model.reservation import Reservation

def add_test_reservations():
    with app.app_context():
        print("Adding test reservations...")
        
        test_data = [
            {
                'date': '2026-04-18',
                'time': '10:30',
                'train_type': 'Steam Locomotive',
                'first_name': 'John',
                'last_name': 'Smith',
                'email': 'john.smith@example.com',
                'phone': '858-555-0101',
                'adults': 2,
                'children': 1,
                'infants': 0
            },
            {
                'date': '2026-04-18',
                'time': '13:15',
                'train_type': 'Steam Locomotive',
                'first_name': 'Maria',
                'last_name': 'Garcia',
                'email': 'maria.garcia@example.com',
                'phone': '858-555-0102',
                'adults': 1,
                'children': 2,
                'infants': 1
            },
            {
                'date': '2026-04-19',
                'time': '11:20',
                'train_type': 'Cable Car',
                'first_name': 'David',
                'last_name': 'Kim',
                'email': 'david.kim@example.com',
                'phone': '858-555-0103',
                'adults': 4,
                'children': 0,
                'infants': 0
            },
            {
                'date': '2026-04-19',
                'time': '13:45',
                'train_type': 'Cable Car',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'email': 'sarah.johnson@example.com',
                'phone': '858-555-0104',
                'adults': 2,
                'children': 3,
                'infants': 0
            },
            {
                'date': '2026-04-20',
                'time': '10:00',
                'train_type': 'Steam Locomotive',
                'first_name': 'Robert',
                'last_name': 'Brown',
                'email': 'robert.brown@example.com',
                'phone': '858-555-0105',
                'adults': 2,
                'children': 2,
                'infants': 0
            }
        ]
        
        added = 0
        for data in test_data:
            # Check if already exists
            existing = Reservation.query.filter_by(
                date=data['date'],
                time=data['time'],
                email=data['email']
            ).first()
            
            if not existing:
                reservation = Reservation(**data)
                result = reservation.create()
                if result:
                    added += 1
                    print(f"✅ Added: {result.confirm_code} - {data['first_name']} {data['last_name']} - {data['date']} {data['time']}")
            else:
                print(f"⏭️  Skipped: {data['first_name']} {data['last_name']} - already exists")
        
        print(f"\n📊 Added {added} new reservations")
        
        # Verify
        total = Reservation.query.count()
        print(f"Total reservations now: {total}")

if __name__ == '__main__':
    add_test_reservations()
