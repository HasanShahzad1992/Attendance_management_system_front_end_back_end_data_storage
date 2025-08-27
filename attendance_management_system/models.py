from tkinter.constants import CASCADE

from django.db import models

class Student_Data(models.Model):
    Seccap_id=models.CharField(max_length=25,primary_key=True)
    Name=models.CharField(max_length=100)
    Father_name=models.CharField(max_length=100)
    sex=models.CharField(max_length=15)
    contact_number=models.CharField(max_length=20)
    choice_of_group=models.CharField(max_length=100)

# class Student_Attendance(models.Model):
#     seccap_object_foreign_key=models.ForeignKey(Student_Data,on_delete=models.CASCADE)
#     time_stamps=models.DateTimeField()
#     status_of_attendance=models.CharField(max_length=20)

class Student_Attendance(models.Model):
    seccap_object_foreign_key=models.ForeignKey(Student_Data,on_delete=models.CASCADE)
    status_of_attendance=models.CharField(max_length=20)
    date=models.DateField()
    time=models.TimeField()
    time_stamps=models.DateTimeField()
# in foreign key column, we send object
# class Abc:
#     def __init__(self,name_of_father):
#         self.name_of_father = name_of_father
#     def display_name(self):
#         print(self.name_of_father)
#     def display_greetings(self):
#         print("Hello")

# # obj = Abc("basit")
# Abc.display_greetings()
#
# let time_now=Date.now()