from django.shortcuts import render
from store.models import Product,Order,OrderItem,ShippingAddress
# Email import
from store.tasks import send_email

from django.template.loader import render_to_string
# Pagination
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

CART_PER_PAGE = 3

from django.http import JsonResponse
import json
from store.utils import cookieCart,cartData,guestOrder

import datetime

def store(request):	
	data = cartData(request)

	cartItems = data['cartItems']

	context={'cartItems':cartItems}
	return render(request, 'main_templates/main.html',context)


def cart(request,slug):
	data = cartData(request)
	products = Product.objects.filter(class_product=slug)
	cartItems = data['cartItems']
	# Pagination
	page = request.GET.get('page', 1)
	cart_page_paginator=Paginator(products,CART_PER_PAGE)
	try:
		products = cart_page_paginator.page(page)
	except PageNotAnInteger:
		products = cart_page_paginator.page(BLOG_POSTS_PER_PAGE)
	except EmptyPage:
		products = cart_page_paginator.page(blog_posts_paginator.num_pages)
	
	context={'cartItems':cartItems,'slug': slug,'products':products}
	return render(request, 'store/cart.html',context)

def cart_views(request,slug,item):
	data = cartData(request)	
	item = Product.objects.get(class_product=slug,name=item)
	size = list(Product.objects.filter(class_product=slug,name=item).values('sizing'))
	cartItems = data['cartItems']
	context={'item':item,'slug':slug,'cartItems':cartItems,'size': size[0]['sizing'].split(',')}
	return render(request, 'store/view_item.html',context)

def basket(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	context={'items': items, 'order': order,'cartItems':cartItems}	
	return render(request, 'store/basket.html',context)

def checkout(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context={'items': items, 'order': order,'cartItems':cartItems}
	return render(request, 'store/checkout.html',context)


def updateItem(request):
	data = json.loads(request.body)
	print(data)
	productId = data['productId']
	action = data['action']
	size = data['size']

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
		orderItem.sizing   =	size
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)
	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()


	return JsonResponse('Item was added', safe=False)

def info_store(request):
	return render(request, 'store/info_store.html',context={})

def processOrder(request):
	transaction_id	= datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)

		template = render_to_string("store/email_template.html", {'first_name': request.user.first_name})
		send_email.delay(request.user.email,template)
	else:
		customer, order = guestOrder(request,data)
		template = render_to_string("store/email_template.html", {'first_name': customer.first_name})
		send_email.delay(customer.email,template)
			
	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
			customer = customer,
			order = order,
			address = data['shipping']['address'],
			city = data['shipping']['city'],
			state = data['shipping']['state'],
			zipcode = data['shipping']['zipcode'],
			)
		
		
	return JsonResponse('Payment complete!', safe=False)
