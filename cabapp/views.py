from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import *
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse
from .forms import ContactForm
import hashlib


def index(request):
    return render(request, "index.html", {"car": car})


def cars(request):
    car = car_tb.objects.all()
    if car.exists():
        return render(request, "index.html", {"car": car})
    else:
        return render(request, "index.html")


def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            # Send the email
            subject = "Contact Form Submission"
            message = f"Name: {name}\nEmail: {email}\nMessage: {message}"
            from_email = email
            recipient_list = [ settings.EMAIL_HOST_USER ]  # Replace with the email where you want to receive the form submissions
            send_mail(subject, message, from_email, recipient_list)
            return HttpResponseRedirect('/')
            # Redirect to a success page
    else:
        form = ContactForm()
        return render(request,"index.html",{"form": form, "car": car})


# def handle_404(request,exception):
#   return render(request,'404.html',{})
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)


########################################### ADMIN ########################################################################
db = admin_login_tb.objects.all()
car = car_tb.objects.all()


def admin(request):
    if request.session.has_key("myid"):
        return render(request, "admin/index.html", {"db": db})
    else:
        return render(request, "login/login.html")


# def admin_reg(request):
#   if request.method=="POST":
#       name=request.POST['name']
#       email=request.POST['email']
#       password=request.POST['password']
#       check=admin_login_tb.objects.all().filter(email=email)
#       if check:
#           messages.error(request,'Email already registered')
#           return render(request,'login/register.html')

#       else:
#           add=admin_login_tb(name=name,email=email,password=password)
#           add.save()
#           messages.success(request,'Account Registered Successfully')
#           return render(request,'login/register.html')
#   else:
#       return render(request,'login/register.html')


def admin_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        hashpass = hashlib.md5(password.encode("utf8")).hexdigest()
        b = admin_login_tb.objects.all().filter(email=email, password=hashpass)
        # b = admin_login_tb.objects.all().filter(email=email, password=password)
        if b.exists():
            for x in b:
                request.session["myid"] = x.id
                return render(request, "admin/index.html", {"db": db})

        else:
            messages.error(request, "Invalid credentials")
            return render(request, "login/login.html")
    else:
        return render(request, "login/login.html")


def admin_logout(request):
    if request.session.has_key("myid"):
        del request.session["myid"]
        logout(request)
    return HttpResponseRedirect("/admin_login/")


def admin_view_profile(request):
    if request.session.has_key("myid"):
        db = admin_login_tb.objects.all().filter()
        print(db)
        if db.exists():
            print("get record")
            return render(request, "admin/view_profile.html", {"db": db})
        else:
            print("failed")
            return render(request, "admin/index.html")
    else:
        return render(request, "login/login.html")


def admin_update_profile(request):
    print("inside getData")
    if request.method == "GET":
        id2 = request.GET["id"]
        b = admin_login_tb.objects.all().filter(id=id2)
        print(b)
        if b.exists():
            print("get record")
            # messages.success(request,'Profile Updated Successfully')
            return render(request, "admin/update_profile.html", {"db": b})
        else:
            print("failed")
            # messages.error(request,'Profile Update Failed')
            return render(
                request,
                "admin/view_profile.html",
                {"message": "Profile Update Failed", "db": b},
            )


def admin_view_update_profile(request):
    if request.session.has_key("myid"):
        if request.method == "POST":
            print("----------update inside post-----------")
            up = request.GET["id"]
            name = request.POST["name"]
            email = request.POST["email"]
            # password=request.POST['password']

            ii = request.session["myid"]

            # admin_login_tb.objects.filter(id=up).update(name=name,email=email,password=password)
            admin_login_tb.objects.filter(id=up).update(name=name, email=email)
            up = admin_login_tb.objects.all().filter()
            print("-----------------render page--------------")
            messages.success(request, "Profile Updated Successfully")
            return render(request, "admin/update_profile.html", {"db": up})
        elif request.method == "GET":
            print("-----------------get update------------")
            id1 = request.GET["id"]
            up = admin_login_tb.objects.all().filter(id=up)
            print("-----------------render page**************")
            messages.error(request, "Profile Update Failed")
            return render(request, "admin/view_profile.html", {"db": up})
    else:
        return render(request, "login/login.html")


def add_car(request):
    if request.session.has_key("myid"):
        if request.method == "POST":
            image = request.FILES["image"]
            name = request.POST["name"]
            people = request.POST["people"]
            fuel = request.POST["fuel"]
            miles = request.POST["miles"]
            transmission = request.POST["transmission"]

            s = car_tb(
                image=image,
                name=name,
                people=people,
                fuel=fuel,
                miles=miles,
                transmission=transmission,
            )
            s.save()
            messages.success(request, "Car Added Successfully")
            return render(request, "admin/add_car.html", {"db": db})

        else:
            # messages.error(request,'Car Add Failed')
            return render(request, "admin/add_car.html", {"db": db})
    else:
        return render(request, "login/login.html")


def view_car(request):
    if request.session.has_key("myid"):
        car = car_tb.objects.all()
        if car.exists():
            return render(request, "admin/view_car.html", {"car": car, "db": db})
        else:
            return render(request, "admin/view_car.html", {"db": db})
    else:
        return render(request, "login/login.html")


def view_single_car(request):
    print("inside getData")
    if request.session.has_key("myid"):
        if request.method == "GET":
            id2 = request.GET["id"]
            car = car_tb.objects.all().filter(id=id2)
            print(car)
            if car.exists():
                print("get record")
                return render(
                    request, "admin/view_single_car.html", {"car": car, "db": db}
                )
            else:
                print("failed")
                return render(request, "admin/view_car.html")
    else:
        return render(request, "login/login.html")


def delete_car(request):
    if request.session.has_key("myid"):
        cid = request.GET["id"]
        car_tb.objects.all().filter(id=cid).delete()
        car = car_tb.objects.all()
        messages.success(request, "Car Deleted Successfully")
        return render(request, "admin/view_car.html", {"car": car, "db": db})
    else:
        return render(request, "login/login.html")


def update_car(request):
    print("inside getData")
    if request.session.has_key("myid"):
        if request.method == "GET":
            id2 = request.GET["id"]
            car = car_tb.objects.all().filter(id=id2)
            print(car)
            if car.exists():
                print("get record")
                return render(request, "admin/update_car.html", {"car": car, "db": db})
            else:
                print("failed")
                return render(request, "admin/view_car.html")
    else:
        return render(request, "login/login.html")


def view_update_car(request):
    if request.session.has_key("myid"):
        if request.method == "POST":
            print("----------update inside post-----------")
            up = request.GET["id"]
            name = request.POST["name"]
            people = request.POST["people"]
            fuel = request.POST["fuel"]
            miles = request.POST["miles"]
            transmission = request.POST["transmission"]

            imgup = request.POST["imgupdate1"]
            if imgup == "Yes":
                image = request.FILES["image"]
                oldrec = car_tb.objects.all().filter(id=up)
                updrec = car_tb.objects.get(id=up)
                for x in oldrec:
                    imgurl = x.image.url
                    pathtoimage = (os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+ imgurl)
                    if os.path.exists(pathtoimage):
                        os.remove(pathtoimage)
                        print("Successfully deleted")
                updrec.image = image
                updrec.save()

            car_tb.objects.filter(id=up).update(
                name=name,
                people=people,
                fuel=fuel,
                miles=miles,
                transmission=transmission,
            )
            up = car_tb.objects.all().filter()

            print("-----------------render page--------------")
            messages.success(request, "Car Updated Successfully")
            return render(request, "admin/view_car.html", {"car": up, "db": db})
        elif request.method == "GET":
            print("-----------------get update------------")
            id1 = request.GET["id"]
            up = car_tb.objects.all().filter(id=up)

            print("-----------------render page--------------")
            messages.error(request, "Car Update Failed")
            return render(request, "admin/view_car.html", {"car": up, "db": db})
    else:
        return render(request, "login/login.html")
