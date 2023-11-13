
from django.contrib import admin
from .models import *
from astoneapp.models import User



admin.site.register(User)
admin.site.register(Product)
admin.site.register(Qrcodescanner)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Productimage)
admin.site.register(Business)
admin.site.register(PdfCartItem)
admin.site.register(Withdraw)

