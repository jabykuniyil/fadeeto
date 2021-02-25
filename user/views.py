from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User, auth
from . models  import userData, Turf, Booking, sportPrice, turfFacility, Category, Comment
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import ast
import json
import datetime
import requests
import random
import http.client
from django.conf import settings
from django.contrib import messages
import folium

def home(request):
    sport = Category.objects.all()
    turf = Turf.objects.filter(status='accept')
    sport_price = sportPrice.objects.all()
    context_ = {'sport' : sport_price, 'turfs' : turf, 'game' : sport}
    return render(request, 'users/home.html', context_)

def map(request, id):
    sport = sportPrice.objects.filter(category_id=id)
    turf_id_list = []
    for x in sport:
        turf_id_list.append(x.turf.id)
    turf = Turf.objects.filter(id__in=turf_id_list, status='accept')
    for x in turf:
        geolocator = Nominatim(user_agent='user')
        x.destination = geolocator.geocode(x.address)
        x.latitude = x.destination.latitude
        x.longitude = x.destination.longitude
    context = {'turf' : turf}
    return render(request, 'users/map.html', context)


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
    if request.method == 'POST':
        review = request.POST['review']
        user = request.user
        Comment.objects.create(comment=review, user=user)
        return redirect(home)
    else:
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


def phone(request):
    if request.user.is_authenticated:
        return redirect(home)
    else:
        if request.method == 'POST':
            phone = request.POST['phone']
            if userData.objects.filter(phone=phone).exists():
                request.session['phone'] = phone
                url = "https://d7networks.com/api/verifier/send"
                phone1 = '91'+str(phone)
                payload = {'mobile': phone1,
                'sender_id': 'SMSINFO',
                'message': 'Your Fadeeto verification code is {code}',
                'expiry': '900'} 
                files = [

                ]
                headers = {
                'Authorization': 'Token 0826e09c83c02826d9767d57fed74ead46c7660a'
                }

                response = requests.request("POST", url, headers=headers, data = payload, files = files)
                data = response.text.encode('utf8')
                dict=json.loads(data.decode('utf8'))
                otp_id = dict["otp_id"]
                request.session['otp_id']=otp_id
                print(request.session['otp_id'])
                print(response.text.encode('utf8'))
                return JsonResponse('true',safe=False)
            else:
                return JsonResponse('false',safe=False)
        else:
            return render(request, 'users/phone.html')
        

def otp(request):
    if request.user.is_authenticated:
        return redirect(home)
    else:
        if request.method == 'POST':
            phone = request.session['phone']
            url = "https://d7networks.com/api/verifier/verify"
            otp = request.POST['otp']
            print(otp)
            print(phone)
            userDat = userData.objects.get(phone=phone)
            user = User.objects.get(id=userDat.user_id)
            otp_id = request.session['otp_id']
            print(otp_id)
            payload = {'otp_id': otp_id , 'otp_code': otp}
            files = [

            ]
            headers = {
            'Authorization': 'Token 0826e09c83c02826d9767d57fed74ead46c7660a'
            }

            response = requests.request("POST", url, headers=headers, data = payload, files = files)
            
            print(response.text.encode('utf8'))
            data = response.text.encode('utf8')
            dict=json.loads(data.decode('utf8'))
            status = dict['status']
            if status == 'success':
                auth.login(request,user)
                return JsonResponse('true', safe=False)
            else:
                return JsonResponse('false', safe=False)
        else:
            if request.session.has_key('otp_id'):
                phone = request.session['phone']
                context = {'phone':phone}
                return render(request,'users/otp.html',context)
            else:
                return redirect(home)



def usersignup(request):
    if request.user.is_authenticated:
        return redirect(home)
    else:
        if request.method == 'POST':
            firstName = request.POST['firstName']
            phone = request.POST['mobile']
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password']
            # otp = str(random.randint(1000, 9999))            
            if User.objects.filter(email=email).exists():
                return JsonResponse('email', safe=False)
            elif User.objects.filter(username=username).exists():
                return JsonResponse('username', safe=False)
            elif userData.objects.filter(phone=phone).exists():
                return JsonResponse('mobile', safe=False)
            else:
                request.session['phone_signup'] = phone
                url = "https://d7networks.com/api/verifier/send"
                phone1 = '91'+str(phone)
                payload = {'mobile': phone1,
                'sender_id': 'SMSINFO',
                'message': 'Your Fadeeto verification code is {code}',
                'expiry': '900'} 
                files = [

                ]
                headers = {
                'Authorization': 'Token 0826e09c83c02826d9767d57fed74ead46c7660a'
                }

                response = requests.request("POST", url, headers=headers, data = payload, files = files)
                data = response.text.encode('utf8')
                dict=json.loads(data.decode('utf8'))
                otp_id = dict["otp_id"]
                request.session['otp_id_signup']=otp_id
                print(request.session['otp_id_signup'])
                print(response.text.encode('utf8'))
                user = User.objects.create_user(first_name=firstName, email=email, username=username, password=password)
                userData.objects.create(user=user, phone=phone)
                # send_otp(mobile, otp)
                # request.session['mobile'] = mobile
                return JsonResponse('true', safe=False)
        else:    
            return render(request, 'users/usersignup.html')


def otp_signin(request):
    if request.user.is_authenticated:
        return redirect(home)
    else:
        if request.method == 'POST':
            phone = request.session['phone_signup']
            url = "https://d7networks.com/api/verifier/verify"
            otp = request.POST['otp']
            print(otp)
            print(phone)
            userDat = userData.objects.get(phone=phone)
            user = User.objects.get(id=userDat.user_id)
            otp_id = request.session['otp_id_signup']
            print(otp_id)
            payload = {'otp_id': otp_id , 'otp_code': otp}
            files = [

            ]
            headers = {
            'Authorization': 'Token 0826e09c83c02826d9767d57fed74ead46c7660a'
            }

            response = requests.request("POST", url, headers=headers, data = payload, files = files)
            
            print(response.text.encode('utf8'))
            data = response.text.encode('utf8')
            dict=json.loads(data.decode('utf8'))
            status = dict['status']
            if status == 'success':
                auth.login(request,user)
                return JsonResponse('true', safe=False)
            else:
                return JsonResponse('false', safe=False)
        else:
            if request.session.has_key('otp_id_signup'):
                phone = request.session['phone_signup']
                context = {'phone':phone}
                return render(request,'users/otp-signin.html',context)
            else:
                return redirect(home)   


def profile(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = userData.objects.get(id = id)
            user.user.first_name = request.POST['name']
            user.user.email = request.POST['email']
            user.phone = request.POST['phone']
            if 'inputprofileimage' not in request.POST:
                image = request.FILES.get('inputprofileimage')
            else:
                image = user.photo
            user.photo = image
            user.save()
            return redirect(home)
        else:
            user = request.user
            userdata = userData.objects.get(user=user.id) 
            print( user)
            context = {'userdata' : userdata}
            return render(request, 'users/profile.html', context)
    else:
        return redirect(usersignin)




def user_history(request):
    if request.user.is_authenticated:
        user = request.user
        booking = Booking.objects.filter(user = user)
        context = {'booking' : booking}
        return render(request, 'users/bookhistory.html', context)
    else:
        return redirect(usersignin)



def userbooking(request, id):
    if request.user.is_authenticated:
        if request.method =='POST':
            print("Muth")
            name = request.POST['name']
            phone = request.POST['phone']
            email = request.POST['email']
            sport = request.POST['sport']
            date = request.POST['date']
            hour = request.POST['hour']
            payment_option = request.POST['payment']
            print(payment_option)
            turf = Turf.objects.get(id=id)
            sport_price = sportPrice.objects.filter(turf_id=turf.id)
            for x in sport_price:
                if x.category.sport == sport:
                    price = x.price
            print(type(price))
            user = request.user
            print(user)
            context = {'price' : price}
            sport = Category.objects.get(sport=sport)
            if Booking.objects.filter(date=date, turf_id = turf.id).exists() and Booking.objects.filter(hour=hour, turf_id = turf.id).exists() and Booking.objects.filter(turf_id = turf.id, status='pending').exists():
                return JsonResponse('exists', safe=False)
            if Booking.objects.filter(date=date, turf_id = turf.id).exists() and Booking.objects.filter(hour=hour, turf_id = turf.id).exists() and Booking.objects.filter(turf_id = turf.id, status='accept').exists():
                return JsonResponse('exists', safe=False)
            else:
                booking = Booking.objects.create(name=name, phone=phone, email=email, date=date, price=price, hour=hour, turf_id = id, sport=sport, user=user, exists=False, payment_option=payment_option)
                data = {'id': booking.id, 'price' : booking.price}
                return JsonResponse(data)
        else:
            user = request.user
            turf = Turf.objects.get(id=id)
            turf.timePeriod = ast.literal_eval(turf.timePeriod)
            userdata = userData.objects.get(user_id=user.id)
            sport_price = sportPrice.objects.filter(turf_id=turf.id)
            booking = Booking.objects.all()
            context = {'user' : user, 'turfs' : turf, 'userData' : userdata, 'sportprice' : sport_price, 'booking' : booking}
            return render(request, 'users/booking.html', context)
    else:
        return redirect(usersignin)


def bookHistory(request, id):
    if request.user.is_authenticated:
        booking = Booking.objects.get(id=id)
        price = sportPrice.objects.all()
        context = {'booking' : booking, 'price' : price}
        return render(request, 'users/history.html', context)
    else:
        return redirect(usersignin)


def logout(request):
    if request.user.is_authenticated:
        user = request.user
        auth.logout(request)
        return redirect(home)
    else:
        return redirect(usersignin)
    




