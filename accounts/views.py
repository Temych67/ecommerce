from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from accounts.forms import LoginForm, SignUpForm, AccountUpdateForm
from accounts.models import Account
from store.models import Customer,Order,Product,OrderItem
from store.utils import cartData
from store.utils import cartData

def handler500(request,*args, **kwargs):
    return render(request,'account/error500.html')

def handler404(request,*args, **kwargs):
    return render(request,'account/error404.html')

def logout_view(request):
	logout(request)
	return redirect('stores')

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    
    return render(request, "account/login.html", {"form": form, "msg" : msg})

def register_user(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(first_name=first_name,last_name=last_name,email=email, password=raw_password)
            created=Customer.objects.get_or_create(user=user,first_name=first_name,last_name=last_name,email=email)
            msg     = 'User created.'
            success = True
            
            #return redirect("/login/")

        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()

    return render(request, "account/register.html", {"form": form, "msg" : msg, "success" : success })

def account_view(request):

    if not request.user.is_authenticated:
        return redirect("login")
    context={}

    if request.POST:

        form = AccountUpdateForm(request.POST or None, request.FILES or None, instance = request.user.customer)   
        if form.is_valid():
            form.save()
        
        form = AccountUpdateForm(request.POST or None, request.FILES or None, instance = request.user)
       
        if form.is_valid():
            form.initial = {
                "email": request.user.email,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
            }
            form.save()

            context['success_message'] = "Update"
    else:
        form = AccountUpdateForm(
            initial={
                    "email": request.user.email,
                    "first_name": request.user.first_name,
                    "last_name": request.user.last_name,
                }
            )

    productItemslist=[]
    order = Order.objects.filter(customer=request.user.customer, complete=True)

    for item in order:
        productItemslist.append(OrderItem.objects.filter(order=item))
    data = cartData(request)
    cartItems = data['cartItems']
    context={'cartItems':cartItems}
    context['orderitem'] = productItemslist
    context['account_form'] = form
    return render(request, "account/account_change.html", context)


def must_authenticate_view(request):
    return render(request, 'account/must_authenticate.html',{})

def must_be_a_admin(request):
    return render(request, 'account/must_be_a_admin.html',{})
