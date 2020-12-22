import json
from store.models import Product,Order,OrderItem,ShippingAddress,Customer

def cookieCart(request):
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart={}
	items=[]
	order = {'get_cart_total':0,'get_cart_items':0}
	cartItems = order['get_cart_items']

	for i  in cart:
		try:
			cartItems += cart[i]["quantity"]

			product = Product.objects.get(id=i)
			total = (product.price * cart[i]["quantity"])

			order['get_cart_total'] += total
			order['get_cart_items'] += cart[i]["quantity"]

			item = {
				'product':{
					'id': product.id,
					'name': product.name,
					'price': product.price,
					'imageURL': product.imageURL,

				},
				'quantity':cart[i]['quantity'],
				'sizing':cart[i]['sizing'],
				'get_total': total,
			}
			items.append(item)
		except:
			pass

	return {'items': items, 'order': order,'cartItems':cartItems}

def cartData(request):
	if request.user.is_authenticated:
		Customer.objects.get_or_create(user=request.user,first_name=request.user.first_name,last_name=request.user.last_name,email=request.user.email)
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']
	return {'items': items, 'order': order,'cartItems':cartItems}

def guestOrder(request,data):
	
	first_name = data['form']['first_name']
	last_name = data['form']['last_name']
	email = data['form']['email']

	cookieData = cookieCart(request)
	items = cookieData['items']

	customer, created = Customer.objects.get_or_create(
		user=None,
		last_name=last_name,
		email=email,
		)
	
	customer.first_name=first_name
	customer.save()

	order = Order.objects.create(
		customer=customer,
		complete=False,
		)

	for item in items:
		product = Product.objects.get(id=item['product']['id'])

		orderItem = OrderItem.objects.create(
			product=product,
			order=order,
			quantity=item['quantity']
			)

	return customer, order