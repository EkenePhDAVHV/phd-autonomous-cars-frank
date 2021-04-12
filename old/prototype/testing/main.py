print("Hello\nWorld")

marks = []

for student in range(0,10):
    print("I am student " + str(student))
    marks.append(int(input("Enter Mark : ")))
sumval = sum(marks)
print ("Sum : " + str(sumval))