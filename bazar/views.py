from django.shortcuts import render, redirect
from .models import ITEMS, USERS, USER_WISHLISTS, CHATROOMS, MESSAGES
from PIL import Image
import requests
import base64
import os
from .fuzzySearch import *
from django.http import JsonResponse, HttpResponse

def home(request):
    try:
        if(request.session['name']):
            items = list(ITEMS.objects.filter().values())
            return render(request, 'home.html', {'msg': items, 'name': request.session['name'], 'number': len(items)})
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
            return render(request, 'home.html', {'msg': items, 'name': request.session['name'], 'number': len(items)})
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
    newItem = ITEMS.objects.create(
        imageURL=url, name=name, price=price, description=desc, category=category, status="0", userid=id
    )
    newItem.save()

    return redirect('home')

def getDetails(request):
    try:
        if(request.session['name']):
            productid = request.POST['productid']
            result = ITEMS.objects.filter(id=productid).values()[0]
            wishlistItems = list(USER_WISHLISTS.objects.filter(itemid=productid).values())
            flag = 0
            if(len(wishlistItems)!=0):
                flag=1
            sellerid=int(result['userid'])
            buyerid=request.session['id']
            
            return render(request, 'product.html', {'result': result, 'flag': flag, 'sellerid': sellerid, 'buyerid': buyerid})
    except:
        return redirect('login')

# Add product to the wishlist
def addToWishlist(request):
    try:
        if(request.session['name']):
            userid = request.session['id']
            productid = request.POST['productid']
            newWishlist = USER_WISHLISTS.objects.create(
                userid=userid, itemid=productid
            )
            newWishlist.save()
            return redirect('wishlists')
    except:
        return redirect('login')

# See the wishlist section
def wishlists(request):
    try:
        if(request.session['name']):
            productids = list(USER_WISHLISTS.objects.filter(userid=request.session['id']).values())
            items = []
            for productid in productids:
                currProduct = list(ITEMS.objects.filter(id=productid['itemid']).values())
                items += currProduct
            return render(request, 'home.html', {'msg': items, 'name': request.session['name'], 'number': len(items)})
    except:
        return redirect('login')

# Filters sorting by price
def filter(request):
    ind = request.POST['sort']
    if(ind=="increasing"):
        items = list(ITEMS.objects.filter().values())
        for i in range(len(items)):
            for j in range(len(items)):
                price1 = int(items[i]['price'])
                price2 = int(items[j]['price'])
                if price1 < price2:
                    items[i], items[j] = items[j], items[i]
        
        return render(request, 'home.html', {'msg': items, 'name': request.session['name'], 'number': len(items)})
    else:
        items = list(ITEMS.objects.filter().values())
        for i in range(len(items)):
            for j in range(len(items)):
                price1 = int(items[i]['price'])
                price2 = int(items[j]['price'])
                if price1 > price2:
                    items[i], items[j] = items[j], items[i]
        return render(request, 'home.html', {'msg': items, 'name': request.session['name'], 'number': len(items)})

# Search
def search(request):
    try:
        if(request.session['name']):
            keyword = request.POST['search']
            all_items = []
            items = list(ITEMS.objects.filter().values())
            for item in items:
                temp=[]
                temp.append(item['name'])
                temp.append(item['id'])
                all_items.append(temp)

            # getting the fuzzy search result
            threshold = 20
            result = luceneFuzzySearchPercentage(all_items, keyword, threshold)
            return_items = []
            for i in result:
                item_id = i[0][1]
                item = list(ITEMS.objects.filter(id=item_id).values())[0]
                return_items.append(item)
            return render(request, 'home.html', {'msg': return_items, 'name': request.session['name'], 'number': len(return_items)})
    except:
        return redirect('login')

# Chatting
def chat(request):
    try:
        if(request.session['name']):
            sellerid=int(request.POST['sellerid'])
            buyerid=int(request.session['id'])
            minid=sellerid
            maxid=buyerid
            if sellerid>buyerid:
                minid=buyerid
                maxid=sellerid
            
            roomidKey = str(minid)+'-'+str(maxid)
            
            result = list(CHATROOMS.objects.filter(roomid=roomidKey).values())
            if(len(result)==0):
                # create the room
                new_room = CHATROOMS.objects.create(roomid=roomidKey)
                new_room.save()
            
            username=str(request.session['id'])
            return redirect('/'+roomidKey+'/?username='+username)
    except:
        return redirect('login')

# Chatting room
def room(request, room):
    username = request.GET.get('username')
    room_id = list(CHATROOMS.objects.filter(roomid=room).values())
    if(room_id!=[]):
        room_id = room_id[0]['id']
    return render(request, 'room.html', {'room': room, 'username': username, 'room_id': room_id})

def getMessages(request, room):
    room_details = CHATROOMS.objects.get(roomid=room)
    messages = MESSAGES.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values()), "ownid": str(request.session['id'])})

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = MESSAGES.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse("Message sent successfully")

def allChats(request):
    try:
        if(request.session['name']):            
            all_rooms = list(CHATROOMS.objects.filter().values())
            ownid = str(request.session['id'])
            roomids_to_be_rendered=[]
            for i in all_rooms:
                room_id = i['roomid'].split('-')
                if ownid in room_id and room_id[0]!=room_id[1]:
                    roomids_to_be_rendered.append(i['roomid'])  

            return render(request, 'chatDashboard.html', {"rooms": roomids_to_be_rendered, "length": len(roomids_to_be_rendered)})
    except:
        return redirect('login')

def resumeChatting(request):
    try:
        if(request.session['name']):
            roomidKey = request.POST['roomidKey']
            username=str(request.session['id'])
            return redirect('/'+roomidKey+'/?username='+username)
    except:
        return redirect('login')

# Viewing my products
def myProducts(request):
    try:
        if(request.session['name']):
            ownid = str(request.session['id'])
            all_product_of_the_user = list(ITEMS.objects.filter(userid=ownid).values())
            return render(request, 'home.html', {'msg': all_product_of_the_user, 'name': request.session['name'], 'number': len(all_product_of_the_user)})
    except:
        return redirect('login')