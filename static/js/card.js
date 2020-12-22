var updateBtns	=	document.getElementsByClassName('update-cart')

var sizes = null;


function cart_view() {
  var size = document.getElementById('mySelect').value;
  sizes = size
}
  
for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		if (sizes != null){
			var sizing 		=	sizes
		}
		else{
			var sizing 		=	this.dataset.sizing
		}
		
		var productId 	=	this.dataset.product
		var action		=	this.dataset.action	
		console.log('productId:', productId, 'action:', action)

		console.log('USER:', user)
		if (user == 'AnonymousUser'){
			addCookieItem(productId, action,sizing)
		}else{
			updateUserOrder(productId, action,sizing)
		}

	})
}


function addCookieItem(productId, action,sizing){
	console.log('User is not authenticated')
	if (action == 'add'){
		if(cart[productId] == undefined){
			cart[productId] = {'quantity': 1}
			cart[productId]['sizing'] = sizing
		}else{
			cart[productId]['quantity'] += 1
			cart[productId]['sizing'] = sizing
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1
		cart[productId]['sizing'] = sizing
		if(cart[productId]['quantity'] <= 0){
			console.log('Remove Item')
			delete cart[productId]
		}
	}
	console.log('cart:', cart)
	document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
	location.reload()

}

function updateUserOrder(productId, action,sizing){
	console.log('User is authenticated, sending data...')
	var url = '/update_item/'

	fetch(url, {
		method:'POST',
		headers:{
			'Content-Type': 'application/json',
        	'Accept': 'application/json',
			'X-CSRFToken': csrftoken,
		},
		
		body:JSON.stringify({'productId': productId, 'action': action,'size':sizing})
	})

	.then((response) =>{
		return response.json()
	})

	.then((data) =>{
		console.log('data:', data)
		location.reload()
	})
}
