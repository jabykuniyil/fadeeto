from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User, auth
from . models  import userData, Turf, Booking, sportPrice, turfFacility, Category, Comment, Coupon, UsedCoupons
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import ast
import json
from datetime import datetime, date
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
    turf = Turf.objects.filter(id__in=turf_id_list)
    context = {'turf' : turf}
    return render(request, 'users/category.html', context)



def turfview(request, id):
    turf = Turf.objects.get(id=id)
    user = User.objects.all()
    user_data = userData.objects.filter(user=user)
    comment = Comment.objects.filter(turf=turf)
    sport_price = sportPrice.objects.filter(turf_id=turf.id )
    facility = turfFacility.objects.filter(turf_id=turf.id)
    turf.timePeriod = ast.literal_eval(turf.timePeriod)
    return render(request, 'users/turf.html', {'turf' : turf,   'sportprice' : sport_price, 'facility' : facility, 'comment' : comment})


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
            userDat = userData.objects.get(phone=phone)
            user = User.objects.get(id=userDat.user_id)
            otp_id = request.session['otp_id']
            payload = {'otp_id': otp_id , 'otp_code': otp}
            files = [

            ]
            headers = {
            'Authorization': 'Token 0826e09c83c02826d9767d57fed74ead46c7660a'
            }

            response = requests.request("POST", url, headers=headers, data = payload, files = files)
            
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
            if User.objects.filter(email=email).exists():
                return JsonResponse('email', safe=False)
            elif User.objects.filter(username=username).exists():
                return JsonResponse('username', safe=False)
            elif userData.objects.filter(phone=phone).exists():
                return JsonResponse('mobile', safe=False)
            else:
                # request.session['phone_signup'] = phone
                # url = "https://d7networks.com/api/verifier/send"
                # phone1 = '91'+str(phone)
                # payload = {'mobile': phone1,
                # 'sender_id': 'SMSINFO',
                # 'message': 'Your Fadeeto verification code is {code}',
                # 'expiry': '900'} 
                # files = [

                # ]
                # headers = {
                # 'Authorization': 'Token 0826e09c83c02826d9767d57fed74ead46c7660a'
                # }

                # response = requests.request("POST", url, headers=headers, data = payload, files = files)
                # data = response.text.encode('utf8')
                # dict=json.loads(data.decode('utf8'))
                # otp_id = dict["otp_id"]
                # request.session['otp_id_signup']=otp_id
                user = User.objects.create_user(first_name=firstName, email=email, username=username, password=password)
                userData.objects.create(user=user, phone=phone)
                return JsonResponse('true', safe=False)
        else:    
            return render(request, 'users/usersignup.html')


# def otp_signin(request):
#     if request.user.is_authenticated:
#         return redirect(home)
#     else:
#         if request.method == 'POST':
#             phone = request.session['phone_signup']
#             url = "https://d7networks.com/api/verifier/verify"
#             otp = request.POST['otp']
#             userDat = userData.objects.get(phone=phone)
#             user = User.objects.get(id=userDat.user_id)
#             otp_id = request.session['otp_id_signup']
#             payload = {'otp_id': otp_id , 'otp_code': otp}
#             files = [

#             ]
#             headers = {
#             'Authorization': 'Token 0826e09c83c02826d9767d57fed74ead46c7660a'
#             }

#             response = requests.request("POST", url, headers=headers, data = payload, files = files)
            
#             data = response.text.encode('utf8')
#             dict=json.loads(data.decode('utf8'))
#             status = dict['status']
#             if status == 'success':
#                 auth.login(request,user)
#                 return JsonResponse('true', safe=False)
#             else:
#                 return JsonResponse('false', safe=False)
#         else:
#             if request.session.has_key('otp_id_signup'):
#                 phone = request.session['phone_signup']
#                 context = {'phone':phone}
#                 return render(request,'users/otp-signin.html',context)
#             else:
#                 return redirect(home)   


def profile(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = userData.objects.get(id = id)
            user1 = User.objects.get(id=user.user.id)
            user1.first_name = request.POST['name']
            user1.email = request.POST['email']
            user.phone = request.POST['phone']
            if 'inputprofileimage' not in request.POST:
                image = request.FILES.get('inputprofileimage')
            else:
                image = user.photo
            user.photo = image
            user1.save()
            user.save()
            return redirect(home)
        else:
            user = request.user
            userdata = userData.objects.get(user=user.id) 
            current_date = date.today()
            if Coupon.objects.exists():
                coupon = Coupon.objects.filter(start_date__lt=current_date, end_date__gt=current_date) 
                context = {'userdata' : userdata, 'coupon' : coupon}
                return render(request, 'users/profile.html', context)
            else:
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
            name = request.POST['name']
            phone = request.POST['phone']
            email = request.POST['email']
            sport = request.POST['sport']
            date_ = request.POST['date']
            hour = request.POST['hour']
            coupon = request.POST['coupon']
            user = request.user
            userdata = userData.objects.get(user=user) 
            turf = Turf.objects.get(id=id)
            sport_price = sportPrice.objects.filter(turf_id=turf.id)
            for x in sport_price:
                if x.category.sport == sport:
                    price = x.price  
            current_date = date.today()
            if Coupon.objects.filter(coupon_code=coupon, turf_id=id, start_date__lte=current_date, end_date__gt=current_date).exists() and not UsedCoupons.objects.filter(user = user, coupon__coupon_code=coupon).exists():
                coupon_discount = Coupon.objects.get(coupon_code=coupon, turf_id=turf.id, start_date__lte=current_date, end_date__gt=current_date)
                discount = coupon_discount.discount
                discounted_amount = (price * discount)/100
                amount_after_discount = price - discounted_amount
                razorpay_amount = amount_after_discount * 100
                paypal_amount = amount_after_discount / 70
                context = {'name' : name, 'phone' : phone, 'coupon' : coupon_discount.coupon_code, 'sport' : sport,  'email' : email, 'date' : date_, 'hour' : hour, 'amount' : amount_after_discount, 'razorpay_amount' : razorpay_amount, 'paypal_amount' : paypal_amount, 'turf_id' : id, 'user_id' : user.id, 
                'userdata_id' : userdata.id}             
                request.session['context'] = json.dumps(context)
                return JsonResponse('true', safe=False)
            else:
                amount_after_discount = price
                razorpay_amount = amount_after_discount * 100
                paypal_amount = amount_after_discount / 70
                context = {'name' : name, 'phone' : phone, 'email' : email, 'sport' : sport, 'date' : date_, 'hour' : hour, 'amount' : amount_after_discount, 'razorpay_amount' : razorpay_amount, 'paypal_amount' : paypal_amount, 'turf_id' : id}             
                request.session['context'] = json.dumps(context)
                return JsonResponse('true', safe=False)
        else:
            user = request.user
            turf = Turf.objects.get(id=id)
            turf.timePeriod = ast.literal_eval(turf.timePeriod)
            userdata = userData.objects.get(user_id=user.id)
            sport_price = sportPrice.objects.filter(turf_id=turf.id)
            booking = Booking.objects.all()
            available = Booking.objects.filter(status='accept', turf_id=turf.id) and Booking.objects.filter(status='pending', turf_id=turf.id)
            booked = {}
            for x in available:
                if x.date in booked.keys():
                    booked[x.date].append(x.hour)
                else:
                    booked[x.date] = [x.hour]
            coupon = Coupon.objects.all()
            context = {'user' : user, 'turfs' : turf, 'available' : available, 'userData' : userdata, 'sportprice' : sport_price, 'booking' : booking, 'coupon' : coupon}
            return render(request, 'users/booking.html', context)
    else:
        return redirect(usersignin)
    
def summary(request):
    if request.user.is_authenticated:
        if request.method =='POST':
            payment_option = request.POST['payment']
            data = request.session['context']
            context = json.loads(data)
            user = request.user
            user_data = userData.objects.get(user=user)
            if 'coupon' in context:
                coupon = Coupon.objects.get(coupon_code=context['coupon'])
                UsedCoupons.objects.create(user=user, coupon=coupon)
            Booking.objects.create(payment_option=payment_option, user_data_id=user_data.id, user_id=user.id, game=context['sport'],   turf_id= context['turf_id'], type_of_booking = 'user side', name= context['name'], phone= context['phone'], email= context['email'], date= context['date'], hour= context['hour'], price= context['amount'], status='accept')
            request.session['context'] = ''
            return JsonResponse('true', safe=False)
        else:
            if request.session['context'] != '':
                data = request.session['context']
                context = json.loads(data)
                return render(request,'users/summary.html', context)
            else:
                return redirect(home)
    else:
        return redirect(home)

def coupon_selected(request, id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            coupon = request.GET['coupon']
            sport = request.GET['sport']
            turf = Turf.objects.get(id=id)
            today = date.today()
            user = request.user
            sport_price = sportPrice.objects.filter(turf_id=turf.id)
            for x in sport_price:
                if x.category.sport == sport:
                    price = x.price
            if Coupon.objects.filter(coupon_code=coupon, turf_id=turf.id).exists():
                coupon_discount = Coupon.objects.get(coupon_code=coupon, turf_id=turf.id)
                if coupon_discount.start_date <= today and coupon_discount.end_date > today :
                    if not UsedCoupons.objects.filter(user=user, coupon=coupon_discount):
                        discount = coupon_discount.discount
                        discounted_amount = (price * discount)/100
                        amount_after_discount = price - discounted_amount
                        context = {'amount_after_discount' : amount_after_discount, 'discount' : discounted_amount}
                        return JsonResponse(context)
                    else:
                        return JsonResponse('used', safe=False)
                else:
                    return JsonResponse('expired', safe=False)
            else:
                return JsonResponse('false', safe=False)   
    else:
        return redirect(home)

def customer_review(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            review = request.POST['review']
            user = request.user
            user_data = userData.objects.get(user=user)
            turf = Turf.objects.get(id=id)
            Comment.objects.create(comment=review, turf_id=turf.id, userDetails_id=user_data.id, user=user)
            return JsonResponse('true', safe=False)
        else:
            return redirect(home)
    else:
        return redirect(home)


def time_slots(request, id):
    date = request.GET['date_selected']
    booking = Booking.objects.filter(date=date, turf_id=id, status__in=['accept', 'pending'])
    used_hours = []
    for x in booking:
        used_hours.append(x.hour)
    return JsonResponse({'used_hours':used_hours})


def logout(request):
    if request.user.is_authenticated:
        user = request.user
        auth.logout(request)
        return redirect(home)
    else:
        return redirect(usersignin)

