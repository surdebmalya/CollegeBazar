from django.shortcuts import render, redirect
from .models import ITEMS, USERS, USER_WISHLISTS
from PIL import Image
import requests
import base64
import os
from .fuzzySearch import *

ADMIN_EMAIL = 'admin@college.bazar'
ADMIN_PASSWORD = '123456'

# Create your views here.
def home(request):
    try:
        if(request.session['name']):
            items = list(ITEMS.objects.filter().values())
            # print(items)
            return render(request, 'home.html', {'msg': items})
    except:
        return redirect('login')

def login(request):
    try:
        if(request.session['name']):
            return redirect('home')
    except:
        return render(request, 'login.html')

def logIntoAccount(request):
    email = request.POST['email']
    password = request.POST['password']
    if USERS.objects.filter(email=email, password=password).exists():
        result = USERS.objects.filter(email=email)
        name = result.values()[0]['name']
        id = result.values()[0]['id']
        blacklsiornot = result.values()[0]['blacklsiornot']
        request.session['name']=name
        request.session['id']=id
        request.session['email']=email
        request.session['blacklsiornot']=blacklsiornot
        return redirect('home')
    else:
        return render(request, 'error.html', {'code': 404})

def signup(request):
    try:
        if(request.session['name']):
            return redirect('home')
    except:
        return render(request, 'signup.html')

def accountCreation(request):
    name = request.POST['name']
    email = request.POST['email']
    password = request.POST['password']
    blacklsiornot = "0" # not backlisted

    if USERS.objects.filter(email=email).exists():
        # user already present
        return render(request, 'error.html', {'code': 409})
    else:
        # create the user
        newUser = USERS.objects.create(name=name, email=email, 
        password=password, blacklsiornot=blacklsiornot)
        newUser.save()
        request.session['name']=name
        result = USERS.objects.filter(email=email)
        id = result.values()[0]['id']
        request.session['id']=id
        request.session['email']=email
        request.session['blacklsiornot']=blacklsiornot
        return redirect('home')

def logout(request):
    request.session.flush()
    return redirect('home')

def categories(request):
    try:
        if(request.session['name']):
            cat = []
            items = list(ITEMS.objects.filter().values())
            for item in items:
                currCat = item['category']
                if currCat not in cat:
                    cat.append(currCat)
            return render(request, 'categories.html', {'categories': cat})
    except:
        return redirect('home')

def categoryProducts(request):
    try:
        if(request.session['name']):
            cat = request.POST['cat']
            items = list(ITEMS.objects.filter(category=cat).values())
            return render(request, 'home.html', {'msg': items})
    except:
        return redirect('home')

def sell(request):
    try:
        if(request.session['name']):
            return render(request, 'sell.html')
    except:
        return redirect('home')

def upload_to_imgbb():
    with open("temp.jpg", "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": "8e8f1d1d91b7dbfd6e540d738b7486b1",
            "image": base64.b64encode(file.read()),
        }
        res = requests.post(url, payload)
    return res.json()['data']['url']

def createProduct(request):
    name = request.POST['name']
    file = request.FILES['fileuploader']
    image = Image.open(file)
    price = str(request.POST['price'])
    desc = request.POST['textArea']
    category = request.POST['selection']
    image.save("temp.jpg")
    url=upload_to_imgbb()
    os.remove("temp.jpg")
    id = str(request.session['id'])
    print(id)
    newItem = ITEMS.objects.create(
        imageURL=url, name=name, price=price, description=desc, category=category, status="0", userid=id
    )
    newItem.save()

    return redirect('home')

def addToWishlist(request):
    try:
        if(request.session['name']):
            userid = request.POST['userid']
            productid = request.POST['productid']
            newWishlist = USER_WISHLISTS.objects.create(
                userid=userid, itemid=productid
            )
            newWishlist.save()
            return redirect('getDetails')
    except:
        return redirect('login')

def getDetails(request):
    try:
        if(request.session['name']):
            productid = request.POST['productid']
            result = ITEMS.objects.filter(id=productid).values()[0]
            print(result)
            wishlistItems = list(USER_WISHLISTS.objects.filter(itemid=productid).values())
            flag = 0
            if(len(wishlistItems)!=0):
                flag=1
            
            return render(request, 'product.html', {'result': result, 'flag': flag})
    except:
        return redirect('login')

def wishlists(request):
    try:
        if(request.session['name']):
            productids = list(USER_WISHLISTS.objects.filter(userid=request.session['id']).values())
            items = []
            for productid in productids:
                currProduct = list(ITEMS.objects.filter(id=productid['itemid']).values())
                items += currProduct
            return render(request, 'home.html', {'msg': items})
    except:
        return redirect('login')

# Search
def search(request):
    try:
        if(request.session['name']):
            pass
    except:
        return redirect('login')

# Filters sorting by price
def filter(request):
    ind = request.POST['sort']
    if(ind=="increasing"):
        items = list(ITEMS.objects.filter().values())
        # print(items)
        for i in range(len(items)):
            for j in range(len(items)):
                price1 = int(items[i]['price'])
                price2 = int(items[j]['price'])
                if price1 < price2:
                    items[i], items[j] = items[j], items[i]
        return render(request, 'home.html', {'msg': items})
    else:
        items = list(ITEMS.objects.filter().values())
        # print(items)
        for i in range(len(items)):
            for j in range(len(items)):
                price1 = int(items[i]['price'])
                price2 = int(items[j]['price'])
                if price1 > price2:
                    items[i], items[j] = items[j], items[i]
        return render(request, 'home.html', {'msg': items})

# Chatting
def chats(request):
    pass

# Admin pannel
def adminCollegeBazar(request):
    try:
        if(request.session['name']):
            return redirect('home')
    except:
        try:
            if(request.session['admin']):
                return render(request, 'adminDashboard.html')
        except:
            return render(request, 'admin.html')

def logIntoAdminAccount(request):
    email = request.POST['email']
    password = request.POST['password']
    if(email==ADMIN_EMAIL and password==ADMIN_PASSWORD):
        request.session['admin'] = 'admin'
        return render(request, 'adminDashboard.html')
    else:
        return redirect('login')