import json

# 讀取 JSON 文件
with open('students.json', 'r') as file:
    data = json.load(file)

# 打印讀取到的數據
print("Data read from JSON file:", data)

# 訪問學生列表
students = data["students"]

# 打印學生列表
print("Students list:", students)

# 遍歷學生列表
for student in students:
    print(f"ID: {student['id']}, Name: {student['name']}, Age: {student['age']}")
    print("Grades:")
    for subject, grade in student["grades"].items():
        print(f"  {subject}: {grade}")

# 計算每個學生的平均成績
for student in students:
    grades = student["grades"]
    average_grade = sum(grades.values()) / len(grades)
    print(f"Average grade for {student['name']}: {average_grade}")