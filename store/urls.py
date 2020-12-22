from django.urls import path,include

from store.views import(
	store,
	cart,
	basket,
	checkout,
	updateItem,
	processOrder,
	)

app_name = 'store'

urlpatterns = [

	path('',store, name='stores'),
	path('cart/<slug>',cart, name='cart'),
	path('cart/<slug>/<item>',cart, name='cart_view'),
	path('basket/',basket, name='basket'),
	path('checkout/',checkout,name='checkout'),
	path('update_item/',updateItem,name='update_item'),
	path('process_order/',processOrder,name='process_order'),

]
