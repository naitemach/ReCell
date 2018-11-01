from django.contrib import admin

from .models import *

admin.site.register(Seller)
admin.site.register(Buyer)
admin.site.register(Item)
admin.site.register(Inventory)
admin.site.register(Location)
admin.site.register(FeedBack)
admin.site.register(Wallet)
admin.site.register(ItemDesc)
admin.site.register(Order)