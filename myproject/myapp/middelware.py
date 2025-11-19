
from django.http import JsonResponse
import re,json

class myappMiddelware:
    def __init__(self,get_response):
        self.get_response = get_response
    def __call__(self,request):
        response = self.get_response(request)
        print(request,"hello")
        print(request.method,"method")
        print(request.path)
        return response
# # class singnMiddelware:
#     def __init__(self,get_response):
#         self.get_response = get_response
#     def __call__(self,request):
#         if (request.path == "/add2"):
#             data = json.loads(request.method)
#             username = data.get("user_name")
#             password = data.get("password")
#             DOB = data.get("dob")
#             Email = data.get("Email")
#             pattern = re.match()
#             if username == re.match("^[\w\.]+!#$%&+@gmail\.com+$"):
#                 pass
#             print(data)
#             print(request.methods,"method")
#             reponse = self.get_response(request)
#         return reponse
 


# class sscMiddelware:
#     def __init__(self,get_response):
#         self.get_response = get_response
#     def __call__(self,request):
#         if request.path['job1/','job2/']:
#             ssc_result = request.GET.get("ssc")
#             if ssc_result != 'true':
#                 return JsonResponse({"error":"you are eligible without ssc"},status = 400)
#         return self.get_response(request)
# class medicalMiddelware:
#     def __init__(self,get_response):
#         self.get_response = get_response
#     def __call__(self, request):
#         if request.path == 'job1/':
#             medical_fit = request.GET.get("fit")
#             if medical_fit != 'true':
#                 return JsonResponse({"error":"u not medically fit to apply for this job role"},status=400)
#         return self.get_response(request)
        
# class ageMiddelware:
#     def __init__(self,get_response):
#         self.get_response = get_response
#     def __call__(self,request):
#         if request.path in ['job1/','job2/']:
#             age_checker = request.GET.get("age")
#             age_checker = int(age_checker)
#             if(age_checker < 18 or age_checker > 25):
#                 return JsonResponse({"Error":"your not eligible must be >18"})
#         return self.get_response(request)
class usernameMiddelware:
    def __init__(self,get_response):
        self.get_response = get_response
    def __call__(self,request):
        if request.path == "/signup/":
            data = json.loads(request.body)
            from myapp.models import Users
            user_name = data.get("username")
            if not user_name:
                return JsonResponse({"error":"username must requried"},status = 400)
            if len(user_name) < 3 or len(user_name) > 20:
                return JsonResponse({"Error":"username more than 3 character and "},status = 400)
            if user_name[0] in "._" or user_name[-1] in (".","_"):
                return JsonResponse({"error":" username should not start or end with . or _"},status =400)
            if not re.match(r"^[A-Za-z0-9._]+$", user_name):
                return JsonResponse({"Error":"username not matched the pattern"},status = 400)
            if ".." in user_name or "__" in user_name or " " in user_name:
                return JsonResponse({"Error":"username does not contain dounle .. or __ or " " sapces not accept"},status = 400)
            if Users.objects.filter(username = user_name).exists():
                return JsonResponse({"Error":"Username Already exits try another"},status=400)
        return self.get_response(request)

class emailMiddelware:
    def __init__(self,get_response):
        self.get_response = get_response
    def __call__(self,request):
        if request.path == "/signup/":
            from myapp.models import Users
            data = json.loads(request.body)
            user_email = data.get("email")
            if not user_email:
                return JsonResponse({"Error":"emailmust requried "},status = 400)
            pattern = r"^[A-Za-z0-9.&*]+@gmail\.com$"
            if not re.match(pattern,user_email):
                return JsonResponse({"Error":"mail format is not matched"},status = 400)
            if " " in user_email or "__" in user_email:
                return JsonResponse({"Error": "Username cannot contain .., __, or spaces"}, status=400)
            if Users.objects.filter(email= user_email).exists():
                return JsonResponse({"Error":"Email already exits"},status = 400)
        return self.get_response(request)
            
class passwordMiddelware:
    def __init__(self,get_response):
        self.get_response = get_response 
    def __call__(self,request):
        if request.path == "/signup/":
            data = json.loads(request.body)
            password = data.get("password")
            username = data.get("username")
            if not password:
                return JsonResponse({"Error":"must requried password"},status = 400)
            if not password[0].isupper():
                return JsonResponse({"Error":" password first letter should be capitial"},status = 400)
            if len(password) > 6:
                return JsonResponse({"Error":"password should be less than 6 letter"},status = 400)
            if re.match(username[0:4],password[0:4]):
                return JsonResponse({"Error":"username and password does not matched"},status = 400)
        return self.get_response(request) 


        
            