from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from myapp.models import studentsNew,Users,Movie
from django.contrib.auth.hashers import make_password,check_password
from django.conf import settings
import jwt
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
 


# Create your views here.
def sample_view(requests):
    return HttpResponse("Hello, this is a sample view!")
def add(request):
    a = request.GET.get("a",13)
    b = request.GET.get("b",13)
    result = a+b
    return HttpResponse(f"sum of a and b = {result} view")

def health(request):
    try:
        with connection.cursor() as c:
            c.execute("SELECT 1")
            return HttpResponse({"status" : "ok","db":"connected"})
    except Exception as e:
        return HttpResponse({"status": "Error","db": str(e)},status = 400)

   
# @csrf_exempt
# def addstudents(request):
#     if request.method == "POST":x
#         # print(data.name,data.age,data.email)
#         Student = studentsNew.objects.create(name = data.get("name"),age = data.get("age"),email = data.get("age"))
#         print(data.get("name"))
#         return JsonResponse({"status": "successful","studenhtid":Student.id},status = 400)
#     # elif request.method == "GET":
#     #     result = tuple(StudentNew.object)
#     return JsonResponse({"error":"use post method"},status = 400)

@csrf_exempt
def addstudents(requests):
    print(requests.method)
    if requests.method=="POST":
        data=json.loads(requests.body)
        student=studentsNew.objects.create(
            name=data.get("name"),
            age=data.get("age"),
            email=data.get("email")
        )
        return JsonResponse({"status":"success","id":student.id},status=400)
    elif requests.method=="GET":
        # data = json.loads(requests.body)
        # dat_filter = list(studentsNew.objects.values("age").distinct())
        result=tuple(studentsNew.objects.values())
        print(result)
        # print(dat_filter)
        return JsonResponse({"status":"ok","data" :result},status=200)
    elif requests.method=="PUT":
        data=json.loads(requests.body)
        ref_id=data.get("id") #getting id
        new_email=data.get("email") #getting email
        exisiting_student=studentsNew.objects.get(id=ref_id)  #fetched the object as per the id
        exisiting_student.email=new_email #updating with newemail
        exisiting_student.save()
        updated_data=studentsNew.objects.filter(id=ref_id).values().first()
        print(updated_data)
        return JsonResponse({"status":"data updated sucessfully","updated_data":updated_data},status=200)
    elif requests.method=="DELETE":
        data=json.loads(requests.body)
        ref_id=data.get("id") #getting id
        get_deleting_data=studentsNew.objects.filter(id=ref_id).values().first()
        to_be_delete=studentsNew.objects.get(id=ref_id)
        to_be_delete.delete()
        return JsonResponse({"status":"sucess","message":"student record deleted sucessfully","deleted data":get_deleting_data},status=200)
    return JsonResponse({"error":"use post method"},status=400)


# def job1():
#     return JsonResponse({"message":"u have successfully applied for job1"},status=200) 
# def job2():
#     return JsonResponse({"message":"u have successfully applied for job2"},status=200) 

@csrf_exempt
def signup(request):
    if request.method == "POST":
        data = request.POST
        print(data)
        user = Users.objects.create(
            username = data.get("username"),
            email = data.get("email"),
            password= make_password(data.get("password")))
        return JsonResponse({"status":"success","data":data},status = 200)
    
@csrf_exempt    
def login(request):
    if request.method == "GET":
        data = request.POST
        users =  list(Users.objects.all().values())
        return JsonResponse({"status": "successful","data":users},status = 200)

    elif request.method == "POST":
        data = request.POST
        user_name = data.get("username")
        password = data.get("password")
        try:
            users = Users.objects.get(username = user_name)
        except:
            return JsonResponse ({"status":"username is incorrect"},status = 400)
        users = Users.objects.get(username = user_name)
        issued_time= datetime.now(ZoneInfo("Asia/kolkata"))
        expired_time = issued_time+timedelta(minutes = 2)

        if check_password(password, users.password):
                payload = {
                    "username":"username",
                    "email":users.email,
                    "password":users.password,
                    "exp": expired_time
                }
                token = jwt.encode(payload,settings.SECRET_KEY,algorithm="HS256")
                return JsonResponse ({"status":"login success","token":token,"issued_time":issued_time,"expiretime_ in":expired_time,"expired in":f"{int((expired_time-issued_time).total_seconds()/60)} min"},status = 200)
        return JsonResponse ({"status":"password is incorrect"},status = 400)
            
@csrf_exempt    
def check(request):
    if request.method == "POST":
        data = request.POST
        hashed =Users.objects
        x = check_password(data.get("password"),hashed)
        print(x)
        return JsonResponse({"data" : x},status = 200)
    return JsonResponse({"status":"erroe"},status = 400)


@csrf_exempt
def forget_password(request):
    if request.method == "POST":
        data = request.POST
        new_password = data.get("password")
        username = data.get("username")
        try:
            user = Users.objects.get(username = username)
        except :
            return JsonResponse({"status":"error user not found"})
        if ( Users.objects.get(username = username)):
            user.password = new_password
            return JsonResponse({"status":"password changed successfully"},status = 200)
        return JsonResponse({"Error":"password not done to cjange"})


# @csrf_exempt
# def moive(request):
#     if request.method == "POST":
#         data = request.POST
#         movie_detils = Movie.objects.create(
#             movie_name = data.get("name"),
#             movie_date = data.get("date"),
#             movie_budget = data.get("budget"),
#             movie_rating = data.get("rating")
#         )
#         return JsonResponse({"status":"success","data":data},status = 200)
#     elif request.method == "GET":
#         data = request.POST
#         name = list(Movie.objects.all())
#         return JsonResponse({"status":"all data are showed"})
#     elif request.method == "PUT":
#         data = request.POST


