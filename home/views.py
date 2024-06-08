import json
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login 
from django.contrib.auth import logout
from django.contrib import messages
from userproject import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from django.core.mail import EmailMessage, send_mail
from django .utils.http import urlsafe_base64_decode
from .models import Student
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_protect
import requests
from django.conf import settings
from django.http import JsonResponse
#password for Radz user - Radhika@user
# Create your views here.

RECAPTCHA_SECRET_KEY = "6Lezdb4pAAAAAH7EgRxrwFpzAunXAMaVp1_7pzyi"

#captcha verification
import requests
from django.conf import settings

def verify_recaptcha(recaptcha_response):
    data = {
     #    'secret': settings.RECAPTCHA_SECRET_KEY,
          'secret': RECAPTCHA_SECRET_KEY,
          'response': recaptcha_response
    }
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = response.json()
    return result['success']

def studenthome(request):
    return render(request,'home.html')

def formSubmission(request):
     #if request.user.is_anonymous:
        #return redirect("/login")
     if request.method== "POST":
         
         name=request.POST.get("name")
         email=request.POST.get("email")
         dob=request.POST.get("dob")
         English=request.POST.get("English")         
         Hindi=request.POST.get("Hindi")
         Maths=request.POST.get("Maths")
         Science=request.POST.get("Science")
         Total_Score_10th = request.POST.get("Total_Score_10th")
         Physics=request.POST.get("Physics")
         Chemistry=request.POST.get("Chemistry")
         Maths2=request.POST.get("Maths2")
         Total_Score_12th = request.POST.get("Total_Score_12th")
         Overall_Score = request.POST.get("Overall_Score")
         Course = request.POST.get("Course")
         print(name,email,dob,English,Hindi,Maths,Science,Total_Score_10th,Physics,Chemistry,Maths2,Total_Score_12th,Overall_Score)
         my_user =Student(name=name,email=email,dob=dob,English=English,Hindi=Hindi,Maths=Maths,Science=Science,Total_Score_10th=Total_Score_10th,Physics=Physics,Chemistry=Chemistry,Maths2=Maths2,Total_Score_12th=Total_Score_12th,Overall_Score=Overall_Score, Course = Course)
         my_user.save() 
         messages.success(request,"Data inserted successfully!")
         return redirect('/home')
     else:
         return render(request,'home.html')
def loginUser(request):
     if request.method == "POST":
          username= request.POST.get("username")
          password = request.POST.get("password")
          hashed_password = make_password(password)
          print(username,password)
          #check if user has entered correct credentials
          my_user = authenticate(username = username, password= password)
          if my_user is not None:
          # A backend authenticated the credentials
               login(request, my_user)
               recaptcha_response = request.POST.get('g-recaptcha-response')
               if verify_recaptcha(recaptcha_response):
                    if my_user.is_staff:
                       return redirect("/adminpage")
                    else:
                     return redirect("/homepage")
               else:
                    # messages.error(request, "Incorrect Captcha Try again!!")
                    # return redirect('/login')
                    return HttpResponse("Captcha is incorrect Please refresh and retry again!!")
            
          # No backend authenticated the credentials
          return render(request,'login.html') 
     return render(request,'login.html')
def logoutUser(request):
     logout(request)
     return redirect("/login")

def registerUser(request):
     if request.method =="POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        
        hashed_password = make_password(password)
        if User.objects.filter(username=username):
            messages.error(request,"Username already exist! Please try some other username")
            return redirect('/register')
        if User.objects.filter(email=email):
           messages.error(request,"Email already registered!")
           return redirect('/register') 
        if len(username)>10:
           messages.error(request,"Username must be under 10 characters")
        if password!= password2:
           messages.error(request,"passwords didn't match") 
        if not username.isalnum():
            messages.error(request,"Username must be Alpha-Numeric!")
            return redirect('/register')     
                           
        my_user = User.objects.create_user(username=username,email=email,password=password)
        my_user.is_active = False
        my_user.save() 
        messages.success(request,'Account created successfully!We have sent you a confirmation email,please confirm your email in order to activate your account. ')

        #Welcome mail
        subject = "Welcome to Django Login!"
        message = "Hello" + my_user.username + "!!\n" +"Welcome to Student Portal\n Thank you for visiting our website\n We have also sent you a confirmation email,please confirm your email address in order to activate your account\n\n Thanking You\n Radhika Agarwal" 
        from_email = settings.EMAIL_HOST_USER
        to_list = [my_user.email]
        send_mail(subject,message,from_email,to_list,fail_silently =True )

        #Email Address Confirmation email
        current_site = get_current_site
        (request)
        email_subject = "Confirm your email @ User django login!!"
        message2  = render_to_string('email_confirmation.html', {
          'name':my_user.first_name,
          'domain': get_current_site(request).domain,
          'uid': urlsafe_base64_encode(force_bytes(my_user.pk)),
          'token': generate_token.make_token(my_user) ,
          "protocol": 'https' if request.is_secure() else 'http' 
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [my_user.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('/login')
     return render(request,'register.html')  

def activate(request,uidb64,token):
     try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        my_user = User.objects.get(pk=uid)
     except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        my_user = None

     if my_user is not None and generate_token.check_token(my_user,token):
        my_user.is_active = True
        my_user.save()
        messages.success(request,"Thank you for email confirmation. Now you can login your account.")
        login(request,my_user)
        return redirect('/login')
     else:
         return render(request,'activation_failed.html')  

def registerAdmin(request):
    if request.method =="POST":
       username=request.POST.get("username")
       password=request.POST.get("password")
       password2=request.POST.get("password2")
       
       hashed_password = make_password(password)
       my_user=User.objects.create_superuser(username=username,password=password)
       my_user.is_active = True
       my_user.save()
       
       return redirect('/login')
    
    return render(request,"admin_register.html")

def admin_dashboard(request):
      return redirect("/admin") 
     # return HttpResponse("Hello Success")
       

    
   
