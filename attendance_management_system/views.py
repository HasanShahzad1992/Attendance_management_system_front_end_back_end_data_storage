from django.shortcuts import render
import json
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from .models import Student_Data,Student_Attendance



@csrf_exempt
def student_data_manually_added_from_excel(initial_request_from_front_end):
    original_excel_file=initial_request_from_front_end.FILES["excel_file_uploaded"]
    panda_data_frame=pd.read_excel(original_excel_file,sheet_name="Database")
    for i,j in panda_data_frame.iterrows():
        student_seccap_id=j["Seccap_Id"]
        Student_name=j["Name"]
        Name_of_Father=j["Father_Name"]
        Sex_of_student=j["Gender"]
        Mobile_number=j["Contact_No"]
        Faculty_department=j["Choice_of_Faculty"]
        copy_received=Student_Data.objects.create(Seccap_id=student_seccap_id,Name=Student_name,Father_name=Name_of_Father,sex=Sex_of_student,contact_number=Mobile_number,choice_of_group=Faculty_department)
    return HttpResponse("for loop done")

def all_student_data_after_clicking_bulk_button(initial_request_from_front_end):
    all_student_data_list_of_dictionaries=list(Student_Data.objects.all().values())
    return JsonResponse({"data_of_all_students":all_student_data_list_of_dictionaries})
@csrf_exempt
def sending_student_data_after_scanning_card(initial_request_from_front_end):
    original_dictionary_in_python=json.loads(initial_request_from_front_end.body)
    seccap_id_of_student=original_dictionary_in_python["seccap_id"]
    time_date_stamp=original_dictionary_in_python["time_date_combined"]
    time_of_scan=original_dictionary_in_python["time_in_12"]
    date_of_scan=original_dictionary_in_python["date_of_scan"]
    current_attendance_status=original_dictionary_in_python["attendance-status"]

    object_of_current_student_whether_enrolled_in_class_or_not=Student_Data.objects.filter(Seccap_id=seccap_id_of_student)
    query_set_converted_to_dict = list(object_of_current_student_whether_enrolled_in_class_or_not.values())

    object_of_whether_student_marked_attendance_for_same_date=Student_Attendance.objects.filter(date=date_of_scan,seccap_object_foreign_key_id=seccap_id_of_student)
    second_query_set_same_student_same_date_attendance_dict=list(object_of_whether_student_marked_attendance_for_same_date.values())



    length_of_list_whether_student_enrolled_in_class=len(query_set_converted_to_dict)
    length_of_list_whether_same_student_marked_attendance_for_same_date=len(second_query_set_same_student_same_date_attendance_dict)
    if length_of_list_whether_student_enrolled_in_class<1:
        return JsonResponse({"message":"this student data does not exist"})
    elif length_of_list_whether_student_enrolled_in_class==1 and length_of_list_whether_same_student_marked_attendance_for_same_date==0 :
        copy_received=Student_Attendance.objects.create(seccap_object_foreign_key_id=seccap_id_of_student,status_of_attendance=current_attendance_status,date=date_of_scan,time=time_of_scan,time_stamps=time_date_stamp)
        return JsonResponse({"message":"attendance has been marked successfuly for " + copy_received.seccap_object_foreign_key.Name + " for date " + copy_received.date + " on " + copy_received.time})
    else:
        return JsonResponse({"message":"the same student attendance has already been marked for " + date_of_scan })

@csrf_exempt
def marking_individual_attendance_of_student(initial_request_from_front_end):
    original_dictionary_in_python=json.loads(initial_request_from_front_end.body)
    date_when_attendance_marked=original_dictionary_in_python["date_of_marking_attendance"]
    time_when_attendance_marked=original_dictionary_in_python["time_at_which_attendance_marked"]
    time_stamps_of_when_attendance_marked=original_dictionary_in_python["time_and_date_combined"]
    id_of_student=original_dictionary_in_python["seccap_id"]
    status_of_attendance=original_dictionary_in_python["attendance_status"]

    object_of_current_student_whether_enrolled_in_class=Student_Data.objects.filter(Seccap_id=id_of_student)
    print(type(object_of_current_student_whether_enrolled_in_class),"A")
    query_set_of_whether_student_enrolled_in_class_in_dict=list(object_of_current_student_whether_enrolled_in_class.values())

    object_of_whether_same_student_marked_on_same_date_or_not=Student_Attendance.objects.filter(date=date_when_attendance_marked,seccap_object_foreign_key_id=id_of_student)
    print(type(object_of_whether_same_student_marked_on_same_date_or_not),"B")
    query_set_of_whether_same_student_marked_on_same_date_dict=list(object_of_whether_same_student_marked_on_same_date_or_not.values())

    if len(query_set_of_whether_student_enrolled_in_class_in_dict)==1 and len(query_set_of_whether_same_student_marked_on_same_date_dict)==0:
        copy_received=Student_Attendance.objects.create(seccap_object_foreign_key_id=id_of_student,status_of_attendance=status_of_attendance,time=time_when_attendance_marked,date=date_when_attendance_marked,time_stamps=time_stamps_of_when_attendance_marked)
        print(type(copy_received),"C")
        return JsonResponse({"message":"Student "+ copy_received.seccap_object_foreign_key.Name + " attendance status has been updated for " + date_when_attendance_marked})
    elif len(query_set_of_whether_student_enrolled_in_class_in_dict)==0:
        return JsonResponse({"message":"No student exists with this current seccap id in this class"})
    elif len(query_set_of_whether_same_student_marked_on_same_date_dict)==1:
        return JsonResponse({"message":"Attendance for " + query_set_of_whether_student_enrolled_in_class_in_dict[0]["Name"] + " on " + date_when_attendance_marked + " is already marked "})

@csrf_exempt
def sending_attendance_of_class_in_bulk(initial_request_from_front_end):

    original_dictionary_in_python=json.loads(initial_request_from_front_end.body)
    list_holding_dictionaries_holding_seccap_id_attendance_status_date_and_time=original_dictionary_in_python["list_holding_dictionaries"]
    current_date_of_taking_attendance=list_holding_dictionaries_holding_seccap_id_attendance_status_date_and_time[0]["date_attendance"]
    for i in list_holding_dictionaries_holding_seccap_id_attendance_status_date_and_time:
        attendance_status_of_student=i["attendance_status_of_student"]
        seccap_id_of_student=i["seccap_Id"]
        date_of_attendance=i["date_attendance"]
        time_of_attendance=i["time_attendance"]
        time_stamp=i["attendance_time_stamp"]
        query_set_of_whether_same_student_marked_on_same_date=Student_Attendance.objects.filter(seccap_object_foreign_key_id=seccap_id_of_student,date=date_of_attendance)
        converting_query_set_into_list_of_dictionary=list(query_set_of_whether_same_student_marked_on_same_date.values())
        if len(converting_query_set_into_list_of_dictionary)==1:
            pass
        else:
            copy_received=Student_Attendance.objects.create(status_of_attendance=attendance_status_of_student,date=date_of_attendance,time=time_of_attendance,time_stamps=time_stamp,seccap_object_foreign_key_id=seccap_id_of_student)
    return JsonResponse({"message":"Attendance for " + current_date_of_taking_attendance + "has been successfully marked"})



