from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from . models  import userData, Turf, Booking, sportPrice, turfFacility
import ast
import json
# Create your views here.

def home(request):
    turf = Turf.objects.all()
    sport_price = sportPrice.objects.all()
    context = {'sport' : sport_price, 'turfs' : turf}
    return render(request, 'users/home.html', context)


def category(request, id):
    sport = sportPrice.objects.filter(category_id=id)
    turf_id_list = []
    for x in sport:
        turf_id_list.append(x.turf.id)
    print(turf_id_list)
    turf = Turf.objects.filter(id__in=turf_id_list)
    print(turf)
    context = {'turf' : turf}
    return render(request, 'users/category.html', context)



def turfview(request, id):
    turf = Turf.objects.get(id=id)
    sport_price = sportPrice.objects.filter(turf_id=turf.id )
    facility = turfFacility.objects.filter(turf_id=turf.id)
    # turf_facility = turfFacility.objects.get(id=id)'turffacility' : turf_facility,
    turf.timePeriod = ast.literal_eval(turf.timePeriod)
    return render(request, 'users/turf.html', {'turf' : turf,   'sportprice' : sport_price, 'facility' : facility})


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
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST['name']
            phone = request.POST['phone']
            email = request.POST['email']
            sport = request.POST['sport']
            date = request.POST['date']
            hour = request.POST['hour']
            turf = Turf.objects.get(id=id)
            sport_price = sportPrice.objects.filter(turf_id=turf.id)
            booking = Booking.objects.create(name=name, phone=phone, email=email, date=date)
            
        else:
            user = request.user
            turf = Turf.objects.get(id=id)
            turf.timePeriod = ast.literal_eval(turf.timePeriod)
            userdata = userData.objects.get(id=user.id)
            sport_price = sportPrice.objects.filter(turf_id=turf.id)
            context = {'user' : user, 'turfs' : turf, 'userData' : userdata, 'sportprice' : sport_price}
            return render(request, 'users/booking.html', context)
    else:
        return redirect(usersignin)


def bookHistory(request, id):
    if request.user.is_authenticated:
        turf = Turf.objects.get(id=id)
        print(booking)
        context = {'booking':booking, 'turfs' : turf}
        # user = request.user
        return render(request, 'users/history.html')
    else:
        return redirect(usersignin)


def logout(request):
    if request.user.is_authenticated:
        user = request.user
        auth.logout(request)
        return redirect(home)
    else:
        return redirect(usersignin)
    




