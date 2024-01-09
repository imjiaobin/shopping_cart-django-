import json
from .models import *
#讓views內重複的程式碼抓過來變成function,在從views載入
#避免使用訪客購物時,資料庫內有異動更新後,但order仍存在有異動前的內容,發生資訊錯誤,導致所有功能掛掉
#登入狀態,可以透過Models建立的物件來傳遞data
#訪客狀態,可以透過js中fetch到的cookie來傳遞data

def cookieCart(request):
    #抓到訪客購物車
	try:
		cart = json.loads(request.COOKIES['cart']) #用loads轉出後就變回python的dict
	except: #避免沒有成功建立而出錯,造成網頁掛掉
		cart = {}
		print('CART:', cart)

	items = [] #為cart建立item
	order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False} #設定cart內的初始狀態,以便在cart()和checkhtml使用
	cartItems = order['get_cart_items'] #顯示在購物車的紅色小字的數量

	for i in cart:
		#這邊都是透過main.html中js的cookie抓取到並顯示在cart.html,尚未丟入db
        #建立try,避免使用訪客購物時,資料庫內有異動更新後,但order仍存在有異動前的內容,發生資訊錯誤,導致所有功能掛掉
			try:
			    cartItems += cart[i]['quantity'] #每當加入購物車時,就增加數量
			    product = Product.objects.get(id=i) #然後取得product顯示在頁面
			    total = (product.price * cart[i]['quantity']) #然後取得金額和商品數量並計算
			    order['get_cart_total'] += total #order抓到的總金額
			    order['get_cart_items'] += cart[i]['quantity']#order抓到總數量
            
                #將以上抓到的data,建立成item dict,並改變原本item=[]的初始狀態,以達到更新頁面和購物車的狀態
			    item = {
				    'id':product.id,
				    'product':{'id':product.id,'name':product.name, 'price':product.price, 
				    'imageURL':product.imageURL}, 'quantity':cart[i]['quantity'],
				    'digital':product.digital,'get_total':total,
				    }
			    items.append(item)
            
			    if product.digital == False:
					    order['shipping'] = True
                        
			except: #避免cart內有關資料庫的東西有錯誤,這樣就不會影響訪客購物車功能
				pass
			
	return {'cartItems':cartItems ,'order':order, 'items':items} #上方設定的cart狀態

def cartData(request):
    
	if request.user.is_authenticated: #使用者登入
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
        #get_or_create(),有就取得order資訊,沒有就建立
		items = order.orderitem_set.all()
        #抓到在order中的orderitem
		cartItems = order.get_cart_items#用models的裝飾器取得
        #cart的品項數量
	else: #訪客
		cookieData = cookieCart(request) 
        #從utils.py載入的功能,收到items,order,cartItems狀態,並根據訪客狀態,傳到templates,調整需變動的欄位
		cartItems = cookieData['cartItems']#抓取cookieData中的資料
		order = cookieData['order']
		items = cookieData['items']

	return {'cartItems':cartItems ,'order':order, 'items':items}

def guestOrder(request, data):
    
	print('User is not logged in')
	print('COOKIES:', request.COOKIES)
    
	name = data['form']['name'] #抓到data中的姓名
	email = data['form']['email'] #抓到data中的郵件資訊

	cookieData = cookieCart(request) #設定存到database的格式
	items = cookieData['items']

	customer, created = Customer.objects.get_or_create(
			email=email,
            #儲存訪客的email,建立訪客customer物件並以email為基準,如果訪客之後要再要註冊登入之後再使用,仍然找得到訂單資料
			)
	customer.name = name #抓到該email的訪客的名稱
	customer.save() #儲存資料

	order = Order.objects.create(
		customer=customer,
		complete=False, #在此筆訂單完成結帳前,都處於False的狀態,繼續存在cookie中
		)

	for item in items: #抓cookieCart中的item資料
		product = Product.objects.get(id=item['id'])
		orderItem = OrderItem.objects.create(
        #這邊用models.py 中的OrderItem,因為有外部索引建到models.py的product和order 連建立orderItem物件
			product=product,
			order=order,
			quantity=item['quantity'],#抓cookieCart中的item 的quantity
		)
	return customer, order

