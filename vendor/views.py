from django.shortcuts import render, redirect
from user.models import userData, Turf
from django.contrib.auth.models import  User
from django.http import JsonResponse
from . models import Vendor
from django.contrib.auth.hashers import make_password, check_password
from django.core.files import File
import json
from admins.models import Category, Facilities
# from .. import app
# from django.contrib.auth import login
# Create your views here.


def signin(request):
    if request.session.has_key('isVendor'):
        return redirect(home)
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            vendor = Vendor.objects.filter(username=username).first()
            if vendor is not None and check_password(password, vendor.password):
                request.session['isVendor'] = True
                # login(request, vendor)
                return JsonResponse('true', safe=False)
            else:
                return JsonResponse('false', safe=False)
        else:
            return render(request, 'vendors/login.html')


def signup(request):
    if request.session.has_key('isVendor'):
        if request.method == 'POST':
            name = request.POST['first_name']
            mobile = request.POST['mobile']
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password']
            if Vendor.objects.filter(email=email).exists():
                return JsonResponse('email', safe=False)
            elif Vendor.objects.filter(username=username).exists():
                return JsonResponse('username', safe=False)
            else:
                Vendor.objects.create(name=name, mobile=mobile, email=email, username=username, password=make_password(password))
                return JsonResponse('true', safe=False)
        else:
            return render(request, 'vendors/signup.html')
    else:
        return redirect(signin)


def home(request):
    if request.session.has_key('isVendor'):
        return render(request, 'vendors/home.html')
    else:
        return redirect(signin)


def bookHistory(request):
    if request.session.has_key('isVendor'):
        return render(request, 'vendors/bookhistory.html')
    else:
        return redirect(signin)


def turfs(request):
    if request.session.has_key('isVendor'):
        turf = Turf.objects.all()
        return render(request, 'vendors/turfs.html', {'turfs' : turf})
    else:
        return redirect(signin)


def editTurf(request,id):
    if request.method == 'POST':
        turf = Turf.objects.get(id=id)
        turf.turfName = request.POST['turfName']
        turf.turfName.capitalize()
        print(request)
        if 'inputimage1' not in request.POST:
            image1 = request.FILES.get('inputimage1')
        else:
            image1 = turf.image1
        turf.image1 = image1
        print(image1)
        if 'inputimage2' not in request.POST:
            image2 = request.FILES.get('inputimage2')
        else:
            image2 = turf.image2
        turf.image2 = image2
        cricket = request.POST.getlist('cricket')
        cricketprice = request.POST['cricketprice']
        football = request.POST.getlist('football')
        footballprice = request.POST['footballprice']
        badminton = request.POST.getlist('badminton')
        badmintonprice = request.POST['badmintonprice']
        am67 = request.POST.getlist('6AM-7AM')
        am78 = request.POST.getlist('7AM-8AM')
        am89 = request.POST.getlist('8AM-9AM')
        am910 = request.POST.getlist('9AM-10AM')
        am1011  = request.POST.getlist('10AM-11AM')
        am1112 = request.POST.getlist('11AM-12AM')
        am121 = request.POST.getlist('12AM-1PM')
        pm12 = request.POST.getlist('1PM-2PM')
        pm23 = request.POST.getlist('2PM-3PM')
        pm34 = request.POST.getlist('3PM-4PM')
        pm45 = request.POST.getlist('4PM-5PM')
        pm56 = request.POST.getlist('5PM-6PM')
        pm67 = request.POST.getlist('6PM-7PM')
        pm78 = request.POST.getlist('7PM-8PM')
        pm89 = request.POST.getlist('8PM-9PM')
        pm910 = request.POST.getlist('9PM-10PM')
        pm1011 = request.POST.getlist('10PM-11PM')
        pm1112 = request.POST.getlist('11PM-12PM')
        bath = request.POST.getlist('bath')
        purifiedWater = request.POST.getlist('purifiedwater')
        washRoom = request.POST.getlist('washroom')
        shower = request.POST.getlist('shower')
        parking = request.POST.getlist('parking')
        gallery = request.POST.getlist('gallery')
        cafteria = request.POST.getlist('cafteria')
        liveScreening = request.POST.getlist('livescreening')
        locker = request.POST.getlist('locker')
        mobileCharging = request.POST.getlist('mobilecharging')
        address = request.POST['address']
        description = request.POST['description']
        timePeriod = am67 + am78 + am89 + am910 + am1011 + am1112 + am121 + pm12 + pm23 + pm34 + pm45 + pm56 + pm67 + pm78 + pm89 + pm910 + pm1011 + pm1112
        turf.timePeriod = timePeriod
        facilities = bath + purifiedWater + washRoom + shower + parking + gallery + cafteria + liveScreening + locker + mobileCharging 
        turf.facilities = facilities
        turf.sport = {}
        if len(cricket) != 0:
            turf.sport[cricket[0]] = int(cricketprice)
        if len(football) != 0:
            turf.sport[football[0]] = int(footballprice)
        if len(badminton) != 0:
            turf.sport[badminton[0]] = int(badmintonprice)
        turf.sport = json.dumps(turf.sport)
        # turf = Turf.objects.filter(turfName=turfName, address=address, description=description, timePeriod=timePeriod, facilities=facilities, sport=sport, image1=image1, image2=image2)
        print(image1,image2)
        turf.save()
        print(turf.turfName)
        return redirect(turfs)
    else:
        turf = Turf.objects.get(id=id)
        turf.sport = json.loads(turf.sport)
        footballprice = turf.sport.get('football')
        cricketprice = turf.sport.get('cricket')
        badmintonprice = turf.sport.get('badminton')
        print(footballprice, cricketprice)
        return render(request, 'vendors/editturf.html', {'turfs' : turf, 'football' : footballprice, 'cricket' : cricketprice, 'badminton' : badmintonprice} )
    
        
def addTurf(request):
    if request.session.has_key('isVendor'):
        if request.method == 'POST':
            turfName = request.POST['turfName']
            turfName.capitalize()
            image1 = request.FILES.get('image1')
            image2 = request.FILES.get('image2')
            cricket = request.POST.getlist('cricket')
            cricketprice = request.POST['cricketprice']
            football = request.POST.getlist('football')
            footballprice = request.POST['footballprice']
            badminton = request.POST.getlist('badminton')
            badmintonprice = request.POST['badmintonprice']
            am67 = request.POST.getlist('6AM-7AM')
            am78 = request.POST.getlist('7AM-8AM')
            am89 = request.POST.getlist('8AM-9AM')
            am910 = request.POST.getlist('9AM-10AM')
            am1011  = request.POST.getlist('10AM-11AM')
            am1112 = request.POST.getlist('11AM-12AM')
            am121 = request.POST.getlist('12AM-1PM')
            pm12 = request.POST.getlist('1PM-2PM')
            pm23 = request.POST.getlist('2PM-3PM')
            pm34 = request.POST.getlist('3PM-4PM')
            pm45 = request.POST.getlist('4PM-5PM')
            pm56 = request.POST.getlist('5PM-6PM')
            pm67 = request.POST.getlist('6PM-7PM')
            pm78 = request.POST.getlist('7PM-8PM')
            pm89 = request.POST.getlist('8PM-9PM')
            pm910 = request.POST.getlist('9PM-10PM')
            pm1011 = request.POST.getlist('10PM-11PM')
            pm1112 = request.POST.getlist('11PM-12PM')
            bath = request.POST.getlist('bath')
            purifiedWater = request.POST.getlist('purifiedwater')
            washRoom = request.POST.getlist('washroom')
            shower = request.POST.getlist('shower')
            parking = request.POST.getlist('parking')
            gallery = request.POST.getlist('gallery')
            cafteria = request.POST.getlist('cafteria')
            liveScreening = request.POST.getlist('livescreening')
            locker = request.POST.getlist('locker')
            mobileCharging = request.POST.getlist('mobilecharging')
            address = request.POST['address']
            description = request.POST['description']
            sport = {}
            if len(cricket) !=0:
                sport[cricket[0]] = int(cricketprice)
            if len(football) !=0:
                sport[football[0]] = int(footballprice)
            if len(badminton) !=0:
                sport[badminton[0]] = int(badmintonprice)
            sport = json.dumps(sport)
            # print(sport)
            # if 'image1' not in request.POST:
            #     image1 = request.FILES.get('image1')
            # else:
            #     image1 = 
            timePeriod = am67 + am78 + am89 + am910 + am1011 + am1112 + am121 + pm12 + pm23 + pm34 + pm45 + pm56 + pm67 + pm78 + pm89 + pm910 + pm1011 + pm1112
            facilities = bath + purifiedWater + washRoom + shower + parking + gallery + cafteria + liveScreening + locker + mobileCharging 
            Turf.objects.create(turfName=turfName, sport=sport, 
                                timePeriod=timePeriod, image1=image1, image2=image2,
                                address=address, description=description, facilities=facilities)
            
            return redirect(turfs)
        else:
            sport = Category.objects.all()
            facility = Facilities.objects.all()
            print('hello')
            return render(request, 'vendors/addturf.html', {'sports' : sport, 'facilities' : facility})
    else:
        return redirect(signin) 
    
    
def deleteTurf(request, id):
    if request.session.has_key('isVendor'):
        turf = Turf.objects.get(id=id)
        turf.delete()
        return redirect(turfs)
    else:
        return redirect(signin)


def logout(request):
    if request.session.has_key('isVendor'):
        request.session.flush()
        return redirect(signin)
    else:
        return redirect(signin)
    
# @app.template_filter()
# def key(d, key_name):
#     return d[key_name]
# key = register.filter('key', key)