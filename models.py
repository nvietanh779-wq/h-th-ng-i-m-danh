from structures import LinkedList

class ClassInfo:
    def __init__(self, class_id, class_name, day_of_week, period, room):
        self.class_id = class_id
        self.class_name = class_name
        self.day_of_week = day_of_week
        self.period = period 
        self.room = room
        self.student_ids = LinkedList()

class Student:
    def __init__(self, student_id, name, major):
        self.student_id = student_id
        self.name = name
        self.major = major

class AttendanceRecord:
    def __init__(self, date, class_id, student_id, status):
        self.date = date
        self.class_id = class_id
        self.student_id = student_id
        self.status = int(status)

class AttendanceReport: 
    def __init__(self, student_id, major, name, class_id, total_sessions, absent_count):
        self.student_id = student_id
        self.major = major
        self.name = name
        self.class_id = class_id
        self.total_sessions = total_sessions
        self.absent_count = absent_count
        # Sửa lỗi chính tả total_sessions ở đây
        self.rate = (absent_count * 100) / total_sessions if total_sessions > 0 else 0.0