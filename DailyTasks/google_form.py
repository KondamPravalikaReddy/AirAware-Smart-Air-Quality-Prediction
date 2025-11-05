name = input("Enter your name: ")                       
age = int(input("Enter your age: "))                    
marks = float(input("Enter your marks: "))             
is_student = input("Are you a student? (yes/no): ")     

# Output with different methods
print("Name:", name, "Age:", age, "Marks:", marks, "Student:", is_student)       
print("Name: " + name + " Age: " + str(age))                                    
print("Marks: %0.2f" % marks)                                                   
print("Student: {} Age: {}".format(is_student, age))                           
print(f"Name: {name} Age: {age}")                                         