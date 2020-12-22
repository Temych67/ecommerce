from django.db import models
from accounts.models import Account
from django.db.models.signals import post_delete
from django.dispatch import receiver

def upload_location(instance,filename):
	file_path = 'store/{class_product}/{filename}'.format(
									class_product=str(instance.class_product),
									filename = filename,
								
		)
	return file_path


class Customer(models.Model):
	user 		=	models.OneToOneField(Account, null=True, blank=True, on_delete=models.CASCADE)
	first_name 	=	models.CharField(max_length=100, null=True)
	last_name 	=	models.CharField(max_length=100, null=True)
	email 		=	models.EmailField(max_length=200)

	def __str__(self):
		return str(self.last_name)+" "+str(self.first_name)

class Product(models.Model):
	class_product 	=	models.CharField(max_length=100, null=True)
	name 			=	models.CharField(max_length=100, null=True)
	price 			=	models.DecimalField(max_digits=7, decimal_places=2)
	image		 	= 	models.ImageField(upload_to=upload_location, null=True, blank=True)
	about_product	=	models.CharField(max_length=400, null=True)
	content			=	models.CharField(max_length=100, null=True)
	colour			=	models.CharField(max_length=100, null=True)
	sizing			=	models.CharField(max_length=100, null=True)
	manufacturer	=	models.CharField(max_length=100, null=True)

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url
@receiver(post_delete,sender=Product)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)
     		
class Order(models.Model):
	customer 		=	models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=False, null=True)
	date_ordered 	=	models.DateTimeField(auto_now_add=True)
	complete 		=	models.BooleanField(default=False, null=True, blank=False)
	transaction_id 	=	models.CharField(max_length=200, null=True)

	def __str__(self):
		return str(self.id)

		
	@property
	def shipping(self):
		shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total
	
class OrderItem(models.Model):
	product 		=	models.ForeignKey(Product, on_delete=models.SET_NULL, blank=False, null=True)
	order 			=	models.ForeignKey(Order, on_delete=models.SET_NULL, blank=False, null=True)
	quantity		=	models.IntegerField(default=0, null=True, blank=True)
	sizing			=	models.CharField(max_length=100, null=True)
	date_added		=	models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	customer 		=	models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=False, null=True)
	order 			=	models.ForeignKey(Order, on_delete=models.SET_NULL, blank=False, null=True)
	address 		=	models.CharField(max_length=100, null=True)
	city 			=	models.CharField(max_length=100, null=True)
	state 			=	models.CharField(max_length=100, null=True)
	zipcode 		=	models.CharField(max_length=100, null=True)
	date_added		=	models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address