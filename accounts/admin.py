from django.contrib import admin
from accounts.models import Account
from django.contrib.auth.admin import UserAdmin


    

class AccountAdmin(UserAdmin):
	list_display = ('first_name','last_name','email','date_joined','last_login','is_admin','is_staff')
	search_fields = ('first_name','last_name','email')
	readonly_fields = ('date_joined', 'last_login')
	
	ordering = ('email',)

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

admin.site.site_header = 'Django Admin Panel'
admin.site.register(Account, AccountAdmin)
