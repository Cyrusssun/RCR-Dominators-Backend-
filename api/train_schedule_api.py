# api/train_schedule_api.py
from flask import Blueprint, jsonify, request
from datetime import datetime
import random

# Create blueprint for train schedule routes
train_schedule_bp = Blueprint('train_schedule', __name__, url_prefix='/api')

# Operating days configuration (Saturday and Sunday)
OPERATING_DAYS = {5, 6}  # Saturday=5, Sunday=6

# Train schedules for different train types
TRAIN_SCHEDULES = {
    "Steam Locomotive": ["10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00"],
    "Cable Car": ["10:00", "10:45", "11:30", "12:15", "13:00", "13:45", "14:30", "15:15"],
    "Speeder": ["10:00", "10:20", "10:40", "11:00", "11:20", "11:40", "12:00", "12:20", "12:40", "13:00", "13:20", "13:40", "14:00", "14:20", "14:40", "15:00"]
}

# Capacity for each train type
CAPACITIES = {
    "Steam Locomotive": 60,
    "Cable Car": 40,
    "Speeder": 20
}

def get_train_type_for_date(check_date):
    """Determine which train type runs on a given date"""
    weekday = check_date.weekday()
    
    # Saturday: Steam Locomotive
    if weekday == 5:
        return "Steam Locomotive"
    
    # Sunday: alternate between Cable Car and Speeder based on week of month
    week_of_month = (check_date.day - 1) // 7
    if week_of_month % 2 == 0:
        return "Cable Car"
    else:
        return "Speeder"

def generate_booking_for_ride(time_str, capacity, date_obj):
    """Generate realistic booking data for each ride"""
    # Use date and time as random seed for consistent data
    random.seed(f"{date_obj}_{time_str}")
    
    hour = int(time_str.split(':')[0])
    
    # Morning rides have fewer bookings, afternoon rides are more popular
    if hour < 12:
        booked = random.randint(10, 35)
    else:
        booked = random.randint(30, capacity)
    
    # Ensure booked does not exceed capacity
    booked = min(booked, capacity)
    available = capacity - booked
    
    # Determine status (matches frontend expectations)
    if available == 0:
        status = "full"
    elif available < 10:
        status = "boarding"
    else:
        status = "ontime"
    
    return {
        "available": available,
        "booked": booked,
        "status": status
    }

@train_schedule_bp.route('/schedule', methods=['GET'])
def get_train_schedule():
    """Get train schedule for a specific date"""
    date_str = request.args.get('date')
    
    if not date_str:
        return jsonify({"error": "Missing date parameter. Use ?date=YYYY-MM-DD"}), 400
    
    try:
        query_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    
    # Check if operating on this date (weekends only)
    is_operating = query_date.weekday() in OPERATING_DAYS
    
    if not is_operating:
        return jsonify({
            "date": date_str,
            "operating": False,
            "train_type": None,
            "rides": []
        })
    
    # Get train type for this date
    train_type = get_train_type_for_date(query_date)
    schedules = TRAIN_SCHEDULES[train_type]
    capacity = CAPACITIES[train_type]
    
    # Generate all rides
    rides = []
    for time_str in schedules:
        booking = generate_booking_for_ride(time_str, capacity, query_date)
        rides.append({
            "time": time_str,
            "available": booking["available"],
            "booked": booking["booked"],
            "capacity": capacity,
            "status": booking["status"],
            "train_type": train_type
        })
    
    return jsonify({
        "date": date_str,
        "operating": True,
        "train_type": train_type,
        "rides": rides
    })

@train_schedule_bp.route('/schedule/today', methods=['GET'])
def get_today_schedule():
    """Get train schedule for today"""
    today = datetime.now().date()
    today_str = today.strftime('%Y-%m-%d')
    # Call the main schedule function
    from flask import current_app
    with current_app.test_request_context(f'/api/schedule?date={today_str}'):
        return get_train_schedule()