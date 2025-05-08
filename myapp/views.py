from django.shortcuts import render,redirect
from myapp.models import pet,Cart,myOrder
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q  #Q used for filteration
import razorpay
import uuid
from django.core.mail import send_mail

# Create your views here.
def index(request):
    user=request.user
    print("user logged in?",user.is_authenticated)
    context={}
    allpets=pet.objects.all()
    context['pets']=allpets
    return render(request,"index.html")

def userLogin(request):
    if request.method=="GET":
        return render(request,"login.html")
    else:
        u=request.POST['username']
        p=request.POST['password']

        user=authenticate(username=u,password=p)
        # print('Login user after authenticate',user)
        if user is not None:
            #successfull login
            login(request,user)
            return redirect('/')
        else:
            context={}
            context['error']='Plz enter valid credentials'
            return render(request,'login.html',context)
    
def userRegister(request):
     if request.method=="GET":
        return render(request,"register.html")
     else:
         u=request.POST['username']
         e=request.POST['email']
         p=request.POST['password']
         cp=request.POST['confirmPassword']

         context={}
     
         if u=='' or e=='' or p=='' or cp=='':
            context['error']='All the fields are compulsory'
            return render(request,'register.html',context)
         elif p!=cp:
             context['error']='Password and confirm password must be same'
             return render(request,'register.html',context)
         else:

            user=User.objects.create(username=u,email=e)
            user.set_password(p)
            user.save()
         
            return redirect('/login')

def index(request):
    context={}
    allPets=pet.objects.all()
    context['pets']=allPets
    return render(request,'index.html',context)


def getPetById(request,petid):
    context={}
    petObj=pet.objects.get(id=petid)
    context['pet']=petObj
    return render(request,'details.html',context)


def userlogout(request):
    logout(request)
    return redirect('/')

def filterByCategory(request,catName):
    context={}
    allPets=pet.objects.filter(type=catName)
    context['pets']=allPets
    print(catName)
    print(allPets)
    return render(request,'index.html',context)

def sortByPrice(request,direction):
    if direction=='asc':
        column='price'
    else:
        column='-price'
    context={}
    allPets=pet.objects.order_by(column)
    context['pets']=allPets
    return render(request,'index.html',context)

def filterByRange(request):
    min=request.GET['min']
    max=request.GET['max']

    c1=Q(price__gte=min)
    c2=Q(price__lte=max)
    pets=pet.objects.filter(c1 & c2)
    context={}
    context['pets']=pets
    return render(request,'index.html',context)

def addToCart(request,petid):
    selectedPetObject=pet.objects.get(id=petid)
    userid=request.user.id
    loggedInUserObject=User.objects.get(id=userid)
    cart=Cart.objects.create(uid=loggedInUserObject,petid=selectedPetObject)
    cart.save()
    return redirect('/')


def showMyCart(request):
    userid=request.user.id
    user=User.objects.get(id=userid)
    myCart=Cart.objects.filter(uid=user)
    print(myCart)
    context={'mycart':myCart}
    count=len(myCart)
    TotalBill = 0
    for cart in myCart:
        TotalBill += cart.petid.price * cart.quantity
    context ["count"]=count 
    context["TotalBill"] = TotalBill
    return render(request,'mycart.html',context)

def removeCart(request,cartid):
    c=Cart.objects.filter(id=cartid)
    c.delete()
    return redirect('/showmycart')

def updateQuantity(request, cartid, operation):
    cart =Cart.objects.filter(id=cartid)

    if operation == 'incr':
        q = cart[0].quantity
        cart.update(quantity=q+1)
        return redirect('/showmycart')
    else:
        q = cart[0].quantity
        cart.update(quantity=q-1)
        return redirect('/showmycart')
    
def confirmOrder(request):
    userid = request.user.id
    print(userid)
    user = User.objects.get(id=userid)
    print(user)
    myCart = Cart.objects.filter(uid = user)
    context = {'mycart': myCart}
    count = len(myCart)
    TotalBill = 0
    for cart in myCart:
        TotalBill += cart.petid.price * cart.quantity
    context ["count"]=count 
    context["TotalBill"] = TotalBill 
    return render (request,'confirm.html', context)


# 1 Add details in order table
#a) get current logged in user 
# get the current users cart data

#find out total bill amount for this user
def makePayment(request):
    userid = request.user.id
    data = Cart.objects.filter(uid = userid)
    total = 0
    for cart in data :
        total += cart.petid.price*cart.quantity
    client=razorpay.Client(auth=("rzp_test_J3K0nbI279n8zQ","NL45n1iC9tkA6Dl0AS9svNPL"))
    data = { 'amount': total*100, 'currency':'INR', 'receipt': ''}
    payment=client.order.create(data=data)
    print(payment)
    context={}
    context['data']=payment

    return render(request,'pay.html', context)

def placeOrder(request):
    ordid = uuid.uuid4()
    userid = request.user.id
    cartlist = Cart.objects.filter(uid = userid)
    for cart in cartlist:
        order = myOrder.objects.create(orderid = ordid, userid = cart.uid, petid = cart.petid, quantity = cart.quantity)
        order.save()
    cartlist.delete()
    #sending mail
    msg="Dhanyawad!.Your order id is:"+str(ordid) 
    send_mail(
        "Order placed successfully",
        msg,
        "vedantkotlapure2770@gmail.com",
        [request.user.email],
        fail_silently=False
    )
    return redirect('/')

def about(request):
    return render(request, 'aboutus.html')

def contact(request):
    return render(request, 'contactus.html')