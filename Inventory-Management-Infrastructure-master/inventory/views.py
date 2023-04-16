from django.shortcuts import render,redirect,Http404, HttpResponse
from .forms import QuestForm
from .models import Quest
from geopy.geocoders import Nominatim
import geoip2.database
from geopy.distance import geodesic
import csv
import random
import requests
import folium
from bs4 import BeautifulSoup
from requests.compat import quote_plus

# This reader object should be reused across lookups as creation of it is
# expensive.

# Create your views here.

def get_inventory(request):
    geolocator = Nominatim(user_agent='inventory')
    location = geolocator.geocode("175 5th Avenue NYC")
    location_long = location.longitude
    location_lat = location.latitude
    point1 = (location_lat,location_long)

    map = folium.Map(width=950, height=600, location=point1,tiles='CartoDB')


    quests = Quest.objects.all()

    return render(request, 'index.html',{'quests': quests, 'map': map})

def read(request):
    quests = Quest.objects.all()
    geolocator = Nominatim(user_agent='quests')
    location = geolocator.geocode("1960 Caprihani Way")
    location_long = location.longitude
    location_lat = location.latitude
    point1 = (location_lat,location_long)
    map = folium.Map(width=950, height=600, location=point1, zoom_start=12)
    folium.TileLayer('cartodbdark_matter').add_to(map)
    iconQuester = folium.features.CustomIcon('./media/images/user-secret-solid.svg', icon_size=(100, 100))
    folium.Marker([location_lat, location_long], tooltip='click for info',
                  popup=location, icon=folium.Icon(color='green',prefix='fa',icon='user-secret')).add_to(map)

    for quest in quests:
        location = geolocator.geocode(quest.location)
        location_long = location.longitude
        location_lat = location.latitude
        folium.Marker([location_lat, location_long], tooltip='click for info',
                    popup=location, icon=folium.Icon(color='red',prefix='fa',icon='briefcase')).add_to(map)
    map = map._repr_html_()



    return render(request, 'index.html',{'quests': quests, 'map': map})

def create_quest(request):
    if request.method == 'POST':
        form = QuestForm(request.POST, request.FILES)
        if form.is_valid():
            quest = form.save(commit=False)
            quest.id = random.randint(100000, 999999)
            quest.save()
            return redirect('/')
    else:
        form = QuestForm()
        return render(request, 'create.html', {'form': form})
#
# def order_inventory(request,id):
#     product = Product.objects.get(code=id)
#     items = Item.objects.all()
#     calc_price = round(float(product.manufacturer_price)*1.11,2)
#     for item in items:
#         if item.itemcode==id:
#             item.delete()
#     item = Item(name=product.name,image=product.image,retail_price=calc_price,description="Enter",quantity=1,location="Ottawa",itemcode=id)
#     if request.method == 'POST':
#         form = ItemForm(request.POST,instance=item)
#         if form.is_valid():
#             form.save()
#             return redirect('/')
#     else:
#         form = ItemForm(instance=item)
#         return render(request,'create.html',{'form':form})
#
#
# def create(request):
#     if request.method == 'POST':
#         form = ItemForm(request.POST,request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('/')
#     else:
#         form = ItemForm()
#         return render(request,'create.html',{'form':form})
#
#
# def create_order(request,id):
#     item = Item.objects.get(itemcode=id)
#     if request.method == 'POST':
#         form=OrderForm(request.POST)
#         if form.is_valid():
#             form.save(commit=False)
#             destination = form.cleaned_data.get('destination')
#             email = form.cleaned_data.get('email')
#             quantity = form.cleaned_data.get('quantity')
#             if quantity  > item.quantity:
#                 quantity = item.quantity
#             item.quantity = item.quantity - quantity
#             orderID = random.randint(100000, 999999)
#             item.save()
#             item_cost = item.retail_price*quantity
#             order = Order(item=item,quantity=quantity,orderID=orderID,email=email,destination=destination,item_cost=item_cost,total_cost=0)
#             order.save()
#             return redirect('/')
#     else:
#         form = OrderForm()
#         return render(request,'order.html',{'form':form})
#
# def read(request):
#     product = Product.objects.all()
#     if product.exists():
#         product.delete()
#     final_url = 'https://www.canadacomputers.com/promotions/awesome-savings'
#     page = requests.get(final_url)
#     soup = BeautifulSoup(page.content, "html.parser")
#     results = soup.find(id="product-list")
#     items = results.find_all('div', {'class': 'col-12 py-1 px-1 bg-white mb-1 productTemplate gridViewToggle'})
#     images = results.find_all('img', {'class': 'pq-img-manu_logo align-self-center'})
#     final_postings = []
#     for item in items:
#         item_name = item.find(class_='text-dark text-truncate_3').text
#         print(item_name)
#         image = item.find('img', {'class': 'pq-img-manu_logo align-self-center'})
#         item_image_url = (image.get('src'))
#         item_price = 0
#         item_code = item.get('data-item-id')
#         price = item.find('div', {'class': 'px-0 col-12 productInfoSearch pt-2'})
#         price = price.find("strong").text
#         price = price.replace('$','')
#         price = price.replace(',','')
#         price = float(price)
#         new_product = Product(
#             name = item_name,
#             image = item_image_url,
#             code = item_code,
#             manufacturer_price = price,
#             )
#         new_product.save()
#         final_postings.append((item_name, item_code,item_image_url,price))
#     items = Item.objects.all()
#     products = Product.objects.all()
#     orders = Order.objects.all()
#     shipments = Shipment.objects.all()
#     return render(request, 'index.html',{'items':items,'orders':orders, 'shipments' : shipments,'final_postings': final_postings})
#
# def update(request,id):
#     item = Item.objects.get(itemcode=id)
#     if request.method == 'POST':
#         form = ItemForm(request.POST, instance =item)
#         if form.is_valid():
#             form.save()
#             return redirect('/')
#     else:
#         form = ItemForm(instance = item)
#         return render(request,'update.html',{'form':form})
#
# def delete(request,id):
#         item = Item.objects.get(itemcode=id)
#         item.delete()
#         return redirect('/empty')
#
# def export_to_csv(request):
#     items = Item.objects.all()
#
#     if items.exists():
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="inventory.csv"'
#
#         writer = csv.writer(response)
#         column_names = ['Name', 'Location', 'Quantity','Description', 'Itemcode']
#         writer.writerow(column_names)
#         for item in items:
#             writer.writerow([item.name, item.location, item.quantity, item.description, item.itemcode])
#         return response
#
#     else:
#        return render(request, 'empty.html',{'items':items})
#
#
#
# def calculate_shipment(request,id):
#     order = Order.objects.get(orderID=id)
#     #Caculate Start Coordinates
#     geolocator = Nominatim(user_agent='inventory')
#     location = geolocator.geocode(order.item.location)
#     location_long = location.longitude
#     location_lat = location.latitude
#     point1 = (location_lat,location_long)
#
#     map = folium.Map(width=900, height=600, location=point1)
#     folium.Marker([location_lat, location_long],tooltip='click for info',
#                   popup=['location'], icon=folium.Icon(color='red')).add_to(map)
#
#     if request.method == 'POST':
#         form = ShipmentForm(request.POST)
#         if form.is_valid():
#             shipment = form.save(commit=False)
#             # Calculate destination coordinates
#             destination1 = form.cleaned_data.get('destination')
#             destination = geolocator.geocode(destination1)
#             destination_long = destination.longitude
#             destination_lat = destination.latitude
#             #Calculate Distance and Cost, Duration
#             point2 = (destination_lat,destination_long)
#             distance = round(geodesic(point1,point2).km,2)
#             cost = round((distance / 100),2)
#             order.total_cost = round(float(order.item_cost)+cost,2)
#             order.save()
#             duration = round((distance/200),0)
#             shipId = random.randint(100000, 999999)
#             #Create Shipment obj
#             shipment = Shipment(order=order,destination=destination,distance=distance,ship_cost=cost,duration=duration,shipId=shipId, total_cost=order.total_cost)
#             # Create Map
#             center = (((location_lat+destination_lat)/2),((location_long+destination_long)/2))
#             map = folium.Map(width=600, height=400, location=center, zoom_start=3)
#             folium.Marker([location_lat, location_long],tooltip='click for info',
#                   popup=location, icon=folium.Icon(color='red')).add_to(map)
#             folium.Marker([destination_lat, destination_long],tooltip='click for info',
#                   popup=destination, icon=folium.Icon(color='red')).add_to(map)
#             line = folium.PolyLine(locations=[point1, point2], weight=2, color='red')
#             map.add_child(line)
#             map = map._repr_html_()
#             return render(request,'shipment_info.html',{'shipment':shipment,'form':form, 'map': map})
#     else:
#         shipment = Shipment(order=order,destination=order.destination,distance=0,ship_cost=0,duration=0,shipId=123456,total_cost=0)
#         shipment.save()
#         form = ShipmentForm(instance=shipment)
#         shipment.delete()
#         return render(request,'shipment.html',{'order':order,'form':form})
#
# def create_shipment(request,id):
#     order = Order.objects.get(orderID=id)
#     ship_cost = round(float(order.total_cost - order.item_cost),2)
#     distance = round((ship_cost*100),2)
#     duration = round((distance/200),0)
#     shipId = random.randint(100000, 999999)
#     shipment = Shipment(
#         order=order,
#         destination=order.destination,
#         distance=distance,
#         ship_cost=ship_cost,
#         duration=duration,
#         shipId = shipId,
#         total_cost = order.total_cost
#         )
#     shipment.save()
#     return redirect('/')

