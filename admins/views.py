from django.shortcuts import render, redirect
from django.http import JsonResponse
from . models import Category, Facilities
from django.core.files import File
from vendor.models import Vendor
from user.models import userData, Turf, turfFacility, sportPrice, Booking
from django.contrib.auth.models import User

# Create your views here.


def adminsignin(request):
    if request.session.has_key('isAdmin'):
        return redirect(adminhome)
    else:
        if request.method == 'POST':
            print('hellooo')
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
        return render(request, 'admin/home.html')
    else:
        return redirect(adminsignin)


def users(request):
    if request.session.has_key('isAdmin'):
        # user = request.user
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
            print("facility")
            Facilities.objects.create(facility=facility)
            return redirect(facilities)
        else:
            print("hooy")
            return render(request, 'admin/addfacility.html')
    else:
        return redirect(adminsignin)



def addCategory(request):
    if request.session.has_key('isAdmin'):
        if request.method=='POST':
            print('hello')
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
            print('post')
            category_sport = Category.objects.get(id=id)
            category_sport.sport = request.POST['category']
            if 'iconfile' not in request.POST:
                icon = request.FILES.get('iconfile')
            else:
                icon = category_sport.icon
            category_sport.icon = icon
            print(category_sport.sport)
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
        print(user.is_active)
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
        if turf.status == 'accept':
            turf.status = 'pending'
        else:
            turf.status = 'accept'
        turf.save()
        return redirect(turfs)
    else:
        return redirect(adminsignin)


def turf_requests(request):
    if request.session.has_key('isAdmin'):
        status = Turf.objects.filter(status='pending')
        print(status)
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


def logout(request):
    if request.session.has_key('isAdmin'):
        request.session.flush()
        return redirect(adminsignin)
    else:
        return redirect(adminsignin)
