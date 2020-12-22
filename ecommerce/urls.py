from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include

from django.conf.urls.static import static
from django.conf import settings



from accounts.views import(
    register_user,
    logout_view,
    login_view,
    must_authenticate_view,
    account_view,
    must_be_a_admin,
    handler404,
    handler500,
)

from store.views import(
    store,
    cart,
    basket,
    checkout,
    updateItem,
    processOrder,
    cart_views,
    info_store,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',store, name='stores'),
    path('cart/<slug>',cart, name='cart'),
    path('cart/<slug>/<str:item>',cart_views, name='cart_view'),
    path('basket/',basket, name='basket'),
    path('checkout/',checkout,name='checkout'),
    path('update_item/',updateItem,name='update_item'),
    path('process_order/',processOrder,name='process_order'),
    path('info_store/',info_store,name='info_store'),

    path('accounts/', include('allauth.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),

    path('account/',account_view,name='account'),  
    path('login/',login_view,name='login'),
    path('register/',register_user,name='register'),
    path('logout/',logout_view,name='logout'),
    path('must_authenticate/',must_authenticate_view,name='must_authenticate'),
    path('must_be_a_admin/',must_be_a_admin,name='must_be_a_admin'),

    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
        name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete'),

]

handler500 = 'accounts.views.handler500'
handler404 = 'accounts.views.handler404'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
  
