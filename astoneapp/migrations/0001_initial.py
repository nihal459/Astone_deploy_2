# Generated by Django 4.2.2 on 2023-11-13 07:51

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('concern', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category_images')),
            ],
        ),
        migrations.CreateModel(
            name='Productimage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_images')),
            ],
        ),
        migrations.CreateModel(
            name='Qrcodescanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('userid', models.CharField(blank=True, max_length=50, null=True)),
                ('couponcode', models.CharField(blank=True, max_length=50, null=True)),
                ('rewardamount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('refferalcode', models.CharField(blank=True, max_length=50, null=True)),
                ('scannedon', models.DateTimeField(auto_now_add=True)),
                ('productid', models.CharField(blank=True, max_length=50, null=True)),
                ('productname', models.CharField(blank=True, max_length=255, null=True)),
                ('productprice', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('commission', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('paymentstatus', models.CharField(blank=True, choices=[('paid', 'Paid'), ('pending', 'Pending'), ('processing', 'Processing'), ('cancelled', 'Cancelled')], default='processing', max_length=20, null=True)),
                ('commissionstatus', models.CharField(blank=True, choices=[('paid', 'Paid'), ('pending', 'Pending'), ('processing', 'Processing'), ('cancelled', 'Cancelled')], default='processing', max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Withdraw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('userid', models.CharField(blank=True, max_length=50, null=True)),
                ('rewardamount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('referralamount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('requestedon', models.DateTimeField(auto_now_add=True)),
                ('paidon', models.DateTimeField(auto_now_add=True)),
                ('paymentstatus', models.CharField(choices=[('paid', 'Paid'), ('pending', 'Pending'), ('processing', 'Processing'), ('cancelled', 'Cancelled')], default='processing', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='astoneapp.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('productcode', models.CharField(blank=True, max_length=20, null=True)),
                ('advantages', models.TextField(blank=True, null=True)),
                ('suitable_surface', models.TextField(blank=True, null=True)),
                ('application', models.TextField(blank=True, null=True)),
                ('additional_information', models.TextField(blank=True, null=True)),
                ('youtube_link', models.URLField(blank=True, null=True)),
                ('reward_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('MRP', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('coupon_code', models.CharField(blank=True, max_length=10, unique=True)),
                ('qr_code', models.ImageField(blank=True, upload_to='qr_codes')),
                ('sold', models.BooleanField(default=False, null=True)),
                ('pdf', models.BooleanField(default=False, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='astoneapp.category')),
                ('images', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='astoneapp.productimage')),
                ('subcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='astoneapp.subcategory')),
            ],
        ),
        migrations.CreateModel(
            name='PdfCartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='astoneapp.product')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_admin', models.BooleanField(default=False, verbose_name='is admin')),
                ('is_staff', models.BooleanField(default=False, verbose_name='is staff')),
                ('is_customer', models.BooleanField(default=False, verbose_name='is customer')),
                ('name', models.CharField(default='User', max_length=100)),
                ('mobile_number', models.CharField(default='Nil', max_length=20)),
                ('bank_name', models.CharField(default='Nil', max_length=100)),
                ('bank_account_number', models.CharField(default='Nil', max_length=50)),
                ('ifsc_code', models.CharField(default='Nil', max_length=20)),
                ('upi_id', models.CharField(default='Nil', max_length=100)),
                ('pan_card_name', models.CharField(default='Nil', max_length=100)),
                ('pan_card_number', models.CharField(default='Nil', max_length=20)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures')),
                ('referral_code', models.CharField(default='DEFAULTCODE', max_length=6, unique=True)),
                ('referred_by', models.CharField(blank=True, max_length=100, null=True)),
                ('supercustomer', models.BooleanField(default=False, null=True)),
                ('rewardamount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('withdrawn', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
