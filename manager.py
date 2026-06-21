from structures import LinkedList
from models import Student, ClassInfo, AttendanceRecord, AttendanceReport

class AttendanceManager:
    def __init__(self): 
        self.classes = LinkedList()
        self.students = LinkedList()
        self.attendance_records = LinkedList()
        self.load_data()

    def load_data(self):
        # 1. Đọc danh sách lớp học
        try:
            with open("classes.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        line = line.split("|")
                        if len(line) >= 5:
                            c = ClassInfo(line[0].strip(), line[1].strip(), line[2].strip(), line[3].strip(), line[4].strip())
                            if len(line) == 6 and line[5].strip():
                                ids = line[5].strip().split(",")
                                for s_id in ids:
                                    if s_id.strip():
                                        c.student_ids.append(s_id.strip())
                            self.classes.append(c)
        except FileNotFoundError:
            pass

        # 2. Đọc danh sách sinh viên
        try:
            with open("students.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        line = line.split("|")
                        if len(line) == 3:  
                            self.students.append(Student(line[0].strip(), line[1].strip(), line[2].strip()))
        except FileNotFoundError:
            pass

        # 3. Đọc lịch sử điểm danh
        try:
            with open("attendance.txt", "r", encoding="utf-8") as f: 
                for line in f:
                    line = line.strip()
                    if line:
                        line = line.split("|") 
                        if len(line) == 4:  
                            self.attendance_records.append(AttendanceRecord(line[0].strip(), line[1].strip(), line[2].strip(), int(line[3].strip())))
        except FileNotFoundError:
            pass

    def save_data(self): 
        with open("classes.txt", "w", encoding="utf-8") as f:
            curr = self.classes.head
            while curr:
                c = curr.data
                c_ids = c.student_ids.head
                ids_list = []
                while c_ids:
                    ids_list.append(c_ids.data)
                    c_ids = c_ids.next
                id_str = ",".join(ids_list)
                f.write(f"{c.class_id} | {c.class_name} | {c.day_of_week} | {c.period} | {c.room} | {id_str}\n")
                curr = curr.next    
        
        with open("students.txt", "w", encoding="utf-8") as f:
            curr = self.students.head
            while curr:
                s = curr.data
                f.write(f"{s.student_id} | {s.name} | {s.major}\n")
                curr = curr.next
        
        with open("attendance.txt", "w", encoding="utf-8") as f:
            curr = self.attendance_records.head 
            while curr:
                a = curr.data
                f.write(f"{a.date} | {a.class_id} | {a.student_id} | {a.status}\n")
                curr = curr.next

    def add_student_to_system(self, student_id, name, major):
        curr = self.students.head
        found = False
        while curr:
            s = curr.data 
            if s.student_id == student_id:
                found = True
                break
            curr = curr.next 
        if not found:
            self.students.append(Student(student_id, name, major))
            self.save_data()
            return True
        return False

    def add_class(self, class_id, class_name, day_of_week, period, room):
        curr = self.classes.head
        while curr:
            c = curr.data
            if c.class_id == class_id:
                print(f" ❌ Lỗi: Mã môn học '{class_id}' đã tồn tại!") 
                return False
            curr = curr.next
        self.classes.append(ClassInfo(class_id, class_name, day_of_week, period, room))
        self.save_data()
        print(f"  Thành công: Đã tạo môn học '{class_name}' ({class_id}).")
        return True     

    def find_class(self, class_id):
        curr = self.classes.head
        while curr:
            f = curr.data
            if f.class_id == class_id:
                return f 
            curr = curr.next 
        return None 

    def enroll_students_to_class(self, student_id, class_id):
        check = self.find_class(class_id)
        if not check:
            print(" ❌ Không tìm thấy mã môn học này!")
            return False 
        
        sv_exist = False
        curr_sv = self.students.head
        while curr_sv:
            if curr_sv.data.student_id == student_id:
                sv_exist = True
                break
            curr_sv = curr_sv.next
        if not sv_exist:
            print(" ❌ Mã sinh viên này chưa được khởi tạo trên hệ thống trường!")
            return False

        curr = check.student_ids.head
        while curr:
            if curr.data == student_id:
                print(" ❌ Sinh viên này đã đăng ký môn học này rồi!")
                return False
            curr = curr.next
        check.student_ids.append(student_id)
        self.save_data()
        return True

    def get_student_by_class(self, class_id):
        res = LinkedList()
        check = self.find_class(class_id)
        if not check:
            print(f" ❌ Mã lớp {class_id} không tồn tại!")
            return False
        
        curr = check.student_ids.head 
        while curr:
            target_id = curr.data
            curr_id = self.students.head 
            while curr_id:
                if curr_id.data.student_id == target_id:
                    res.append(curr_id.data) 
                    break
                curr_id = curr_id.next
            curr = curr.next 
        return res 

    def take_attendance(self, date, class_id, input_status):
        check = self.find_class(class_id)
        if not check:
            print(" ❌ Không tìm thấy mã lớp này!")
            return
        
        students_list = self.get_student_by_class(class_id)
        if not students_list or not students_list.head:
            print(" ❌ Lớp học này hiện chưa có sinh viên nào đăng ký học!")
            return
            
        print(f"\n--- ĐIỂM DANH MÔN: {check.class_name} | NGÀY: {date} ---")
        curr = students_list.head
        while curr:
            c = curr.data
            status = input_status(c.name, c.student_id, c.major)
            self.attendance_records.append(AttendanceRecord(date, class_id, c.student_id, status))
            curr = curr.next
        self.save_data() 
        print("  Đã lưu kết quả điểm danh thành công!")

    def search_attendance(self, date, class_id):
        print(f"\n--- KẾT QUẢ ĐIỂM DANH MÔN {class_id} NGÀY {date} ---")
        curr = self.attendance_records.head
        found = False
        while curr:
            r = curr.data
            if r.class_id == class_id and r.date == date:
                c = self.students.head
                name, major = "Unknown", "Unknown"
                while c:
                    if c.data.student_id == r.student_id:
                        name = c.data.name
                        major = c.data.major 
                        break 
                    c = c.next  
                
                if r.status == 1:
                    status_str = "Có mặt"  
                elif r.status == 2:
                    status_str = "Vắng có phép"
                else:
                    status_str = "Vắng không phép"
                print(f"[{r.student_id}] {name} (Ngành: {major}) -> {status_str}")
                found = True 
            curr = curr.next 
        if not found:
            print(" ❌ Không tìm thấy dữ liệu điểm danh cho ngày và môn học này.")

    def report_most_absent(self):
        print("\n--- DANH SÁCH THỐNG KÊ VÀ CẢNH BÁO VẮNG HỌC ---")
        report_list = LinkedList()
        curr_class = self.classes.head
        
        while curr_class:
            cc = curr_class.data
            curr_student = self.students.head
            while curr_student:
                cs = curr_student.data    
                is_enrolled = False
                check_id = cc.student_ids.head
                while check_id:
                    if check_id.data == cs.student_id:
                        is_enrolled = True
                        break
                    check_id = check_id.next
                
                if is_enrolled:
                    curr_report = self.attendance_records.head
                    total_sessions = 0 
                    total_absents = 0
                    while curr_report:
                        cr = curr_report.data
                        if cc.class_id == cr.class_id and cs.student_id == cr.student_id:
                            total_sessions += 1
                            if cr.status in [2, 3]: 
                                total_absents += 1
                        curr_report = curr_report.next 
                    
                    if total_sessions > 0:
                        report_list.append(AttendanceReport(cs.student_id, cs.major, cs.name, cc.class_id, total_sessions, total_absents))
                curr_student = curr_student.next
            curr_class = curr_class.next
            
        if not report_list.head:
            print(" Chưa có dữ liệu điểm danh nào để thống kê.")
            return

        ### THUẬT TOÁN SẮP XẾP NỔI BỌT (BUBBLE SORT) ###
        end = None 
        while end != report_list.head:
            curr = report_list.head
            while curr.next != end:
                if curr.data.rate < curr.next.data.rate: 
                    curr.data, curr.next.data = curr.next.data, curr.data 
                curr = curr.next 
            end = curr 
            
        curr = report_list.head
        while curr:
            c = curr.data
            warning = "  ⚠️ [NGUY CƠ CẤM THI]" if c.rate > 20.0 else ""
            print(f"Môn: {c.class_id} | Ngành: {c.major} | [{c.student_id}] {c.name} | Vắng: {c.absent_count}/{c.total_sessions} buổi | Tỷ lệ vắng: {c.rate:.2f}%{warning}")
            curr = curr.next