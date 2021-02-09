from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from . models  import userData, Turf, Booking
import ast
import json
# Create your views here.

def home(request):
    turf = Turf.objects.all()
    return render(request, 'users/home.html', {'turfs' : turf})


def turfview(request, id):
    turf = Turf.objects.get(id=id)
    turf.sport = json.loads(turf.sport)
    print(turf.sport)
    turf.facilities = ast.literal_eval(turf.facilities)
    turf.timePeriod = ast.literal_eval(turf.timePeriod)
    return render(request, 'users/turf.html', {'turf' : turf})


def usersignin(request):
    if request.user.is_authenticated:
        return redirect(home)
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return JsonResponse('true', safe=False)
            else:
                return JsonResponse('false', safe=False)
        else:    
            return render(request, 'users/login.html')


def usersignup(request):
    if request.user.is_authenticated:
        return redirect(home)
    else:
        if request.method == 'POST':
            firstName = request.POST['firstName']
            mobile = request.POST['mobile']
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password']
            if User.objects.filter(email=email).exists():
                return JsonResponse('email', safe=False)
            elif User.objects.filter(username=username).exists():
                return JsonResponse('username', safe=False)
            else:
                user = User.objects.create_user(first_name=firstName, email=email, username=username, password=password)
                userData.objects.create(user=user, phone=mobile)
                return JsonResponse('true', safe=False)
            
        else:    
            return render(request, 'users/usersignup.html')


def userbooking(request, id):
    print('hello')
    if request.user.is_authenticated:
        if request.method=='POST':
            print('hha')
            # name = request.POST['name']
            # phone = request.POST['phone']
            # email = request.POST['email']
            # turf = request.POST['turf']
            date = request.POST['date']
            hour = request.POST['hour']
            sport = request.POST['sport']
            user = request.user
            userdata = userData.objects.get(user=user)
            turf = Turf.objects.get(id=id)
            # date = Booking.objects.get(turf=turf)
            # user.first_name = name
            # user.email = email
            # userdata.phone = phone
            # turf.turf = turf
            # date.date = date
            # turf.hour = hour
            # turf.sport = sport
            # user.save()
            # userData.save()
            # turf.save()
            # date.save()
            # userdata =  userData.objects.get(id=id)
            
            
            booking = Booking.objects.create(turf_name=turf.turfName, date=date, time_period=hour, sport=sport, userdata= userdata )
            bookings = Booking.objects.get(id=id)
            return render(request, 'users/history.html', {'booking' : bookings})
        else:
            user = request.user
            turf = Turf.objects.get(id=id)
            turf.sport = json.loads(turf.sport)
            turf.timePeriod = ast.literal_eval(turf.timePeriod)
            userdata = userData.objects.get(id=user.id)
            bookings = Booking.objects.get(id=id)
            print('higbhbli')
            return render(request, 'users/booking.html', {'user' : user, 'turfs' : turf, 'userData' : userdata, 'booking' : bookings})
    else:
        return redirect(usersignin)



def logout(request):
    if request.user.is_authenticated:
        user = request.user
        auth.logout(request)
        return redirect(home)
    else:
        return redirect(usersignin)
    
def bookHistory(request,id):
    if request.user.is_authenticated:
        booking = Booking.objects.get(id=id)
        turf = Turf.objects.get(id=id)
        print(booking)
        turf.sport = json.loads(turf.sport)

        
        # user = request.user
        return render(request, 'users/history.html',{'booking':booking, 'turfs' : turf})
    else:
        return redirect(usersignin)



