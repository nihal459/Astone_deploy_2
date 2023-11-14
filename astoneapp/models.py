from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
import random
import string
from django.contrib.auth.models import AbstractUser
import random
import string
from django.utils import timezone


class Category(models.Model):
    category = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='category_images', blank=True, null=True)

    def __str__(self):
        return self.category
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return  url

class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Productimage(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='product_images', blank=True, null=True)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return  url



class Cardimage(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='card_images', blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return  url




class Product(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    images = models.ForeignKey(Productimage, on_delete=models.CASCADE, null=True,blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True)
    productcode = models.CharField(max_length=20, null=True, blank=True)
    advantages = models.TextField(null=True, blank=True)
    suitable_surface = models.TextField(null=True, blank=True)
    application = models.TextField(null=True, blank=True)
    additional_information = models.TextField(null=True, blank=True)
    youtube_link = models.URLField(null=True, blank=True)
    reward_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True )
    MRP = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    coupon_code = models.CharField(max_length=10, unique=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    sold = models.BooleanField(default=False, null=True)
    pdf = models.BooleanField(default=False, null=True)


    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        if not self.coupon_code:
            characters = string.ascii_letters + string.digits
            self.coupon_code = ''.join(random.choice(characters) for _ in range(6))
        
        if not self.qr_code:  # Generate and save QR code if not already present
            qrcode_img = qrcode.make(self.coupon_code)
            canvas = Image.new('RGB', (290, 290), 'white')
            draw = ImageDraw.Draw(canvas)
            canvas.paste(qrcode_img)
            fname = f'qr_code-{self.name}.png'
            buffer = BytesIO()
            canvas.save(buffer, 'PNG')
            self.qr_code.save(fname, File(buffer), save=False)
            canvas.close()
        
        super().save(*args, **kwargs)

    @property
    def imageURL(self):
        try:
            url = self.qr_code.url
        except:
            url = ''
        return  url
    


class User(AbstractUser):
    is_admin = models.BooleanField('is admin', default=False)
    is_staff = models.BooleanField('is staff', default=False)
    is_customer = models.BooleanField('is customer', default=False)
    name = models.CharField(max_length=100, default='User')
    mobile_number = models.CharField(max_length=20, default='Nil')
    bank_name = models.CharField(max_length=100, default='Nil')
    bank_account_number = models.CharField(max_length=50, default='Nil')
    ifsc_code = models.CharField(max_length=20, default='Nil')
    upi_id = models.CharField(max_length=100, default='Nil')
    pan_card_name = models.CharField(max_length=100, default='Nil')
    pan_card_number = models.CharField(max_length=20, default='Nil')
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    referral_code = models.CharField(max_length=6, unique=True, default='DEFAULTCODE')
    referred_by = models.CharField(max_length=100, null=True, blank=True)
    supercustomer = models.BooleanField(default=False, null=True)
    rewardamount = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    withdrawn = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.referral_code or self.referral_code == 'DEFAULTCODE':
            self.generate_referral_code()
        super(User, self).save(*args, **kwargs)

    def generate_referral_code(self):
        characters = string.ascii_letters + string.digits
        code_length = 6
        while True:
            referral_code = ''.join(random.choice(characters) for _ in range(code_length))
            if not User.objects.filter(referral_code=referral_code).exists() and referral_code != 'DEFAULTCODE':
                self.referral_code = referral_code
                break

    @property
    def imageURL(self):
        try:
            url = self.profile_picture.url
        except:
            url = ''
        return  url



class Qrcodescanner(models.Model):
    username = models.CharField(max_length=255, null=True, blank=True)
    userid = models.CharField(max_length=50, null=True, blank=True)
    couponcode = models.CharField(max_length=50, null=True, blank=True)
    rewardamount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    refferalcode = models.CharField(max_length=50, null=True, blank=True)
    scannedon = models.DateTimeField(auto_now_add=True)
    productid = models.CharField(max_length=50, null=True, blank=True)
    productname = models.CharField(max_length=255, null=True, blank=True)
    productprice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)

    
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('cancelled', 'Cancelled'),
    )
    paymentstatus = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='processing', null=True, blank=True)
    commissionstatus = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='processing', null=True, blank=True)


    def __str__(self):
        return str(self.username)


class Business(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    mobile_number = models.CharField(max_length=20,null=True,blank=True)
    email=models.EmailField(max_length=50,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    concern = models.CharField(max_length=100,null=True,blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.name)
    


class PdfCartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.product)
    

class Withdraw(models.Model):
    username = models.CharField(max_length=255, null=True, blank=True)
    userid = models.CharField(max_length=50, null=True, blank=True)
    rewardamount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    referralamount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    requestedon = models.DateTimeField(auto_now_add=True)
    paidon = models.DateTimeField(auto_now_add=True)
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('cancelled', 'Cancelled'),
    )
    paymentstatus = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='processing')

    def __str__(self):
        return str(self.username)
    