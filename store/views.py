from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import * 
def store(request):
	data = cartData(request) #從utils 載入cartData()
    #抓取cookieCart中fetch出來的data,並取得views到store.html所需要的資料
	products = Product.objects.all()
	cartItems = data['cartItems'] #顯示購物車數量(小紅字)
	context = {'products':products, 'cartItems':cartItems}
    #store.html需要取值的字典
	return render(request, 'store/store.html', context)

def cart(request):
	data = cartData(request) #從utils 載入cartData()
    #抓取cookieCart中fetch出來的data
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	context = {'items':items, 'order':order, 'cartItems':cartItems}
    #cart.html需要取值的字典
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request) #從utils 載入cartData()
    #讀取cookieCart中fetch出來的data
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
    #checkout.html需要取值的字典
	return render(request, 'store/checkout.html', context)

def updateItem(request): #登入使用者狀態下,監聽購物車增加減少的功能
	data = json.loads(request.body) #取得fetch到的資料
	productId = data['productId'] 
	action = data['action'] 
	print('Action:', action) #在開發人員工具看到驗證
	print('Product:', productId) #在開發人員工具看到驗證

	customer = request.user.customer #抓到登入的使用者,以在資料庫辨認(main.html中只有確認狀態,這裡才用Models物件化,以便抓取)
	product = Product.objects.get(id=productId) #用Models物件化抓到商品
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #回應是否有order
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    #如果order存在,就執行以下調整quantity的選擇結構
    
	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)#在console顯示
    #safe=true是回應字典,false回應字串

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp() #已完成時間建立交易的id
	data = json.loads(request.body)
    
	if request.user.is_authenticated: #登入
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)

	else: #訪客
		customer, order = guestOrder(request, data) #使用utils.py 的guestOrder()


	total = eval(data['form']['total'])
	order.transaction_id = transaction_id #上方設定的
        
	if total == order.get_cart_total:
		order.complete = True #與check.html/傳入的結果一樣的話,就成立,以保護上方設定的data
	order.save()

	if order.shipping == True: #如果上方data 有shipping資訊, 建立shipping的物件
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'], #抓到data中的address
		city=data['shipping']['city'], #抓到data中的city
		state=data['shipping']['state'], #抓到data中的state
		zipcode=data['shipping']['zipcode'], #抓到data中的zipcode
		)

	return JsonResponse('Payment submitted..', safe=False)        