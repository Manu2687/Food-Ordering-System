from django.contrib import admin
from Home_App.models import category_table, food_table, order_table, admin_table, customer_table

# Register your models here.
admin.site.register((category_table, food_table, order_table, admin_table, customer_table))