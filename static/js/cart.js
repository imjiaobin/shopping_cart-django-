var updateBtns = document.getElementsByClassName('update-cart')
    /*建立updateBtns監聽事件, 以update-cart為辨認的class節點*/
for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){ 
	    /*點擊加入購物車就執行*/
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
		
		/*於main.html就監聽的使用者狀態*/
		console.log('USER:', user)
		if (user == 'AnonymousUser'){
			addCookieItem(productId, action) /*是訪客的話,就進行addCookieItem*/
			
		}else{
			updateUserOrder(productId, action)
		}

	})
}


/*是登入的使用者的話,就用更新訂單內購物車的方式*/
function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/' /*傳遞監聽資訊給views的updateItem()*/

		fetch(url, {  /*以fetch()傳遞監聽資訊*/
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken': csrftoken, /*csrftoken保護*/
			}, 
			body:JSON.stringify({'productId':productId, 'action':action}) /*以字串形式傳遞*/
		})
		.then((response) => {
		   return response.json(); /*轉成json給JsonResponse*/
		})
		.then((data) => {
		    console.log('data:', data) /*回應promise*/
		    location.reload() /*每一次回應promise便reload以得到監聽的updatItem()最新狀態*/
		});
}

function addCookieItem(productId, action){  
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}