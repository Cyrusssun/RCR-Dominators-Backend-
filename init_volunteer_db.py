#!/usr/bin/env python
# init_volunteer_db.py - Initialize volunteer database

from __init__ import app, db
from model.volunteer import VolunteerShift, VolunteerAssignment, VolunteerJob

def init_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Volunteer tables created")
        
        # Add job types
        jobs = ['Conductor', 'Ticket Taker', 'Safety Officer', 'Engineer', 'Fireman', 'Brake Operator']
        for job_name in jobs:
            existing = VolunteerJob.query.filter_by(job_name=job_name).first()
            if not existing:
                job = VolunteerJob(job_name=job_name)
                db.session.add(job)
        
        db.session.commit()
        print(f"✅ Added {len(jobs)} job types")
        
        # Generate shifts based on schedule
        RR_SCHEDULE = {
            '2026-03-07': 'steam', '2026-03-14': 'steam', '2026-03-15': 'cable',
            '2026-03-21': 'steam', '2026-03-22': 'speeder', '2026-03-28': 'steam',
            '2026-03-29': 'cable', '2026-04-04': 'steam', '2026-04-05': 'cable',
            '2026-04-11': 'steam', '2026-04-12': 'none', '2026-04-18': 'steam',
            '2026-04-19': 'cable', '2026-04-25': 'steam', '2026-04-26': 'speeder',
            '2026-05-02': 'steam', '2026-05-03': 'cable', '2026-05-09': 'steam',
            '2026-05-10': 'none', '2026-05-16': 'steam', '2026-05-17': 'cable',
            '2026-05-23': 'steam', '2026-05-24': 'speeder', '2026-05-30': 'steam',
            '2026-05-31': 'cable',
        }
        
        time_ranges = {
            'steam': ('10:00', '14:00'),
            'cable': ('11:00', '14:00'),
            'speeder': ('11:00', '14:00')
        }
        
        added_count = 0
        for date_key, train_type in RR_SCHEDULE.items():
            if train_type == 'none':
                continue
            
            start, end = time_ranges[train_type]
            
            # Check if shift already exists
            existing = VolunteerShift.query.filter_by(date=date_key, train_type=train_type).first()
            if not existing:
                shift = VolunteerShift(
                    date=date_key,
                    time_start=start,
                    time_end=end,
                    train_type=train_type,
                    max_volunteers=4
                )
                db.session.add(shift)
                added_count += 1
        
        db.session.commit()
        print(f"✅ Added {added_count} shifts")
        
        # Show summary
        shifts = VolunteerShift.query.all()
        print(f"\n📊 Total shifts in database: {len(shifts)}")
        for s in shifts[:10]:
            print(f"  {s.date}: {s.train_type} ({s.time_start}-{s.time_end})")
        
        return True

if __name__ == '__main__':
    init_database()
    print("\n🎉 Volunteer database initialized successfully!")
