from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model): #使用者
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    #'OneToOne'表示每一位使用者只會配一個帳號
    #設定'on_delete=models.CASCADE',一旦帳號被刪除,使用者也會被刪除
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Product(models.Model): #商品
	name = models.CharField(max_length=200)
	price = models.FloatField()
	digital = models.BooleanField(default=False,null=True, blank=True)
    #shipping 時判斷是否為實體商品,以在js中確認是否要顯示 shipping-Info
	image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return self.name


	@property #建立image的網頁連結後,抓取image
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

        
class Order(models.Model): #訂單
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    #繼承Customer,建立複合鍵
    #如果使用者被刪除,訂單資訊還是會在,故設定'on_delete=models.SET_NULL'
	date_ordered = models.DateTimeField(auto_now_add=True)#訂單成立時間
	complete = models.BooleanField(default=False)#js在判斷訂單狀況時可以使用
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id) #轉成str才能以__str__回傳

	@property #計算訂單總金額,傳給cart.html的form
	def get_cart_total(self):
		orderitems = self.orderitem_set.all() 
		total = sum([item.get_total for item in orderitems])#迴圈計算商品總額
		return total 

	@property #計算訂單品項總數,傳給cart.html的form
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])#迴圈計算商品總數
		return total
    
	@property #是否有需要寄送表格
	def shipping(self):
		shipping = False #不用寄送
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping #回傳product的digital狀態

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property #計算購物車個別品項的總金額
	def get_total(self):
		total = self.product.price * self.quantity
		return total
    #計算個別商品的數量由js監聽器操作箭頭處理

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address