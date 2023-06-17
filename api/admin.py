from django.contrib import admin
from .models import UserProfile,Product,Cart,CartItem,User

admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.site_header = 'Bit64 Administration'
admin.site.site_title = 'Bit64'
admin.site.index_title = 'Welcome'