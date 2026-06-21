from manager import AttendanceManager

def get_attendance_input(name, student_id, major):
    while True:
        try:
            status = int(input(f"SV: {name} ({student_id}) - Ngành: {major} [1-Có, 2-Phép, 3-Vắng]: "))
            if status in [1, 2, 3]:
                return status
            print(" ❌ Chỉ nhập 1, 2 hoặc 3!")
        except ValueError:
            print(" ❌ Vui lòng nhập số!")
def main():
    manager = AttendanceManager()
    
    while True:
        print("\n========================================")
        print("   HỆ THỐNG QUẢN LÝ ĐIỂM DANH HỌC PHẦN  ")
        print("========================================")
        print("1. Tạo môn học mới")
        print("2. Thêm hoặc Đăng ký sinh viên vào môn học")
        print("3. Tìm danh sách sinh viên học 1 môn học bất kỳ")
        print("4. Thực hiện điểm danh theo ngày")
        print("5. Xem danh sách điểm danh theo ngày của môn học")
        print("6. Xuất danh sách cảnh báo vắng học theo môn")
        print("0. Thoát")

        choice = input("Mời chọn chức năng (0-6): ").strip()
        
        if choice == "1":
            class_id = input("Nhập mã môn học: ").strip()
            class_name = input("Nhập tên môn học: ").strip()
            day = input("Nhập thứ học: ").strip()
            period = input("Nhập tiết học: ").strip()
            room = input("Nhập phòng học: ").strip()
            
            manager.add_class(class_id, class_name, day, period, room)
            
        elif choice == "2":
            student_id = input("Nhập mã sinh viên: ").strip()
            name = input("Nhập họ tên sinh viên: ").strip()
            major = input("Nhập ngành học của sinh viên: ").strip()
            class_id = input("Nhập mã môn học sinh viên muốn đăng ký vào: ").strip()
            
            manager.add_student_to_system(student_id, name, major)
            
            if manager.enroll_students_to_class(student_id, class_id):
                print(f"  Đăng ký thành công cho SV {name} vào môn {class_id}!")
                
        elif choice == "3":
            class_id = input("Nhập mã lớp muốn kiểm tra danh sách lớp: ").strip()
            students_list = manager.get_student_by_class(class_id)
            
            if students_list:
                curr = students_list.head
                if not curr:
                    print("  Môn học này chưa có sinh viên nào đăng ký.")
                else:
                    print(f"\n--- DANH SÁCH LỚP PHẦN: {class_id} ---")
                    index = 0
                    while curr:
                        index += 1
                        s = curr.data  
                        print(f"{index}. [{s.student_id}] {s.name} | Ngành: {s.major}")
                        curr = curr.next
                        
        elif choice == "4":
            date = input("Nhập ngày thực hiện điểm danh (DD/MM/YYYY): ").strip()
            class_id = input("Nhập mã môn học: ").strip()
            manager.take_attendance(date, class_id, get_attendance_input)
            
        elif choice == "5":
            date = input("Nhập ngày cần tìm (DD/MM/YYYY): ").strip()
            class_id = input("Nhập mã môn học: ").strip()
            manager.search_attendance(date, class_id)
            
        elif choice == "6":
            manager.report_most_absent()
            
        elif choice == "0":
            print("💾 Dữ liệu đã được cập nhật an toàn lên ổ cứng!")
            print("👋 Tạm biệt!")
            break
        else:
            print(" ❌ Lựa chọn không hợp lệ! Vui lòng chọn từ 0 đến 6.")

if __name__ == "__main__":
    main()