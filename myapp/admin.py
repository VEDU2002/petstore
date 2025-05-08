from django.contrib import admin
from myapp.models import pet,Cart,myOrder

# Register your models here.

class PetAdmin(admin.ModelAdmin):
    list_display=['id','name','age','breed','type','price','gender','description','petimage']
    list_filter=['type','price']

admin.site.register(pet,PetAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display=['id','uid','petid','quantity']
admin.site.register(Cart,CartAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display=['id','orderid','petid','userid','quantity']
    list_filter=['petid','userid']

admin.site.register(myOrder,OrderAdmin)
