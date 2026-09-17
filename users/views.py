from django.shortcuts import render,redirect
from django.contrib import messages
from .models import AdminDetails
from .models import CustomerDetails
from .models import DriverDetails
from .models import Location
from .models import OrderDetails
from django.db import IntegrityError

# Create your views here.
def mainlogin(request):
    return render(request,'mainlogin.html')
def success(request):
    return render(request,'success.html')
def admindashboard(request,id):
    if request.session.get('user_type')=='admin' and request.session.get('admin_id')==id:
        driver=DriverDetails.objects.all().values()
        customer=CustomerDetails.objects.all().values()
        location=Location.objects.all().values()
        location_count=Location.objects.count()
        driver_count=DriverDetails.objects.count()
        customer_count=CustomerDetails.objects.count()
        orders=OrderDetails.objects.all().values()
        orders_count=OrderDetails.objects.count()
        orders_completed=OrderDetails.objects.filter(status='delivered').count()
        orders_pending=OrderDetails.objects.filter(status='processing').count()
        orders_picked=OrderDetails.objects.filter(status='Driver assigned').count()

        return render(request,'adminpage.html',{'driver':driver,'customer':customer,
                                                'location':location,'loc_count':location_count,
                                                'order_completed':orders_completed,'orders_count':orders_count,
                                                'driv_count':driver_count,'cust_count':customer_count,
                                                'orders':orders,'orders_pending':orders_pending,
                                                'orders_picked':orders_picked,'id':id})
    else:
        return redirect('mainlogin')
def loginprocess(request):
    uname=request.POST.get('uname')
    pwt=request.POST.get('pwt')
    acctype=request.POST.get('acctype')
    dit={'actype':acctype}
    if acctype=='admin':
        user=AdminDetails.objects.filter(username=uname).first()
        if user and pwt==user.password:
            request.session['user_type']='admin'
            request.session['admin_id']=user.id
            return redirect('admindashboard',id=user.id)
        else:
            return redirect('mainlogin')    
    elif acctype=='customer':
        user=CustomerDetails.objects.filter(username=uname).first()
        if user and pwt==user.password:
            request.session['user_type']='customer'
            request.session['cust_id']=user.id
            # return render(request,'success.html',{'dit':dit})
            return redirect('customerdashboard',id=user.id)
        else:
            return redirect('mainlogin')
    else:
        user=DriverDetails.objects.filter(username=uname).first()
        if user and pwt==user.password:
            request.session['user_type']='driver'
            request.session['driver_id']=user.id
            return redirect('driverdashboard',id=user.id)
        else:
            return redirect('mainlogin')
def registration(request):
    return render(request,'registration.html')
def registrationprocess(request):
    uname=request.POST.get('uname')
    pwt=request.POST.get('pwt')
    try:
        user1=CustomerDetails(username=uname,password=pwt)
        user1.save()
        return redirect('mainlogin')
    except IntegrityError:
                    messages.error(request, 'Username already exists. Please choose another username.')
                    return render(request,'duplicatename.html',{'id':id,'value':'registration'})
def adddriver(request,id):
    if request.session.get('user_type')=='admin' and request.session.get('admin_id')==id:
        uname=request.POST.get('uname')
        pwt=request.POST.get('pwt')
        loc=request.POST.get('location')
        try:
            user1=DriverDetails(username=uname,password=pwt,location=loc)
            user1.save()
        except IntegrityError:
                messages.error(request, 'Username already exists. Please choose another username.')
                return render(request,'duplicatename.html',{'id':id,'value':'admindashboard'})
                # return redirect('admindashboard', id=id)
        return redirect('admindashboard',id=id)
    else:
        return redirect('mainlogin')
def addlocation(request,id):
    if request.session.get('user_type')=='admin' and request.session.get('admin_id')==id:
        loc=request.POST.get('location1')
        km=request.POST.get('km')
        loc1=Location(location=loc,km=km)
        loc1.save()
        return redirect('admindashboard',id=id)
    else:
        return redirect('mainlogin')
def customerdashboard(request,id):
    if request.session.get('user_type')=='customer' and request.session.get('cust_id')==id:
        customer=CustomerDetails.objects.filter(id=id).first()
        orders=OrderDetails.objects.all().values()
        location=Location.objects.all().values()
        Driv_ass=OrderDetails.objects.filter(customer_id=id,status='Driver assigned').count()
        completed=OrderDetails.objects.filter(customer_id=id,status='delivered').count()
        processing=OrderDetails.objects.filter(customer_id=id,status='processing').count()
        orders_count=OrderDetails.objects.filter(customer_id=id).count()
        id1=id
        return render(request,'customerdashboard.html',{'orders':orders,'id':id1,'location':location,
                                                        'Driver_assigned':Driv_ass,
                                                        'orders_count':orders_count,
                                                        'completed':completed,
                                                        'processing':processing,
                                                        'customer':customer,
                                                        })
    else:
        return redirect('mainlogin')
def ordering(request,id):
    if request.session.get('user_type')=='customer' and request.session.get('cust_id')==id:
        name = request.POST.get('name')
        # flocation = request.POST.get('flocation')
        flocation ="chennai"
        tlocation = request.POST.get('tlocation')
        weight1=request.POST.get('weight')
        cust_id = request.POST.get('cust_id')
        product = request.POST.get('product')
        order=OrderDetails(name=name,from_location=flocation,to_location=tlocation,weight=weight1,customer_id=cust_id,product=product)
        order.save()
        location=Location.objects.filter(location=tlocation).first()
        kmamount=(int(location.km)*5)
        kgamount=(int(weight1)*10)
        total=kmamount+kgamount
        return render(request,'payment.html',{'locationkm':location.km,'kg':weight1,'location':location.location,'cust_id':cust_id,
                                            'kmamount':kmamount,'kgamount':kgamount,'total':total,'id':id})
        return redirect('customerdashboard',id=cust_id)
    else:
        return redirect('mainlogin')
def payment(request):
    pass
def duplicatename(request):
    pass
def assingdriver(request,id):
    if request.session.get('user_type')=='admin' and request.session.get('admin_id')==id:
        if request.method == 'POST':
            drivers = DriverDetails.objects.filter(status='available')
            for y in drivers:
                orders = OrderDetails.objects.filter(status='processing',to_location=y.location)
                if orders.exists():
                    for x in orders:
                        OrderDetails.objects.filter(id=x.id).update(Driver_id=y.id,Driver_name=y.username,status='Driver assigned')
                    DriverDetails.objects.filter(id=y.id).update(status='in order')
            return redirect('admindashboard',id=id)
        else:
            return render(request, 'success.html')
    else:
        return redirect('mainlogin')
def driverdashboard(request,id):
    if request.session.get('user_type')=='driver' and request.session.get('driver_id')==id:
        orders=OrderDetails.objects.all().values()
        id1=id
        driver=DriverDetails.objects.filter(id=id1).first()
        order_count=OrderDetails.objects.filter(Driver_id=id).count()
        completed=OrderDetails.objects.filter(Driver_id=id,status='delivered').count()
        assinged=OrderDetails.objects.filter(Driver_id=id,status='Driver assigned').count()
        return render(request,'driverdashboard.html',{'orders':orders,'id':id1,'driver':driver,
                                                    'order_count':order_count,'completed':completed,
                                                    'assinged':assinged,
                                                    })
    else:
        return redirect('mainlogin')
def delivered(request,orderid,driverid):
    if request.session.get('user_type')=='driver' and request.session.get('driver_id')==driverid:
        OrderDetails.objects.filter(id=orderid).update(status='delivered')
        check=OrderDetails.objects.filter(Driver_id=driverid,status='Driver assigned').first()
        if not check:
            DriverDetails.objects.filter(id=driverid).update(status='available')
        return redirect('driverdashboard', id=driverid)
    else:
        return redirect('mainlogin')
def logout(request):
    request.session.flush()
    return redirect('mainlogin')

# def assingdriver(request):
#     orders=OrderDetails.objects.all()
#     driver=DriverDetails.objects.all()
#     customer=CustomerDetails.objects.all()
#     if request.method=='POST':
#         for x in orders:
#             if x.status=='processing':
#                 for y in driver:
#                     if y.status=='available' and x.to_location==y.location:
#                         OrderDetails.objects.filter(id=x.id).update(Driver_id=y.id,Driver_name=y.username,status='Driver assigned')
#                         DriverDetails.objects.filter(id=y.id).update(status='in order')
#         return redirect('admindashboard')
#     else:
#         return render(request,'success.html')
#     if request.method=='POST':
#         drivers=DriverDetails.objects.filter(status=='available').first()

        
