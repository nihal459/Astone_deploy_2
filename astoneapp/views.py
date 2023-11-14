from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
import string
import random
import qrcode
from PIL import Image, ImageDraw
from io import BytesIO
from django.core.files import File
from django.db.utils import IntegrityError
from django.db.models import Q
from django.db.models import Count
from django.db.models import F
from django.db.models import Sum

##################################################################################################################################################################

############## FOR ALL USERS ##############

def index(request):
    categories = Category.objects.all()

    # Get all products
    products = Product.objects.all()

    # Create a dictionary to store unique products by name
    unique_products_dict = {}
    for product in products:
        unique_products_dict[product.name] = product

    # Convert the dictionary values back to a list of unique products
    unique_products = list(unique_products_dict.values())

    context = {'categories': categories, 'products': unique_products}
    return render(request, 'general/index.html', context)

def categories(request):
    categories = Category.objects.all()
    context = {'categories': categories}

    return render(request, 'general/categories.html', context)

def subcategories(request, pk):
    category = Category.objects.get(pk=pk)
    subcategories = Subcategory.objects.filter(category=category)

    return render(request, 'general/subcategories.html', {'category': category, 'subcategories': subcategories})



def subproducts(request, pk):
    subcategory = Subcategory.objects.get(pk=pk)
    products = Product.objects.filter(subcategory=subcategory)

    unique_products = {}
    for product in products:
        unique_products[product.name] = product

    return render(request, 'general/subproducts.html', {'subcategory': subcategory, 'products': unique_products.values()})


# def (request, pk):
def product(request, pk):

    products = Product.objects.get(pk=pk)
    context = {'products':products}

    return render(request, 'general/product.html', context)


# def products(request):
#     products = Product.objects.all()
#     unique_products_dict = {}
#     for product in products:
#         unique_products_dict[product.name] = product

#     # Convert the dictionary values back to a list of unique products
#     unique_products = list(unique_products_dict.values())

#     context = {'products':unique_products}
#     return render(request, 'general/products.html', context)

from django.db.models import Q  # Import the Q object

def products(request):
    search_query = request.GET.get('search_query')

    # If a search query is provided, filter products by name; otherwise, get all products
    if search_query:
        products = Product.objects.filter(Q(name__icontains=search_query))
    else:
        products = Product.objects.all()

    unique_products_dict = {}
    for product in products:
        unique_products_dict[product.name] = product

    # Convert the dictionary values back to a list of unique products
    unique_products = list(unique_products_dict.values())

    context = {'products': unique_products}
    return render(request, 'general/products.html', context)



def contactus(request):
    return render(request, 'general/contactus.html')


def contact_enquiry(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        concern = request.POST.get('concern')
        description = request.POST.get('description')


    business = Business.objects.create(name=name, email=email, concern=concern, description=description)

    messages.success(request, 'Enquiry Submitted')

    return redirect('contactus')



def aboutus(request):
    return render(request, 'general/aboutus.html')

def gallery(request):
    return render(request, 'general/gallery.html')

def adminregister(request):
    return render(request, 'general/adminregister.html')

def pdf2(request):
    return render(request, 'astone_admin/pdf2.html')

def admin_registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return render(request, 'general/adminregister.html')

        
        user = User.objects.create_user(
            username=username,
            password=password,
            is_admin=True,
        )
                
        return redirect('index') 
    
    return render(request, 'general/adminregister.html')


from django.db.models import Q

def view_requests(request):
    query = request.GET.get('query')
    requests = Withdraw.objects.exclude(paymentstatus='Paid')

    if query:
        requests = requests.filter(Q(username__icontains=query) | Q(userid__icontains=query))

    context = {'requests': requests}
    return render(request, 'astone_admin/view_requests.html', context)

def add_staff(request):
    return render(request, 'astone_admin/add_staff.html')

def cash_error(request):
    return render(request, 'astone_admin/cash_error.html')

def viewrewardrequestsingle(request, pk):
    rewards = Withdraw.objects.filter(userid=pk)
    context = {'rewards':rewards}
    return render(request, 'astone_admin/viewrewardrequestsingle.html', context)

# from decimal import Decimal

# def update_request(request, pk):
#     get_reward_req = get_object_or_404(Withdraw, pk=pk)
#     amount_requested = get_reward_req.rewardamount

#     getuser = get_reward_req.userid
#     user = get_object_or_404(User, pk=getuser)

#     totatreward = user.rewardamount
#     balance = user.balance

#     if request.method == "POST":
#         payment_status = request.POST.get('payment_status', '') 

#         if amount_requested <= balance:
#             if payment_status == 'Paid':
#                     user.withdrawn = user.withdrawn + amount_requested
#                     user.balance = totatreward - user.withdrawn
#                     user.save()

#             get_reward_req.paymentstatus = payment_status
#             get_reward_req.save()
#             print("user:", user)
#             print("user.balance:", user.balance)
#             print("amount_requested:", amount_requested)

#             return redirect('view_users')
#         else:
#             messages.error(request, 'Amount requested greater than users reward balance')
#             return render(request, 'astone_admin/cash_error.html')
#     else:
#         context = {
#             'get_reward_req': get_reward_req,
#         }
#         return render(request, 'astone_admin/update_request.html', context)





from decimal import Decimal

def update_request(request, pk):
    get_reward_req = get_object_or_404(Withdraw, pk=pk)
    amount_requested = get_reward_req.rewardamount

    getuser = get_reward_req.userid
    user = get_object_or_404(User, pk=getuser)
    user_id = user.pk

    user_referral_code = user.referral_code
    matching_referrals = Qrcodescanner.objects.filter(refferalcode=user_referral_code)
    matching_userid = Qrcodescanner.objects.filter(userid=user_id)

    total_reward_amount = matching_userid.aggregate(Sum('rewardamount'))['rewardamount__sum'] or 0
    user.rewardamount = total_reward_amount
    user.balance = total_reward_amount - user.withdrawn
    user.save()
    
    totatreward = user.rewardamount
    balance = user.balance

    if request.method == "POST":
        payment_status = request.POST.get('payment_status', '') 

        if amount_requested <= balance:
            if payment_status == 'Paid':
                    user.withdrawn = user.withdrawn + amount_requested
                    user.balance = totatreward - user.withdrawn
                    user.save()

            get_reward_req.paymentstatus = payment_status
            get_reward_req.save()
            print("user:", user)
            print("user.balance:", user.balance)
            print("amount_requested:", amount_requested)

            return redirect('view_users')
        else:
            messages.error(request, 'Amount requested greater than users reward balance')
            return render(request, 'astone_admin/cash_error.html')
    else:
        context = {
            'get_reward_req': get_reward_req,
            'totalreward':totatreward,
            'balance':balance,
            'user':user,
            'amount_requested':amount_requested,
        }
        return render(request, 'astone_admin/update_request.html', context)








def delete_request(request, pk):
    req = get_object_or_404(Withdraw, pk=pk)
    req.delete()
    return redirect('view_requests')

def addstaff(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return render(request, 'astone_admin/add_staff.html')

        
        user = User.objects.create_user(
            username=username,
            password=password,
            is_staff=True,
        )
                
        return redirect('view_staff') 
    
    return render(request, 'astone_admin/add_staff.html')


def view_staff(request):
    staffs = User.objects.filter(is_staff=True).exclude(is_superuser=True)
    context = {'staffs': staffs}
    return render(request, 'astone_admin/view_staff.html', context)


def delete_staff(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('view_staff')


def astonestaff(request):
    if request.method == 'POST':
        username_or_number = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username_or_number).first()
        
        if user is not None and user.check_password(password) and user.is_staff:
            login(request, user)
            return redirect('astoneadminhome')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'astone_staff/astonestaff.html')

############## ADMIN ##############################################################################################################################

def astoneadmin(request):
    if request.method == 'POST':
        username_or_number = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username_or_number).first()
        
        if user is not None and user.check_password(password) and user.is_admin:
            login(request, user)
            return redirect('astoneadminhome')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'astone_admin/astoneadmin.html')


def SignOut2(request):
     logout(request)
     return redirect('index')

from django.db.models import Count

def astoneadminhome(request):
    top_referral_codes = (
        Qrcodescanner.objects
        .values('refferalcode')
        .annotate(code_count=Count('userid', distinct=True))
        .order_by('-code_count')
        [:11]
    )

    return render(request, 'astone_admin/astoneadminhome.html', {'top_referral_codes': top_referral_codes})


def add_productimage(request):
    productimage = Productimage.objects.all()
    context = {'productimage':productimage}
    return render(request, 'astone_admin/add_productimage.html', context)

def view_enquiry(request):
    enquiry = Business.objects.all()
    context = {'enquiry':enquiry}
    return render(request, 'astone_admin/view_enquiry.html', context)


# def view_referral(request):
#     top_referral_codes = Qrcodescanner.objects.values('refferalcode').annotate(code_count=Count('refferalcode')).order_by('-code_count')
#     return render(request, 'astone_admin/view_referral.html', {'top_referral_codes': top_referral_codes})


from django.db.models import Count

def view_referral(request):
    top_referral_codes = (
        Qrcodescanner.objects
        .values('refferalcode')
        .annotate(code_count=Count('userid', distinct=True))
        .order_by('-code_count')
    )
    return render(request, 'astone_admin/view_referral.html', {'top_referral_codes': top_referral_codes})



def addproductimage(request):
    a = request.POST.get("name")
    b = request.FILES["image"]
    product = Productimage.objects.create(name=a, image=b)
    return redirect('add_productimage')


def edit_productimage(request, pk):
    get_category = get_object_or_404(Productimage, pk=pk)
    if request.method == "POST":
        new_category = request.POST['name']

        # Check if a new image was provided
        new_image = request.FILES.get('image')
        if new_image:
            get_category.image = new_image

        get_category.name = new_category
        get_category.save()
        return redirect('add_productimage')
    else:
        context = {
            'get_category': get_category,
        }
        return render(request, 'astone_admin/edit_productimage.html', context)

def delete_productimage(request, pk):
    category = get_object_or_404(Productimage, pk=pk)
    category.delete()
    return redirect('add_productimage')

 
def addproduct(request):
    productimage= Productimage.objects.all()
    category = Category.objects.all()
    subcategory = Subcategory.objects.all()
    context = {'category':category, 'subcategory':subcategory, 'productimage':productimage}
    return render(request, 'astone_admin/addproduct.html', context)



def generate_coupon_code():
    # Generate a unique coupon code
    while True:
        characters = string.ascii_letters + string.digits
        coupon_code = ''.join(random.choice(characters) for _ in range(6))
        
        # Check if the coupon code already exists in the Product table
        if not Product.objects.filter(coupon_code=coupon_code).exists():
            return coupon_code

def generate_qr_code(coupon_code):
    # Generate a QR code with the coupon code content
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(coupon_code)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    return img


def add_product(request):

    try:

        if request.method == "POST":
            quantity = int(request.POST.get("quantity", 1))
            products = []

            for index, _ in enumerate(range(quantity)):
                a = request.POST.get("productName")
                b = request.POST.get("description")
                c = request.POST.get("category")
                d = request.POST.get("image")
                e = request.POST.get("subcategory")
                f = request.POST.get("code")
                g = request.POST.get("advantages")
                h = request.POST.get("surface")
                i = request.POST.get("application")
                j = request.POST.get("info")
                k = request.POST.get("youtubeLink")
                l = request.POST.get("rewardAmount")
                m = request.POST.get("mrp")
                n = Category.objects.filter(category=c).first()
                o = Subcategory.objects.filter(name=e).first()
                p = Productimage.objects.filter(name=d).first()

                # Generate a unique coupon code for each product
                coupon_code = generate_coupon_code()  # Use the function to generate the code

                # Generate a QR code image
                qr_code_image = generate_qr_code(coupon_code)

                product = Product(
                    name=a, description=b, category=n, subcategory=o, productcode=f,
                    advantages=g, suitable_surface=h, application=i, additional_information=j,
                    youtube_link=k, reward_amount=l, MRP=m, images=p, coupon_code=coupon_code  # Use the generated code
                )

                # Save the QR code image to the product's qr_code field with a unique filename
                img_buffer = BytesIO()
                qr_code_image.save(img_buffer, format="PNG")
                filename = f'qr_code-{coupon_code}.png'  # Use coupon code in the filename
                product.qr_code.save(filename, File(img_buffer))

                products.append(product)

            with transaction.atomic():
                Product.objects.bulk_create(products)

    except IntegrityError:
                pass

    return redirect('view_product')

def view_product(request):
    query = request.GET.get('query')
    productcode = request.GET.get('productcode')
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')

    n = Category.objects.filter(category=category).first()
    o = Subcategory.objects.filter(name=subcategory).first()

    products = Product.objects.all()
    pcategory = Category.objects.all()
    psubcategory = Subcategory.objects.all()

    if query:
        products = products.filter(name__icontains=query)
        
    if productcode:
        products = products.filter(productcode__icontains=productcode)

    if category:
        products = products.filter(category=n)

    if subcategory:
        products = products.filter(subcategory=o)

    if price_from and price_to:
        min_price, max_price = float(price_from), float(price_to)
        products = products.filter(MRP__gte=min_price, MRP__lte=max_price)

    # Remove duplicate products based on name
    unique_products = {}
    for product in products:
        unique_products[product.name] = product

    # Calculate the count of unique products
    num_unique_products = len(unique_products)

    context = {
        'products': unique_products.values(),  # Convert back to a list of unique products
        'query': query,
        'productcode': productcode,
        'category': category,
        'subcategory': subcategory,
        'price_from': price_from,
        'price_to': price_to,
        'pcategory': pcategory,
        'psubcategory': psubcategory,
        'num_unique_products': num_unique_products,  # Add the count to the context
    }
    return render(request, 'astone_admin/view_product.html', context)




def editproduct(request, pk):
    category = Category.objects.all()
    subcategory = Subcategory.objects.all()
    image = Productimage.objects.all()
    get_product = get_object_or_404(Product, pk=pk)
    
    if request.method == "POST":
        new_name = request.POST['name']
        new_description = request.POST['description']
        new_image = request.POST['image']
        new_category = request.POST['category']
        new_subcategory = request.POST['subcategory']
        new_productcode = request.POST['productcode']
        new_advantages = request.POST['advantages']
        new_suitable_surface = request.POST['suitable_surface']
        new_application = request.POST['application']
        new_additional_information = request.POST['additional_information']
        new_youtube_link = request.POST['youtube_link']
        new_reward_amount = request.POST['reward_amount']
        new_MRP = request.POST['MRP']
        n = Category.objects.filter(category=new_category).first()
        o = Subcategory.objects.filter(name=new_subcategory).first()
        p = Productimage.objects.filter(name=new_image).first()

        # Check if a new image was provided

        get_product.name = new_name
        get_product.description = new_description
        get_product.images = p
        get_product.category = n
        get_product.subcategory = o
        get_product.productcode = new_productcode
        get_product.advantages = new_advantages
        get_product.suitable_surface = new_suitable_surface
        get_product.application = new_application
        get_product.additional_information = new_additional_information
        get_product.youtube_link = new_youtube_link
        get_product.reward_amount = new_reward_amount
        get_product.MRP = new_MRP

        get_product.save()
        
        # Find all copies of the product based on the product code
        copies = Product.objects.filter(productcode=new_productcode)
        
        # Update attributes of all copies to match the edited product
        for copy in copies:
            copy.name = new_name
            copy.description = new_description
            copy.images = p
            copy.category = n
            copy.subcategory = o
            copy.advantages = new_advantages
            copy.suitable_surface = new_suitable_surface
            copy.application = new_application
            copy.additional_information = new_additional_information
            copy.youtube_link = new_youtube_link
            copy.reward_amount = new_reward_amount
            copy.MRP = new_MRP
            copy.save()
        
        return redirect('view_product')
    
    else:
        context = {
            'get_product': get_product,
            'category': category,
            'subcategory': subcategory,
            'productimage': image
        }
        return render(request, 'astone_admin/editproduct.html', context)


# def viewproductsingle(request,pk):
#     try:
#         get_product = get_object_or_404(Product, pk=pk)
#         context = {'get_product':get_product}
#     except Http404:
#         # If the user is not found, raise Http404 with a custom message
#         context = {
#             'error_message': 'Product Sold Out & Cleared From Inventory.'
#         }
#         return render(request, 'astone_admin/viewproductsingle.html', context)   




from django.http import Http404, HttpResponse

def viewproductsingle(request, pk):
    try:
        get_product = get_object_or_404(Product, pk=pk)
        context = {'get_product': get_product}
    except Http404:
        # If the product is not found, return an error message as an HttpResponse
        error_message = 'Product Sold Out & Cleared From Inventory.'
        return HttpResponse(error_message, content_type="text/plain")

    return render(request, 'astone_admin/viewproductsingle.html', context)


def delete_user1(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('view_users')

def delete_user2(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('view_supercustomer')

def make_supercustomer(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.supercustomer = True
    user.save()
    return redirect('view_users')

def make_normalcustomer(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.supercustomer = False
    user.save()
    return redirect('view_supercustomer')

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    productcode = product.productcode  
    product.delete()
    Product.objects.filter(productcode=productcode).delete()
    messages.success(request, 'Product deleted successfully')

    return redirect('view_product')


def add_category(request):
    category = Category.objects.all()
    context = {'category':category}
    return render(request, 'astone_admin/add_category.html', context)

def addcategory(request):
    a = request.POST.get("category")
    b = request.FILES["image"]
    try:
        category = Category.objects.create(category=a, image=b)
    except IntegrityError:
        messages.error(request, 'Category already exists.')
        
    return redirect('add_category')

def edit_category(request, pk):
    get_category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        new_category = request.POST['category']

        # Check if a new image was provided
        new_image = request.FILES.get('image')
        if new_image:
            get_category.image = new_image

        get_category.category = new_category
        get_category.save()
        return redirect('add_category')
    else:
        context = {
            'get_category': get_category,
        }
        return render(request, 'astone_admin/edit_category.html', context)


def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('add_category')



from django.db.models import Q

def view_rewards(request):
    search_query = request.GET.get('query')

    # Initial queryset to get all objects not having 'Paid' payment status
    rewards = Qrcodescanner.objects.exclude(paymentstatus='paid')

    if search_query:
        # Add filters to search for the provided query in multiple fields
        rewards = rewards.filter(
            Q(username__icontains=search_query) |
            Q(couponcode__icontains=search_query) |
            Q(refferalcode__icontains=search_query) |
            Q(productname__icontains=search_query)
        )

    total_reward_amount = rewards.aggregate(total_reward=Sum('rewardamount'))['total_reward']

    context = {'rewards': rewards, 'total_reward_amount':total_reward_amount}
    return render(request, 'astone_admin/view_rewards.html', context)




def view_paidrewards(request):
    # Filter objects where paymentstatus is 'Paid'
    query = request.GET.get('query')

    paid_rewards = Withdraw.objects.filter(paymentstatus='Paid')
    if query:
        paid_rewards = paid_rewards.filter(Q(username__icontains=query) | Q(userid__icontains=query))

    # Calculate the sum of rewardamount for paid_rewards
    total_paid_rewardamount = paid_rewards.aggregate(total_rewardamount=Sum('rewardamount'))

    # Extract the sum from the aggregation result
    total_sum = total_paid_rewardamount['total_rewardamount'] or 0

    context = {'rewards': paid_rewards, 'total_sum': total_sum}
    return render(request, 'astone_admin/view_paidrewards.html', context)


def view_users(request):
    query = request.GET.get('query')
    
    # Start with all customers and filter based on the query
    customers = User.objects.filter(is_customer=True, supercustomer=False)
    
    if query:
        # Use Q objects to create an OR condition for username and name
        customers = customers.filter(Q(username__icontains=query) | Q(name__icontains=query)| Q(referral_code__icontains=query))
    
    context = {'users': customers, 'query': query}
    return render(request, 'astone_admin/view_users.html', context)


def view_supercustomer(request):
    query = request.GET.get('query')
    
    # Start with all customers and filter based on the query
    customers = User.objects.filter(is_customer=True, supercustomer=True)
    
    if query:
        # Use Q objects to create an OR condition for username and name
        customers = customers.filter(Q(username__icontains=query) | Q(name__icontains=query)| Q(referral_code__icontains=query))
    
    context = {'users': customers, 'query': query}
    return render(request, 'astone_admin/view_supercustomer.html', context)


from django.db.models import Count

def viewusersingle(request, pk):
    try:
        get_user = get_object_or_404(User, pk=pk)
        user_referral_code = get_user.referral_code
        user_id = get_user.pk

        matching_referrals = Qrcodescanner.objects.filter(refferalcode=user_referral_code)
        matching_userid = Qrcodescanner.objects.filter(userid=user_id)

        total_reward_amount = matching_userid.aggregate(Sum('rewardamount'))['rewardamount__sum'] or 0
        get_user.rewardamount = total_reward_amount
        get_user.balance = total_reward_amount - get_user.withdrawn
        get_user.save()

        # Count the total number of times the referral code has been used
        total_referral_usage = matching_referrals.count()
        total_rewards = matching_userid.count()

        # Count the number of unique users that used this user's referral code
        unique_users_count = matching_referrals.values('userid').distinct().count()

        context = {
            'get_user': get_user,
            'matching_referrals': matching_referrals,
            'matching_userid': matching_userid,
            'total_reward_amount': total_reward_amount,
            'total_referral_usage': total_referral_usage,
            'unique_users_count': unique_users_count,
            'total_rewards':total_rewards,
        }

        return render(request, 'astone_admin/viewusersingle.html', context)

    except Http404:
        # If the user is not found, raise Http404 with a custom message
        context = {
            'error_message': 'User not found.'
        }
        return render(request, 'astone_admin/viewusersingle.html', context)


from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import User, Qrcodescanner

def viewusersingle2(request, referral_code):
    try:
        get_user = get_object_or_404(User, referral_code=referral_code)
        user_referral_code = get_user.referral_code
        matching_referrals = Qrcodescanner.objects.filter(refferalcode=user_referral_code)
        user_id = get_user.pk
        matching_userid = Qrcodescanner.objects.filter(userid=user_id)
        total_reward_amount = matching_userid.aggregate(Sum('rewardamount'))['rewardamount__sum'] or 0
        get_user.rewardamount = total_reward_amount
        total_referral_usage = matching_referrals.count()
        total_rewards = matching_userid.count()
        unique_users_count = matching_referrals.values('userid').distinct().count()

        context = {
            'get_user': get_user,
            'matching_referrals': matching_referrals,
            'matching_userid': matching_userid,
            'total_reward_amount': total_reward_amount,
            'total_referral_usage': total_referral_usage,
            'unique_users_count': unique_users_count,
            'total_rewards':total_rewards,
        }

        return render(request, 'astone_admin/viewusersingle2.html', context)

    except Http404:
        # If the user is not found, raise Http404 with a custom message
        context = {
            'error_message': 'User not found.'
        }
        return render(request, 'astone_admin/viewusersingle2.html', context)




def subcategory(request):
    category = Category.objects.all()
    subcategory = Subcategory.objects.all()
    context = {'subcategory':subcategory, 'category':category}
    return render(request, 'astone_admin/subcategory.html', context)


def add_subcategory(request):
    a = request.POST.get("category")
    b = request.POST.get("subcategory")
    c = Category.objects.filter(category=a).first()
    category = Subcategory.objects.create(category=c, name=b)
    return redirect('subcategory')

def edit_subcategory(request, pk):
    get_subcategory = get_object_or_404(Subcategory, pk=pk)
    if request.method == "POST":
        new_subcategory = request.POST['subcategory']

        get_subcategory.name = new_subcategory
        get_subcategory.save()
        return redirect('subcategory')
    else:
        context = {
            'get_subcategory': get_subcategory,
        }
        return render(request, 'astone_admin/edit_subcategory.html', context)

def delete_subcategory(request, pk):
    subcategory = get_object_or_404(Subcategory, pk=pk)
    subcategory.delete()
    return redirect('subcategory')




def add_to_pdf_cart(request):
    if request.method == 'POST':
        selected_item_ids = request.POST.getlist('selected_items')
        for item_id in selected_item_ids:
            product = Product.objects.get(pk=item_id)
            pdf_cart_item, created = PdfCartItem.objects.get_or_create(
                product=product
            )
        messages.success(request, 'Products added to PDF')

        return redirect('view_unsoldproducts')
    else:
        # Handle GET request or other cases here
        pass

def delete_pdf(request):
    
    PdfCartItem.objects.all().delete()
    messages.success(request, 'PDF Cart Cleared')
    return redirect('make_pdf')

def delete_singlepdf(request, pk):
    pdf = get_object_or_404(PdfCartItem, pk=pk)
    pdf.delete()
    messages.success(request, 'PDF Cart Cleared')
    return redirect('make_pdf')



from django.db.models import Count

def delete_soldproducts(request):
    if request.method == 'POST':
        selected_item_ids = request.POST.getlist('selected_items')
        
        # Get the products corresponding to the selected_item_ids
        selected_products = Product.objects.filter(pk__in=selected_item_ids)
        
        # Create a dictionary to store the count of each product code
        productcode_count = {}
        
        for product in selected_products:
            productcode = product.productcode
            if productcode in productcode_count:
                productcode_count[productcode] += 1
            else:
                productcode_count[productcode] = 1
        
        # Loop through the selected products and delete all except one for each product code
        for productcode, count in productcode_count.items():
            if count > 1:
                # Get the products with the same product code
                products_to_delete = selected_products.filter(productcode=productcode)
                # Keep one and delete the rest
                products_to_delete.exclude(pk=products_to_delete.first().pk).delete()

        messages.success(request, 'Inventory Cleared')

        return redirect('view_soldproducts')
    else:
        pass



def make_pdf(request):
    query = request.GET.get('query')
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')

    n = Category.objects.filter(category=category).first()
    o = Subcategory.objects.filter(name=subcategory).first()

    products = PdfCartItem.objects.all()  
    pcategory = Category.objects.all()
    psubcategory = Subcategory.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category:
        products = products.filter(category=n)

    if subcategory:
        products = products.filter(subcategory=o)

    if price_from and price_to:
        min_price, max_price = float(price_from), float(price_to)
        products = products.filter(MRP__gte=min_price, MRP__lte=max_price)

    context = {
        'products': products,
        'query': query,
        'category': category,
        'subcategory': subcategory,
        'price_from': price_from,
        'price_to': price_to,
        'pcategory': pcategory,
        'psubcategory': psubcategory,
    }
    return render(request, 'astone_admin/make_pdf.html', context)

from django.db.models import Q



def view_unsoldproducts(request):
    query = request.GET.get('query')
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')

    n = Category.objects.filter(category=category).first()
    o = Subcategory.objects.filter(name=subcategory).first()

    products = Product.objects.filter(sold=False)  # Filter for unsold products
    pcategory = Category.objects.all()
    psubcategory = Subcategory.objects.all()

    if query:
        # Search by both name and product code using Q objects
        products = products.filter(
            Q(name__icontains=query) |
            Q(productcode__icontains=query) |
            Q(coupon_code__icontains=query)
        )

    if category:
        products = products.filter(category=n)

    if subcategory:
        products = products.filter(subcategory=o)

    if price_from and price_to:
        min_price, max_price = float(price_from), float(price_to)
        products = products.filter(MRP__gte=min_price, MRP__lte=max_price)

    num_products = products.count()

    context = {
        'products': products,
        'query': query,
        'category': category,
        'subcategory': subcategory,
        'price_from': price_from,
        'price_to': price_to,
        'pcategory': pcategory,
        'psubcategory': psubcategory,
        'num_products':num_products,
    }
    return render(request, 'astone_admin/view_unsoldproducts.html', context)




def view_soldproducts(request):
    query = request.GET.get('query')
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')

    n = Category.objects.filter(category=category).first()
    o = Subcategory.objects.filter(name=subcategory).first()

    products = Product.objects.filter(sold=True)  # Filter for sold products
    pcategory = Category.objects.all()
    psubcategory = Subcategory.objects.all()

    if query:
        # Search by product name, product code, or coupon code
        products = products.filter(
            Q(name__icontains=query) |
            Q(productcode__icontains=query) |
            Q(coupon_code__icontains=query)
        )

    if category:
        products = products.filter(category=n)

    if subcategory:
        products = products.filter(subcategory=o)

    if price_from and price_to:
        min_price, max_price = float(price_from), float(price_to)
        products = products.filter(MRP__gte=min_price, MRP__lte=max_price)

    num_products = products.count()

    context = {
        'products': products,
        'query': query,
        'category': category,
        'subcategory': subcategory,
        'price_from': price_from,
        'price_to': price_to,
        'pcategory': pcategory,
        'psubcategory': psubcategory,
        'num_products': num_products,
    }
    return render(request, 'astone_admin/view_soldproducts.html', context)




def update_reward(request, pk):
    get_reward = get_object_or_404(Qrcodescanner, pk=pk)
    if request.method == "POST":
        new_status = request.POST['status']
        new_commission = request.POST['commission']

        get_reward.commission = new_commission
        get_reward.paymentstatus = new_status
        get_reward.save()
        return redirect('view_rewards')
    else:
        context = {
            'get_reward': get_reward,
        }
        return render(request, 'astone_admin/update_reward.html', context)


from django.db.models import Q

def referralpayment(request):
    # Get all records with a non-None referralcode
    all_records = Qrcodescanner.objects.exclude(refferalcode__isnull=True)

    # Extract the query entered by the user
    query = request.GET.get('query')

    # Apply the search filter
    if query:
        all_records = all_records.filter(
            Q(username__icontains=query) | Q(refferalcode__icontains=query) | Q(userid__icontains=query)
        )

    # Extract the selected payment status from the filter dropdown
    payment_status = request.GET.get('category')

    # Apply the payment status filter
    if payment_status:
        all_records = all_records.filter(commissionstatus=payment_status)

    # Create a dictionary to store unique users and their details, separated by commissionstatus
    unique_user_dict = {'Paid': {}, 'processing': {}}

    # Process the records to keep only the latest record for each user
    for record in all_records:
        userid = record.userid
        commissionstatus = record.commissionstatus
        if userid in unique_user_dict[commissionstatus]:
            if record.scannedon > unique_user_dict[commissionstatus][userid].scannedon:
                unique_user_dict[commissionstatus][userid] = record
        else:
            unique_user_dict[commissionstatus][userid] = record

    # Combine the unique user details while maintaining the processing records on top
    unique_user_details = list(unique_user_dict['processing'].values()) + list(unique_user_dict['Paid'].values())

    context = {
        'unique_user_details': unique_user_details,
        'selected_payment_status': payment_status,  # Pass the selected payment status to the template
    }
    return render(request, 'astone_admin/referralpayment.html', context)




from django.db.models import Q

def view_commissions(request):
    # Filter objects where paymentstatus is 'Paid' and commissionstatus is not 'Paid'
    paid_rewards = Qrcodescanner.objects.filter(paymentstatus='Paid').exclude(commissionstatus='Paid')
    
    context = {'rewards': paid_rewards}
    return render(request, 'astone_admin/view_commissions.html', context)




def update_commission(request, pk):
    get_reward = get_object_or_404(Qrcodescanner, pk=pk)
    user = get_reward.userid
    
    if request.method == "POST":
        amount = request.POST['amount']
        new_commission = request.POST['commission']

        # Update the commission and commissionstatus for all users with the same userid
        Qrcodescanner.objects.filter(userid=user).update(commission=amount, commissionstatus=new_commission)

        return redirect('referralpayment')
    else:
        context = {
            'get_reward': get_reward,
        }
        return render(request, 'astone_admin/update_commission.html', context)






############## USER #######################################################################################

def registration(request):
    return render(request, 'astone_user/registration.html')

def registration_success(request):
    return render(request, 'astone_user/registration_success.html')

def customer_home(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    unique_products = {}
    for product in products:
        unique_products[product.name] = product

    context = {'categories':categories, 'products': unique_products.values()}

    return render(request, 'astone_user/customer_home.html', context)

def qrcodescanner(request):
    return render(request, 'astone_user/qrcodescanner.html')

def reward(request):
    return render(request, 'astone_user/reward.html')

def view_transactions(request):
    current_user = request.user
    transactions = Withdraw.objects.filter(username=current_user).order_by('-requestedon')
    context={'transactions':transactions}
    return render(request, 'astone_user/view_transactions.html', context)

def withdaw_done(request):
    return render(request, 'astone_user/withdaw_done.html')

def withdraw(request):
    if request.user.is_authenticated:
        current_user = request.user
        rewardamount = current_user.rewardamount
        if current_user.withdrawn == None:
            withdrawn = 0.00
        else:
            withdrawn = current_user.withdrawn
        print("rewardamount:", rewardamount)
        print("withdrawn:", withdrawn)
        rewards = Qrcodescanner.objects.filter(username=current_user).order_by('-scannedon')
        max_amount = rewardamount - withdrawn
    else:
        max_amount = 0

    context = {
        'max_amount': max_amount,
    }
        # context = {'rewards': rewards}
    return render(request, 'astone_user/withdraw.html', context)






def withdraw_request(request):
    if request.method == "POST":
        amount = request.POST.get('amount')
        uname = request.user.username
        uid = request.user.pk

        withdraw_request = Withdraw.objects.create(username=uname, userid=uid, rewardamount=amount)

        messages.success(request, 'Request Submitted')

    return render(request, 'astone_user/withdaw_done.html')






def enquiry(request):
    return render(request, 'astone_user/enquiry.html')

def viewallcategories(request):
    categories = Category.objects.all()
    context = {'categories':categories} 
    return render(request, 'astone_user/viewallcategories.html', context)


def viewsubcategories(request, pk):
    category = Category.objects.get(pk=pk)
    subcategories = Subcategory.objects.filter(category=category)
    return render(request, 'astone_user/viewsubcategories.html', {'category': category, 'subcategories': subcategories})

def viewsubproducts(request, pk):
    subcategory = Subcategory.objects.get(pk=pk)
    products = Product.objects.filter(subcategory=subcategory)

    unique_products = {}
    for product in products:
        unique_products[product.name] = product

    return render(request, 'astone_user/viewsubproducts.html', {'subcategory': subcategory, 'products': unique_products.values()})


def viewproductsingleuser(request, pk):

    products = Product.objects.get(pk=pk)
    context = {'products':products}

    return render(request, 'astone_user/viewproductsingleuser.html', context)



def viewallproductsuser(request):
    products = Product.objects.all()

    unique_products = {}
    for product in products:
        unique_products[product.name] = product

    return render(request, 'astone_user/viewallproductsuser.html', {'products': unique_products.values()})



def enquiry_form(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        state = request.POST.get('state')
        city = request.POST.get('city')
        concern = request.POST.get('concern')
        description = request.POST.get('description')


    business = Business.objects.create(name=name, mobile_number=phone, email=email, state=state, city=city, concern=concern, description=description)

    messages.success(request, 'Enquiry Submitted')

    return redirect('enquiry')

@login_required
def viewmyrewards(request):
    current_user = request.user.pk
    rewards = Qrcodescanner.objects.filter(userid=current_user).order_by('-scannedon')
    total_reward_amount = rewards.aggregate(Sum('rewardamount'))['rewardamount__sum'] or 0

    user_instance = User.objects.get(pk=current_user)

    user_instance.rewardamount = total_reward_amount

    user_instance.save()

    context = {'rewards': rewards, 'total_reward_amount':total_reward_amount}
    return render(request, 'astone_user/viewmyrewards.html', context)







from django.shortcuts import render
from .models import Qrcodescanner

def viewmyreferrals(request):
    current_user = request.user
    user_referral_code = current_user.referral_code

    # Get a list of unique users who used the referral code
    unique_users = Qrcodescanner.objects.filter(refferalcode=user_referral_code).values('username', 'userid', 'commission', 'commissionstatus').distinct()

    context = {'unique_users': unique_users}
    return render(request, 'astone_user/viewmyreferrals.html', context)

User = get_user_model()


from django.conf import settings
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
from django.urls import reverse


def customer_registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        mobile_number = request.POST['number']

        # Check if the username, email, or mobile number already exist in the database
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'astone_user/registration.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'astone_user/registration.html')
        
        if User.objects.filter(mobile_number=mobile_number).exists():
            messages.error(request, 'Mobile number already registered.')
            return render(request, 'astone_user/registration.html')

        try:
            # Initialize Twilio client
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            # Send OTP to the mobile number
            verification = client.verify.services(settings.TWILIO_VERIFY_SID).verifications.create(
                to=mobile_number,
                channel="sms"
            )
            
            # Check if OTP was sent successfully
            if verification.status == 'pending':
                # Store the mobile number and verification SID in the session
                request.session['mobile_number'] = mobile_number
                request.session['verification_sid'] = verification.sid
                
                # Pass username and email as query parameters in the redirect URL
                otp_verification_url = reverse('otp_verification') + f'?username={username}&email={email}'
                return redirect(otp_verification_url)
            else:
                messages.error(request, 'Failed to send OTP. Please try again.')
                return render(request, 'astone_user/registration.html')
        
        except TwilioRestException as e:
            messages.error(request, f'Twilio Error: {str(e)}')
            return render(request, 'astone_user/registration.html')

    return render(request, 'astone_user/registration.html')

# def otp_verification(request):
#     if request.method == 'POST':
#         otp_code = request.POST['otp_code']
#         mobile_number = request.session.get('mobile_number')
#         verification_sid = request.session.get('verification_sid')
        
#         # Retrieve username and email from query parameters
#         username = request.GET.get('username')
#         email = request.GET.get('email')
        
#         try:
#             # Initialize Twilio client
#             client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
#             # Verify the OTP code
#             verification_check = client.verify.services(settings.TWILIO_VERIFY_SID).verification_checks.create(
#                 to=mobile_number,
#                 code=otp_code,
#                 verification_sid=verification_sid
#             )
            
#             if verification_check.status == 'approved':
#                 # OTP verification successful, continue with user registration
#                 user = User.objects.create_user(
#                     username=username,
#                     email=email,
#                     mobile_number=mobile_number,
#                     is_customer=True,
#                 )
#                 messages.success(request, 'Registration Completed')
#                 return redirect('customer_home')
#             else:
#                 messages.error(request, 'Invalid OTP. Please try again.')
        
#         except TwilioRestException as e:
#             messages.error(request, f'Twilio Error: {str(e)}')
    
#     return render(request, 'astone_user/otp_verification.html')
from django.contrib.auth import login

def otp_verification(request):
    if request.method == 'POST':
        otp_code = request.POST['otp_code']
        mobile_number = request.session.get('mobile_number')
        verification_sid = request.session.get('verification_sid')

        username = request.GET.get('username')
        email = request.GET.get('email')
        
        try:
            # Initialize Twilio client
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            # Verify the OTP code
            verification_check = client.verify.services(settings.TWILIO_VERIFY_SID).verification_checks.create(
                to=mobile_number,
                code=otp_code,
                verification_sid=verification_sid
            )
            
            if verification_check.status == 'approved':
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    mobile_number=mobile_number,
                    is_customer=True,
                )
                # OTP verification successful, log in the user
                user = User.objects.filter(mobile_number=mobile_number).first()
                if user is not None and user.is_customer:
                    # Log in the user
                    login(request, user)
                    
                    # Redirect to the home page
                    return redirect('customer_home')
                else:
                    messages.error(request, 'User not found or is not a customer.')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
        
        except TwilioRestException as e:
            messages.error(request, f'Twilio Error: {str(e)}')
    
    return render(request, 'astone_user/otp_verification.html')



def customer_login(request):
    if request.method == 'POST':
        username_or_number = request.POST['username_or_number']
        
        # Check if a user with the provided phone number exists
        user = User.objects.filter(mobile_number=username_or_number).first()
        
        if user is not None and user.is_customer:
            try:
                # Initialize Twilio client
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                
                # Send OTP to the provided phone number
                verification = client.verify.services(settings.TWILIO_VERIFY_SID).verifications.create(
                    to=username_or_number,
                    channel="sms"
                )
                
                # Check if OTP was sent successfully
                if verification.status == 'pending':
                    # Store the phone number and verification SID in the session
                    request.session['mobile_number'] = username_or_number
                    request.session['verification_sid'] = verification.sid
                    
                    return redirect('otp_login_verification')
                else:
                    messages.error(request, 'Failed to send OTP. Please try again.')
            except TwilioRestException as e:
                messages.error(request, f'Twilio Error: {str(e)}')
        else:
            messages.error(request, 'Invalid phone number or user not found.')

    return render(request, 'astone_user/customer_login.html')



def otp_login_verification(request):
    if request.method == 'POST':
        otp_code = request.POST['otp_code']
        mobile_number = request.session.get('mobile_number')
        verification_sid = request.session.get('verification_sid')
        
        try:
            # Initialize Twilio client
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            # Verify the OTP code
            verification_check = client.verify.services(settings.TWILIO_VERIFY_SID).verification_checks.create(
                to=mobile_number,
                code=otp_code,
                verification_sid=verification_sid
            )
            
            if verification_check.status == 'approved':
                # OTP verification successful, log in the user
                user = User.objects.filter(mobile_number=mobile_number).first()
                if user is not None and user.is_customer:
                    login(request, user)
                    return redirect('customer_home')
                else:
                    messages.error(request, 'User not found or is not a customer.')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
        
        except TwilioRestException as e:
            messages.error(request, f'Twilio Error: {str(e)}')
    
    return render(request, 'astone_user/otp_login_verification.html')






def SignOut(request):
     logout(request)
     return redirect('customer_home')


from django.contrib import messages

def update_profile(request, pk):
    get_profile = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        new_name = request.POST['name']
        new_bank_name = request.POST['bank_name']
        new_bank_account_number = request.POST['bank_account_number']
        new_ifsc_code = request.POST['ifsc_code']
        new_upi_id = request.POST['upi_id']
        new_pan_card_name = request.POST['pan_card_name']
        new_pan_card_number = request.POST['pan_card_number']
        new_referred_by = request.POST['referred_by']

        # Check if a new image was provided
        new_profile_picture = request.FILES.get('profile_picture')
        if new_profile_picture:
            get_profile.profile_picture = new_profile_picture

        # Check if the user's own referral code was provided
        if new_referred_by == get_profile.referral_code:
            messages.error(request, "Invalid referral code. You cannot use your own referral code.")
        else:
            # Check if the provided referral code exists in the database
            if new_referred_by:
                try:
                    referred_user = User.objects.get(referral_code=new_referred_by)
                    get_profile.referred_by = new_referred_by
                except User.DoesNotExist:
                    messages.error(request, "Invalid referral code. This referral code does not exist")

            get_profile.name = new_name
            get_profile.bank_name = new_bank_name
            get_profile.bank_account_number = new_bank_account_number
            get_profile.ifsc_code = new_ifsc_code
            get_profile.upi_id = new_upi_id
            get_profile.pan_card_name = new_pan_card_name
            get_profile.pan_card_number = new_pan_card_number
            get_profile.save()
            return redirect('customer_home')


    context = {
        'get_profile': get_profile,
    }
    return render(request, 'astone_user/update_profile.html', context)


from django.shortcuts import render, get_object_or_404
from .models import Product, Qrcodescanner

def addReward(request):
    a = request.user.username
    b = request.user.pk
    c = request.user.referred_by
    coupon_code = request.POST.get("couponcode")
    
    try:
        # Check if the QR code has already been scanned
        if Qrcodescanner.objects.filter(couponcode=coupon_code).exists():
            return render(request, 'astone_user/qrcodescanner.html', {'message': 'This QR is already scanned'})
        
        qrcodescanner = get_object_or_404(Product, coupon_code=coupon_code)
        
        reward_amount = qrcodescanner.reward_amount
        product_id = qrcodescanner.pk
        product_name = qrcodescanner.name
        product_price = qrcodescanner.MRP
        
        # Create a new Qrcodescanner object
        rewards = Qrcodescanner.objects.create(
            username=a,
            userid=b,
            refferalcode=c,
            couponcode=coupon_code,
            rewardamount=reward_amount,
            productid=product_id,
            productname=product_name,
            productprice=product_price
        )
        
        # Update the 'sold' field to True in the Product table
        qrcodescanner.sold = True
        qrcodescanner.save()
        
        return render(request, 'astone_user/reward.html', {'reward_amount': reward_amount})
    
    except Exception as e:
        print(e)
        return render(request, 'astone_user/qrcodescanner.html', {'message': 'Invalid QR Code'})

from django.shortcuts import render
from .models import Product

def search_products(request):
    # Get the search query from the request's GET parameters
    query = request.GET.get('q')

    # Perform a case-insensitive search for products by name
    products = Product.objects.filter(name__icontains=query)

    unique_products = {}
    for product in products:
        unique_products[product.name] = product

    context = {
        'query': query,
        'products': unique_products.values(),
    }

    return render(request, 'astone_user/viewallproductsuser.html', context)


# from django.http import HttpResponse
# from io import BytesIO
# from PIL import Image
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas

# def customer_render_pdf_view(request):
#     if request.method == 'POST':
#         selected_item_ids = request.POST.getlist('selected_items') 
#         pdf_cart_items = PdfCartItem.objects.filter(pk__in=selected_item_ids)

#         # Create a Django response object with content_type as pdf
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = 'filename="product.pdf"'

#         # Create a PDF document using BytesIO
#         pdf_buffer = BytesIO()

#         # Initialize variables for arranging items
#         items_per_row = 2
#         rows_per_page = 8
#         items_on_current_row = 0
#         rows_on_current_page = 0
#         x_offset = 0
#         y_offset = 0
#         x_spacing = 300  # Adjust as needed
#         y_spacing = 200  # Adjust as needed

#         # Create a ReportLab PDF canvas
#         c = canvas.Canvas(pdf_buffer, pagesize=letter)


#         # Generate PDF content dynamically
#         for item in pdf_cart_items:
#             if items_on_current_row >= items_per_row:
#                 items_on_current_row = 0
#                 x_offset = 0
#                 y_offset += y_spacing

#             if rows_on_current_page >= rows_per_page:
#                 c.showPage()
#                 rows_on_current_page = 0
#                 y_offset = 0

#             # Load the card image
#             card_image_path = 'static/img/1.png'
#             card_image = Image.open(card_image_path)

#             # Position the card image on the page
#             c.drawImage(card_image_path, x=x_offset, y=y_offset, width=250, height=150)

#             # Load the QR code image from the PdfCartItem model
#             qr_code_image_path = item.product.qr_code.path

#             # Position the QR code image on top of the card image
#             c.drawImage(qr_code_image_path, x=x_offset + 180, y=y_offset + 50, width=50, height=50)

#             c.setFont("Helvetica-Bold", 6.5)
#             c.setFillColorRGB(255, 255, 255)

#             # Display the "Reward Inside" text below the QR code
#             reward_text = f"Reward: Rs.{item.product.reward_amount}/-"
#             c.drawString(x_offset + 177, y_offset + 39, reward_text)

#             reward_code = f"Coupon Code: {item.product.coupon_code}"
#             c.drawString(x_offset + 169, y_offset + 27, reward_code)

#             # Update offsets and counters
#             x_offset += x_spacing
#             items_on_current_row += 1
#             rows_on_current_page += 1

#         for item in pdf_cart_items:
#             product = item.product
#             product.pdf = True
#             product.save()
#         # Save the PDF content to the response
#         c.save()
#         pdf_buffer.seek(0)
#         response.write(pdf_buffer.read())
#         pdf_buffer.close()

#         return response

#     else:
#         # Handle GET request or other cases here
#         pass




from django.http import HttpResponse
from io import BytesIO
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Cardimage
from .models import PdfCartItem

def customer_render_pdf_view(request):
    if request.method == 'POST':
        selected_item_ids = request.POST.getlist('selected_items')
        pdf_cart_items = PdfCartItem.objects.filter(pk__in=selected_item_ids)

        # Create a Django response object with content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="product.pdf"'

        # Create a PDF document using BytesIO
        pdf_buffer = BytesIO()

        # Initialize variables for arranging items
        items_per_row = 2
        rows_per_page = 8
        items_on_current_row = 0
        rows_on_current_page = 0
        x_offset = 0
        y_offset = 0
        x_spacing = 300  # Adjust as needed
        y_spacing = 200  # Adjust as needed

        # Create a ReportLab PDF canvas
        c = canvas.Canvas(pdf_buffer, pagesize=letter)

        # Generate PDF content dynamically
        for item in pdf_cart_items:
            if items_on_current_row >= items_per_row:
                items_on_current_row = 0
                x_offset = 0
                y_offset += y_spacing

            if rows_on_current_page >= rows_per_page:
                c.showPage()
                rows_on_current_page = 0
                y_offset = 0

            # Load the card image from the Cardimage model
            card_image = Cardimage.objects.get(name='Card')  # Replace 'your_image_name' with the actual name or identifier
            card_image_path = card_image.image.path

            # Position the card image on the page
            c.drawImage(card_image_path, x=x_offset, y=y_offset, width=250, height=150)

            # Load the QR code image from the PdfCartItem model
            qr_code_image_path = item.product.qr_code.path

            # Position the QR code image on top of the card image
            c.drawImage(qr_code_image_path, x=x_offset + 180, y=y_offset + 50, width=50, height=50)

            c.setFont("Helvetica-Bold", 6.5)
            c.setFillColorRGB(255, 255, 255)

            # Display the "Reward Inside" text below the QR code
            reward_text = f"Reward: Rs.{item.product.reward_amount}/-"
            c.drawString(x_offset + 177, y_offset + 39, reward_text)

            reward_code = f"Coupon Code: {item.product.coupon_code}"
            c.drawString(x_offset + 169, y_offset + 27, reward_code)

            # Update offsets and counters
            x_offset += x_spacing
            items_on_current_row += 1
            rows_on_current_page += 1

            # Set product.pdf to True and save the product
            product = item.product
            product.pdf = True
            product.save()

        # Rest of your code...

        # Save the PDF content to the response
        c.save()
        pdf_buffer.seek(0)
        response.write(pdf_buffer.read())
        pdf_buffer.close()

        return response

    else:
        # Handle GET request or other cases here
        pass
