from django.shortcuts import render, redirect
from user.models import userData, Turf, sportPrice, turfFacility, Booking
from django.contrib.auth.models import  User
from django.http import JsonResponse
from . models import Vendor
from django.contrib.auth.hashers import make_password, check_password
from django.core.files import File
import json, ast
from admins.models import Category, Facilities
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


def signin(request):
    if request.session.has_key('isVendor'):
        return redirect(home)
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            vendor = Vendor.objects.filter(username=username).first()
            if vendor is not None and check_password(password, vendor.password):
                if vendor.is_active == True:
                    request.session['isVendor'] = True
                    request.session['vendor_id'] = vendor.id
                    return JsonResponse('true', safe=False)
                else:
                    return JsonResponse('false', safe=False)
            else:
                return JsonResponse('false', safe=False)
            
        else:
            print('hello')
            return render(request, 'vendors/login.html')


def signup(request):
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
            Vendor.objects.create(name=name, mobile=mobile, email=email, username=username, password=make_password(password), is_active=True)
            return JsonResponse('true', safe=False)
    else:
        return render(request, 'vendors/signup.html')

   

def home(request):
    if request.session.has_key('isVendor'):
        # sport_price = sportPrice.objects.all()
        return render(request, 'vendors/home.html')
    else:
        return redirect(signin)


def bookHistory(request):
    if request.session.has_key('isVendor'):
        vendor_id = request.session['vendor_id']
        booking = Booking.objects.filter(turf__vendor__id = vendor_id)
        context = {'booking' : booking}
        return render(request, 'vendors/bookhistory.html', context)
    else:
        return redirect(signin)



def turfs(request):
    if request.session.has_key('isVendor'):
        vendor_id = request.session['vendor_id']
        turf = Turf.objects.filter(vendor_id=vendor_id)
        sport_price = sportPrice.objects.all()
        turf_facility = turfFacility.objects.all()
        return render(request, 'vendors/turfs.html', {'turfs' : turf, 'sportprice' : sport_price, 'turffacility' : turf_facility})
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
        turf.latitude = request.POST['lat']
        turf.longitude = request.POST['lng']
        geolocator = Nominatim(user_agent='vendor')
        turf.address = geolocator.reverse(turf.latitude+","+turf.longitude) 
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
        turf.description = request.POST['description']
        timePeriod = am67 + am78 + am89 + am910 + am1011 + am1112 + am121 + pm12 + pm23 + pm34 + pm45 + pm56 + pm67 + pm78 + pm89 + pm910 + pm1011 + pm1112
        turf.timePeriod = timePeriod
        facily = turfFacility.objects.filter(turf=turf.id)
        facily.delete()
        facility = request.POST.getlist('facility')
        spopri = sportPrice.objects.filter(turf=id)
        spopri.delete()
        sport_category = request.POST.getlist('category')
        for x in facility:
            turfFacility.objects.create(facilities_id=x, turf_id=turf.id)
        for x in sport_category:
            name = x+'-price'
            sport_price = request.POST.get(name)
            sportPrice.objects.create(category_id=x, turf_id=turf.id, price=sport_price)
        turf.save()
        return redirect(turfs)
    else:
        turf_facility_list = []
        sportprice_list = []
        turf = Turf.objects.get(id=id)
        facility = Facilities.objects.all()
        sport = Category.objects.all()
        turf_facility = turfFacility.objects.filter(turf_id=turf.id)
        for x in turf_facility:
            turf_facility_list.append(x.facilities.facility)
        sport_price = sportPrice.objects.filter(turf_id=turf.id)
        for x in sport_price:
            sportprice_list.append(x.category.sport)
        print(turf.longitude)
        return render(request, 'vendors/editturf.html', {'turfs' : turf, 'turffacilitylist' : turf_facility_list, 'facility' : facility, 'sportpricelist' : sportprice_list, 'sportprice' : sport_price, 'sport' : sport} )


   
        
def addTurf(request):
    if request.session.has_key('isVendor'):
        if request.method == 'POST':
            vendor_id = request.session['vendor_id']
            turfName = request.POST['turfName']
            turfName.capitalize()
            lat = request.POST['lat']
            lng = request.POST['lng']
            geolocator = Nominatim(user_agent='vendor')
            Latitude = lat
            Longitude = lng
            
            location = geolocator.reverse(Latitude+","+Longitude) 
            
            # Display 
            image1 = request.FILES.get('image1')
            image2 = request.FILES.get('image2')
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
            facility = request.POST.getlist('facility')
            # address = request.POST['address']
            description = request.POST['description']
            timePeriod = am67 + am78 + am89 + am910 + am1011 + am1112 + am121 + pm12 + pm23 + pm34 + pm45 + pm56 + pm67 + pm78 + pm89 + pm910 + pm1011 + pm1112
            turf = Turf.objects.create(turfName=turfName, 
                                timePeriod=timePeriod, image1=image1, image2=image2,
                                address=location, description=description, is_active=True,vendor_id=vendor_id, status='pending', latitude=lat, longitude=lng)
            category = request.POST.getlist('category')            
            for categories in category:
                name=categories+'-price'
                sport_price = request.POST.get(name)
                sportPrice.objects.create(category_id=categories, turf_id = turf.id, price =sport_price)
            for facilities in facility:
                turfFacility.objects.create(facilities_id=facilities, turf_id=turf.id)
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
    
    
def book_specific(request):
    if request.session.has_key('isVendor'):
        vendor_id = request.session['vendor_id']
        turf = Turf.objects.filter(vendor_id=vendor_id, status='accept')
        context = {'turf' : turf}
        return render(request, 'vendors/bookspecific.html', context)
    else:
        return redirect(signin)


def accept_booking(request, id):
    if request.session.has_key('isVendor'):
        booking = Booking.objects.get(id=id)
        if booking.status == 'pending':
            booking.status = 'accept'
        else:
            booking.status = 'pending'
        booking.save()
        return redirect(bookHistory)
    else:
        return redirect(signin)


def reject_booking(request, id):
    if request.session.has_key('isVendor'):
        booking = Booking.objects.get(id=id)
        if booking.status == 'pending':
            booking.status = 'Rejected'
        else:
            booking.status = 'pending'
        booking.save()
        return redirect(book_requests)
    else:
        return redirect(signin)
   
    
def vendor_booking(request, id):
    if request.session.has_key('isVendor'):
        if request.method =='POST':
            name = request.POST['name']
            phone = request.POST['phone']
            email = request.POST['email']
            sport = request.POST['sport']
            date = request.POST['date']
            hour = request.POST['hour']
            turf = Turf.objects.get(id=id)
            sport_price = sportPrice.objects.filter(turf_id=turf.id)
            print(turf.id)
            for x in sport_price:
                if x.category.sport == sport:
                    price = x.price
            print(price)
            sport = Category.objects.get(sport=sport)
            if Booking.objects.filter(date=date, turf_id = turf.id) and Booking.objects.filter(hour=hour, turf_id = turf.id).exists() and Booking.objects.filter(status='accept', turf_id = turf.id).exists() :
                return JsonResponse('exists', safe=False)
            elif Booking.objects.filter(date=date, turf_id = turf.id) and Booking.objects.filter(hour=hour, turf_id = turf.id).exists() and Booking.objects.filter(status='pending', turf_id = turf.id).exists() :
                return JsonResponse('exists', safe=False)
            else:
                booking = Booking.objects.create(name=name, phone=phone, email=email, date=date, price=price, hour=hour, turf_id = id, sport=sport, exists=False, status='accept', type_of_booking = 'vendor side')
                data = {'id': booking.id}
                # print(data.id)
                return JsonResponse(data)
        else:
            turf = Turf.objects.get(id=id, status='accept')
            print(turf)
            turf.timePeriod = ast.literal_eval(turf.timePeriod)
            sport_price = sportPrice.objects.filter(turf_id = turf.id)
            context = {'turf' : turf, 'sport' : sport_price}
            return render(request, 'vendors/vendorbooking.html', context)
    else:
        return redirect(signin)
    

def book_summary(request, id):
    if request.session.has_key('isVendor'):
        booking = Booking.objects.get(id=id)
        price = sportPrice.objects.all()
        context = {'booking' : booking, 'price' : price}
        return render(request, 'users/history.html', context)
    else:
        return redirect(signin)


def book_requests(request):
    if request.session.has_key('isVendor'):
        vendor_id = request.session['vendor_id']
        booking = Booking.objects.filter(turf__vendor__id = vendor_id, status='pending')
        context = {'booking' : booking}
        return render(request, 'vendors/booking-requests.html', context)
    else:
        return redirect(signin)


def logout(request):
    if request.session.has_key('isVendor'):
        request.session.flush()
        return redirect(signin)
    else:
        return redirect(signin)

def index(request):
    return render(request, 'vendors/index.html')
  
# @app.template_filter()
# def key(d, key_name):
#     return d[key_name]
# key = register.filter('key', key)