# structures.py

class Node:
    def __init__(self, data):
        self.data = data      # Lưu trữ dữ liệu (ví dụ: student_id, ClassInfo...)
        self.next = None      # Con trỏ trỏ đến Node tiếp theo


class LinkedList:
    def __init__(self):
        self.head = None      # Ban đầu danh sách rỗng

    def append(self, data):
        new_node = Node(data) # 1. Tạo một Node mới chứa dữ liệu
        
        # Case 1: Nếu danh sách đang rỗng, Node mới chính là head
        if self.head is None:
            self.head = new_node
            return
            
        # Case 2: Nếu danh sách đã có phần tử, duyệt đến Node cuối cùng
        curr = self.head
        while curr.next is not None:
            curr = curr.next
            
        # Gán Node mới vào đuôi danh sách
        curr.next = new_node