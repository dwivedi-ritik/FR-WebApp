import os

r = os.path.isdir("./Attendence lists/8")

if not r:
    os.mkdir("./Attendence lists/8")

# print(r)