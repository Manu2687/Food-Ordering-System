from django.db import models
from django.core.validators import RegexValidator


# Create your models here.

#Category
class category_table(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_title = models.CharField(max_length=55)
    img_name = models.CharField(max_length = 55)
    feature = models.CharField(max_length = 90)
    active = models.CharField(max_length = 9)

#Order
class order_table(models.Model):
    order_id = models.AutoField(primary_key=True)
    # food_title = models.CharField(primary_key=True, max_length=20)
    category_id=models.ForeignKey(category_table,on_delete=models.CASCADE)
    price = models.IntegerField()
    qty = models.IntegerField()
    total = models.IntegerField()
    date = models.DateField()
    status = models.CharField(max_length=20)
    cust_name = models.CharField(max_length=20)
    cust_contact = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d+$', #regex for only numeric digits
                message='Phone number must contain only numeric digits.',
                code='invalid phone number'
            ),
        ]
    )


#Food
class food_table(models.Model):
    food_id = models.AutoField(primary_key=True)
    food_title = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    price = models.IntegerField()
    img_name = models.CharField(max_length=20)
    category_id = models.ForeignKey(category_table,on_delete=models.CASCADE)
    feature = models.CharField(max_length=20)
    active = models.CharField(max_length=10) 
    


#Admins 
class admin_table(models.Model):
    is_admin = models.BooleanField(default=True)
    admin_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=20)
    user_name = models.CharField(max_length=30)
    password = models.CharField(max_length=50)

# Customer Table
class customer_table(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email_id = models.CharField(max_length=50)
    dob = models.CharField(max_length=10)
    phone_no = models.CharField(max_length=10)
    user_id = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

