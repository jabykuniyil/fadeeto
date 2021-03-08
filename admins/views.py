from django.shortcuts import render, redirect
from django.http import JsonResponse
from . models import Category, Facilities
from django.core.files import File
from vendor.models import Vendor
from user.models import userData, Turf, turfFacility, sportPrice, Booking, Comment
from django.contrib.auth.models import User
from datetime import datetime, date
# Create your views here.


def adminsignin(request):
    if request.session.has_key('isAdmin'):
        return redirect(adminhome)
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            if username == 'admin' and password == 'admin':
                request.session['isAdmin'] = True
                return JsonResponse('true', safe=False)
            else:
                return JsonResponse('false', safe=False)
        else:
            return render(request, 'admin/login.html')


def adminhome(request):
    if request.session.has_key('isAdmin'):
        user = User.objects.all().count()
        vendor = Vendor.objects.all().count()
        turf = Turf.objects.all().count()
        booking = Booking.objects.all().count()
        y_1 = datetime.now().year
        y_2 = y_1 - 1
        y_3 = y_1 - 2
        y_4 = y_1 - 3
        y_5 = y_1 - 4
        book_y1 = Booking.objects.filter(date__year=y_1).count()
        book_y2 = Booking.objects.filter(date__year=y_2).count()
        book_y3 = Booking.objects.filter(date__year=y_3).count()
        book_y4 = Booking.objects.filter(date__year=y_4).count()
        book_y5 = Booking.objects.filter(date__year=y_5).count()
        turfs = Turf.objects.all()
        category = Category.objects.all()
        facilities = Facilities.objects.all()
        comment = Comment.objects.all().count()
        price = 0
        amount = Booking.objects.all()
        for x in amount:
            price = price + x.price
        month = datetime.now().month
        this_month_price = 0
        price_month = Booking.objects.filter(date__month=month, status='accept')
        for x in price_month:
            this_month_price = this_month_price + x.price
        turf_accept = Turf.objects.filter(status='accept').count()
        turf_pending = Turf.objects.filter(status='pending').count()
        context = {'book_y1' : book_y1, 'book_y2' : book_y2, 'book_y3' : book_y3, 'book_y4' : book_y4, 'book_y5' : book_y5, 'y_1' : y_1, 'y_2' : y_2, 'y_3' : y_3, 'y_4' : y_4, 'users' : user, 'vendors' : vendor, 'turfs' : turf, 'bookings' : booking, 'turf' : turfs, 'category' : category, 'facilities' : facilities, 'comment' : comment, 'price' : price, 'this_month_price' : this_month_price, 'turf_accept' : turf_accept, 'turf_pending' : turf_pending}
        return render(request, 'admin/home.html', context)
    else:
        return redirect(adminsignin)


def users(request):
    if request.session.has_key('isAdmin'):
        userdata = userData.objects.all()
        return render(request, 'admin/users.html', {"userdata" : userdata})
    else:
        return redirect(adminsignin)


def vendors(request):
    if request.session.has_key('isAdmin'):
        vendor = Vendor.objects.all()
        return render(request, 'admin/vendors.html', {'vendor' : vendor})
    else:
        return redirect(adminsignin)


def turfs(request):
    if request.session.has_key('isAdmin'):
        turf = Turf.objects.filter(status='accept')
        turffacility = turfFacility.objects.all()
        sport_price = sportPrice.objects.all()
        return render(request, 'admin/turfs.html', {'turfs' : turf, 'turffacility' : turffacility, 'sportprice' : sport_price})
    else:
        return redirect(adminsignin)
    
    
def accept_turf(request, id):
    if request.session.has_key('isAdmin'):
        turf = Turf.objects.get(id=id)
        if turf.status == 'pending':
            turf.status = 'accept'
        else:
            turf.status = 'pending'
        turf.save()
        return redirect(turf_requests)
    else:
        return redirect(adminsignin)
    
    
def reject_turf(request, id):
    if request.session.has_key('isAdmin'):
        turf = Turf.objects.get(id=id)
        turf.delete()
        return redirect(turf_requests)
    else:
        return redirect(adminsignin)
    

def facilities(request):
    if request.session.has_key('isAdmin'):
        facility = Facilities.objects.all()
        return render(request, 'admin/facilities.html', {'facilities' : facility})
    else:
        return redirect(adminsignin)


def category(request):
    if request.session.has_key('isAdmin'):
        category = Category.objects.all()
        return render(request, 'admin/category.html', { 'categories' : category})
    else:
        return redirect(adminsignin)


def addFacilities(request):
    if request.session.has_key('isAdmin'):
        if request.method=='POST':
            facility = request.POST['facility']
            Facilities.objects.create(facility=facility)
            return redirect(facilities)
        else:
            return render(request, 'admin/addfacility.html')
    else:
        return redirect(adminsignin)



def addCategory(request):
    if request.session.has_key('isAdmin'):
        if request.method=='POST':
            category1 = request.POST['category']
            icon = request.FILES.get('icon')
            Category.objects.create(sport=category1, icon=icon)
            return redirect(category)
        else: 
            return render(request, 'admin/addcategory.html')
    else:
        return redirect(adminsignin)
    
    
def editFacilities(request, id):
    if request.session.has_key('isAdmin'):
        if request.method=='POST':
            facilities = Facilities.objects.get(id=id)
            facilities.facility = request.POST['facility']
            facilities.save()
            return redirect('facilities')
        else:
            facilities = Facilities.objects.get(id=id)
            return render(request, 'admin/editfacility.html', {'facilities' : facilities})
    
    
def editCategory(request, id):
    if request.session.has_key('isAdmin'):
        if request.method == 'POST':
            category_sport = Category.objects.get(id=id)
            category_sport.sport = request.POST['category']
            if 'iconfile' not in request.POST:
                icon = request.FILES.get('iconfile')
            else:
                icon = category_sport.icon
            category_sport.icon = icon
            category_sport.save()
            return redirect(category)
        else:
            categories = Category.objects.get(id=id)
            return render(request, 'admin/editcategory.html', {'category' : categories})
    else:
        return redirect(adminsignin)
    
    
def deleteFacility(request, id):
    if request.session.has_key('isAdmin'):
        Facilities.objects.get(id=id).delete()
        return redirect('facilities')
    else:
        return redirect(adminsignin)
    
    
def deleteCategory(request, id):
    if request.session.has_key('isAdmin'):
        Category.objects.get(id=id).delete()
        return redirect(category)
    else:
        return redirect(adminsignin)
    


def block_user(request, id):
    if request.session.has_key('isAdmin'):
        user = User.objects.get(id=id)
        if user.is_active == True:
            user.is_active = False 
        else:
            user.is_active = True
        user.save()
        return redirect(users)
    else:
        return redirect(adminsignin)
    


def block_vendor(request, id):
    if request.session.has_key('isAdmin'):
        vendor = Vendor.objects.get(id=id)
        if vendor.is_active == True:
            vendor.is_active = False
        else:
            vendor.is_active = True
        vendor.save()
        return redirect(vendors)
    else:
        return redirect(adminsignin)
        
       
       
def block_turf(request, id):
    if request.session.has_key('isAdmin'):
        turf = Turf.objects.get(id=id)
        if turf.is_active == True:
            turf.is_active = False
        else:
            turf.is_active = True
        turf.save()
        if turf.status == 'accept':
            turf.status = 'Blocked'
        else:
            turf.status = 'accept'
        turf.save()
        return redirect(turfs)
    else:
        return redirect(adminsignin)



def blocked_turfs(request):
    if request.session.has_key('isAdmin'):
        status = Turf.objects.filter(status='Blocked')
        for x in status:
            x.is_active = False
            x.save()
        context = {'turfs' : status}
        return render(request, 'admin/blocked-turfs.html', context)
    else:
        return redirect(adminsignin)


def turf_requests(request):
    if request.session.has_key('isAdmin'):
        status = Turf.objects.filter(status='pending')
        context = {'turf' : status}
        return render(request, 'admin/turfrequests.html', context)
    else:
        return redirect(adminsignin)



def bookingSummary(request):
    if request.session.has_key('isAdmin'):
        booking = Booking.objects.all()
        return render(request, 'admin/bookingsummary.html', {'booking' : booking})
    else:
        return redirect(adminsignin)


def reviews(request):
    if request.session.has_key('isAdmin'):
        turf = Turf.objects.filter(status='accept')
        context = {'turf' : turf}
        return render(request, 'admin/reviews.html', context)
    else:
        return redirect(adminsignin)

        

def reviewspecific(request, id):
    if request.session.has_key('isAdmin'):
        turf = Turf.objects.get(id=id)
        comment = Comment.objects.filter(turf=turf)
        context = {'turf' : turf, 'comment' : comment}
        return render(request, 'admin/reviewspecific.html', context)
    else:
        return redirect(adminsignin)


def logout(request):
    if request.session.has_key('isAdmin'):
        request.session.flush()
        return redirect(adminsignin)
    else:
        return redirect(adminsignin)

