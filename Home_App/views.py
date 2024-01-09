from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from Home_App.models import customer_table, admin_table, category_table, food_table, order_table, reservation_table
# from django.contrib.auth import get_user_model
# from django.core.exceptions import ObjectDoesNotExist
# from django.http import JsonResponse
from Home_App.forms import *
from django.urls import reverse


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
        'reservation':'admin-dashboard-reservation.html',
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
    reservation=reservation_table.objects.all()
    return render(request, template_name, {'categories':categories, 'categoryCount':category_count, 'foodItems':foodItems, 'food_item_count':foodItem_count, 'customers':customers, 'customerCount':customer_count, 'reservations':reservation})



#  CRUD Operation at Admin-Dashboard

# ---------- Customer ----------
def edit_customer(request,customer_id):
    customer = get_object_or_404(customer_table,customer_id=customer_id)
    if request.method == 'POST':
        form = CustomerEditForm(request.POST)
        if form.is_valid():
            #updating customer details
            customer.first_name=form.cleaned_data['first_name']
            customer.last_name=form.cleaned_data['last_name']
            customer.email_id=form.cleaned_data['email_id']
            customer.dob=form.cleaned_data['dob']
            customer.phone_no=form.cleaned_data['phone_no']
            customer.user_id=form.cleaned_data['user_id']
            customer.password=form.cleaned_data['password']
            customer.save()
            return redirect(reverse('admin-dashboard-section',kwargs={'section':'customers'}))
    else:
            form = CustomerEditForm(initial={
                'first_name':customer.first_name,
                'last_name':customer.last_name,
                'email_id':customer.email_id,
                'dob':customer.dob,
                'phone_no':customer.phone_no,
                'user_id':customer.user_id,
                'password':customer.password
            })

    return render(request,'admin-dashboard-customer-edit-modal.html',{'form':form,'customer_id':customer_id})
    
def delete_customer(request,customer_id):
    customer = get_object_or_404(customer_table,customer_id=customer_id)
    customer.delete()
    return redirect(reverse('admin-dashboard-section',kwargs={'section':'customers'}))

def add_customer(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('admin-dashboard-section',kwargs={'section':'customers'}))
    return render(request,'admin-dashboard-customer-add.html',{'form':form})

    

# ---------- Category ----------    
def edit_category(request, category_id):
    category = get_object_or_404(category_table, category_id=category_id)

    if request.method == 'POST':
        form = CategoryEditForm(request.POST)
        if form.is_valid():
            # Update category fields based on form data
            category.category_title = form.cleaned_data['category_title']
            category.feature = form.cleaned_data['feature']
            category.save()

            # display success message
            messages.success(request, ' Category details updated successfully.')
            return redirect(reverse('admin-dashboard-section',kwargs={'section':'categories'}))  
    else:
        form = CategoryEditForm(initial={
            'category_title': category.category_title,
            'feature': category.feature,
        })

    return render(request, 'admin-dashboard-category-edit-modal.html', {'form': form, 'category_id': category_id})


def delete_category(request, category_id):
    category = get_object_or_404(category_table,category_id=category_id)
    category.delete()

    # displaying message
    messages.success(request,'Category deleted successfully.')
    return redirect(reverse('admin-dashboard-section', kwargs={'section':'categories'}))


def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Category added successfully')
            return redirect(reverse('admin-dashboard-section', kwargs={'section':'categories'}))
        
    return render(request,'admin-dashboard-category-add.html',{'form':form})


# ---------- Food Items ----------    
def edit_foodItems(request, food_id):
    food = get_object_or_404(food_table, food_id=food_id)

    if request.method == 'POST':
        form = FoodItemsEditForm(request.POST)
        if form.is_valid():
            # Update category fields based on form data
            food.food_title = form.cleaned_data['food_title']
            food.description = form.cleaned_data['description']
            food.price = form.cleaned_data['price']
            food.img_name = form.cleaned_data['img_name']
            category_id = form.cleaned_data['category_id']
            category = get_object_or_404(category_table,category_id=category_id)
            food.category_id=category
            food.feature = form.cleaned_data['feature']
            food.save()

            # display success message
            return redirect(reverse('admin-dashboard-section',kwargs={'section':'foodItems'}))  
    else:
        form = FoodItemsEditForm(initial={
            'food_title': food.food_title,
            'description': food.description,
            'price': food.price,
            'img_name': food.img_name,
            'category_id': food.category_id,
            'feature': food.feature,
        })

    return render(request, 'admin-dashboard-foodItems-edit-modal.html', {'form': form, 'food_id': food_id})


def delete_foodItems(request, food_id):
    food = get_object_or_404(food_table,food_id=food_id)
    food.delete()
    return redirect(reverse('admin-dashboard-section', kwargs={'section':'foodItems'}))


def add_foodItems(request):
    form = FoodItemsForm()
    if request.method == 'POST':
        form = FoodItemsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('admin-dashboard-section', kwargs={'section':'foodItems'}))
        
    return render(request,'admin-dashboard-foodItems-add.html',{'form':form})


#  ----- Reservation -----
def approve_reservation_request(request, reservation_id):
    reservation = get_object_or_404(reservation_table, reservation_id=reservation_id)
    reservation.status='approved'
    reservation.save()
    return redirect(reverse('admin-dashboard-section',kwargs={'section':'reservation'}))

def deny_reservation_request(request,reservation_id):
    reservation = get_object_or_404(reservation_table,reservation_id=reservation_id)
    reservation.status='denied'
    reservation.save()
    return redirect(reverse('admin-dashboard-section',kwargs={'section':'reservation'}))
