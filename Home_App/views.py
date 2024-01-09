from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from Home_App.models import customer_table, admin_table, category_table, food_table, order_table
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse


# Create your views here.

# for customers
class CustomerTableBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # check if the credentials are in customer table or not
            customer = customer_table.objects.get(user_id=username, password=password)
        
            #creating a User instance using customer_table data
            user = User(
                id=customer.customer_id,
                username=customer.user_id,
                first_name=customer.first_name,
                last_name=customer.last_name,
                email=customer.email_id,
                password=customer.password,
            )
            print("Authenticated as customer:", user)
            return user
        except customer_table.DoesNotExist:
            pass

        
    

    def login_user(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('pass1')

            #using custom authentication method
            user = authenticate(request,username=username, password=password)

            if user is not None:
                # user credentails are correct then log in the user
                login(request,user)
                fname = user.first_name
                return render(request,"index.html", {'fname':fname})
            else:
                # user credentials are incorrect, display an error message
                messages.error(request,"Invalid Credentials!")
                return redirect('index')
            
        return render(request,'login.html')


    

    
# For Admin
class AdminTableBackend(ModelBackend):
    def authenticate(self, request, user_name=None, password=None, **kwargs):
    
        try:
            #check if the credentials are in admin table or not
            admin_user = admin_table.objects.get(user_name=user_name, password=password)

            #creating a user instance using admin data
            user = User(
                id=admin_user.admin_id,
                username=admin_user.user_name,
                password=admin_user.password,
                # is_admin=admin_user.is_admin,
            )

            # user.is_admin = admin_user.is_admin
            # print("Authenticated as admin:", user)
            return user
        
        except admin_table.DoesNotExist:
            return None

        
    

    def login_user(request):
        if request.method == 'POST':
            user_name = request.POST.get('user_name')
            password = request.POST.get('password')

            #using custom authentication method
            user = authenticate(request,user_name=user_name, password=password)

            if user is not None:
                # user credentails are correct then log in the user
                login(request,user)
                # user_name = user.user_name
                return render(request,"admin-dashboard.html", {'user_name':user_name})
            else:
                # user credentials are incorrect, display an error message
                messages.error(request,"Invalid Credentials!")
                return redirect('index')
            
        return render(request,'admin-login.html')
    




def signup(request):
    if request.method=="POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        dob = request.POST['dob']
        phone_no = request.POST['phone_no']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return render(request,'signup')

       

        new_customer = customer_table (
            first_name=fname,
            last_name=lname,
            email_id=email,
            dob=dob,
            phone_no=phone_no,
            user_id=username,
            password=pass1,
        )

        # myuser.save()
        new_customer.save()

        messages.success(request, "Your Account has been successfully created")

        return redirect('/login')
    
    return render(request, 'signup.html')





def signout(request):
    logout(request)
    messages.success(request,"Logout Successfully")
    return render(request,'index.html')


def index(request):
    if request.user.is_authenticated:
        fname = request.user.first_name
        return render(request, 'index.html', { 'fname': fname})
    else:
        return render(request, 'index.html')


def adminLogin(request):
    return render(request,'admin-login.html')

def adminDashboard(request, section=None):
    section_template = {
        'categories': 'admin-dashboard-category.html',
        'customers': 'admin-dashboard-customers.html',
        'foodItems': 'admin-dashboard-foodItems.html',
        'recentOrders': 'admin-dashboard-recentOrders.html'
    }
    template_name = section_template.get(section, 'admin-dashboard.html')
    # return render(request,template_name)

    categories = category_table.objects.all()
    category_count = category_table.objects.count()
    foodItems = food_table.objects.all()
    foodItem_count = food_table.objects.count()
    customers = customer_table.objects.all()
    customer_count=customer_table.objects.count()
    return render(request, template_name, {'categories':categories, 'categoryCount':category_count, 'foodItems':foodItems, 'food_item_count':foodItem_count, 'customers':customers, 'customerCount':customer_count})





