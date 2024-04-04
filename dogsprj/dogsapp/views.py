from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from dogsapp.models import Product,Cart,Order
from django.db.models import Q
import random
import razorpay



# Create your views here.

def Userlogin(request):
    if request.method=="POST":
        context={}

        uname=request.POST["uname"]
        upass=request.POST["upass"]

        if uname=="" or upass=="":
            context['errormsg']="Field cannot be empty"
            return render(request,"register.html",context)
        
        else:
            a=authenticate(username=uname,password=upass)

            if a is not None:
                login(request,a)

                return redirect("/home")
            
            else:
                context['errormsg']="Invalid username & password"
                return render(request,"login.html",context)

    
    else:
        return render(request,"login.html")
    

def Userlogout(request):
    logout(request)
    return redirect("/home")

def register(request):
     context={}
     if request.method=='POST':
       uname=request.POST['uname']
       upass=request.POST['upass']
       upsc=request.POST['upsc']
       if uname==''or upass=='':
            context['errormsg']='Field should not be empty'
            return render(request,'register.html',context)
       elif upass !=upsc:
           context['errormsg']="Password didn't match"
           return render(request,'register.html',context)
           
       else:
          try:
               c=User.objects.create(username=uname)
               c.set_password(upass)
               c.save()
               context['success']="user created succesfully plz login"
               return render(request,'register.html',context)
          except Exception:
              context['errormsg']='Username Already Exists'
              return render(request,'register.html',context)
     else:
      if request.method=='GET':
        return render(request,'register.html')
      

def home(request):
     context={}
     p=Product.objects.filter(is_active=True)
     context['products']=p
     return render(request,"index.html",context)


def product_details(request,pid):
     context={}
     context['products']= Product.objects.filter(id=pid)
     return render(request,"product_details.html",context)

def catfilter(request,cv):
    print(cv)
    q1=Q(is_active=True)
    q2=Q(cat=int(cv))
    p=Product.objects.filter(q1 & q2)
    print(p)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated:
     userid=request.user.id
     u=User.objects.filter(id=userid)
     print(u[0])
     p=Product.objects.filter(id=pid)
     print(p[0])
     c=Cart.objects.create(uid=u[0],pid=p[0])
     c.save()
     #print(userid)
     #print(pid)
     return HttpResponse("id fetched")
    else:
        return redirect("/login")

def viewcart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    s=0
    np=len(c)
    for x in c:
        #print(x)
        #print(x.pid.price)
        s=s+x.pid.price *x.qty
        context={}
        context['n']=np
        context['products']=c
        context['total']=s
    return render(request,'cart.html',context)

def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    print('order id ',oid)
    

    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    np=len(c)
    
    for x in c:

        s=s+x.pid.price*x.qty
        context={}
        context['n']=np
        context['products']=c
        context['total']=s
    return render(request,'placeorder.html',context)

def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    if qv=="1":
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
           t=c[0].qty-1
           c.update(qty=t)
    return redirect('/viewcart')

def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    context={}
    for x in orders:

        s=s+x.pid.price*x.qty
        oid=x.order_id
    
    client = razorpay.Client(auth=("rzp_test_E817J41F3AnuA8", "72ZXK5Lwz6fondt5Hmw1eXns"))

    data = { "amount": s*100, "currency": "INR", "receipt": "oid" }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context["data"]=payment
    return render(request,"pay.html",context)

 
    

def register(request):
     context={}
     if request.method=='POST':
       uname=request.POST['uname']
       upass=request.POST['upass']
       upsc=request.POST['upsc']
       if uname==''or upass=='':
            context['errormsg']='Field should not be empty'
            return render(request,'register.html',context)
       elif upass !=upsc:
           context['errormsg']="Password didn't match"
           return render(request,'register.html',context)
           
       else:
          try:
               c=User.objects.create(username=uname)
               c.set_password(upass)
               c.save()
               context['success']="user created succesfully plz login"
               return render(request,'register.html',context)
          except Exception:
              context['errormsg']='Username Already Exists'
              return render(request,'register.html',context)
     else:
      if request.method=='GET':
        return render(request,'register.html')


def remove(request,cid):
     c=Cart.objects.filter(id=cid)
     c.delete()
     return redirect('/viewcart')

# Create your views here.
