from django.db import models
from django.utils import timezone


class User(models.Model):
    u_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30,null=True)
    last_name = models.CharField(max_length=30,null=True)
    dob = models.DateField(null=True)
    email = models.EmailField()
    password = models.CharField(max_length=10)
    is_seller = models.BooleanField()

    loc = models.ForeignKey('Location', on_delete=models.CASCADE)
    wall = models.ForeignKey('Wallet', on_delete=models.CASCADE)
    created_date = models.DateTimeField(
        default=timezone.now)

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.u_id)


class Location(models.Model):
    lid = models.AutoField(primary_key=True)
    zip_code = models.IntegerField(null=True)
    city_name = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.address)


class Inventory(models.Model):
    inv_id = models.AutoField(primary_key=True)
    category = models.CharField(null=True,max_length=100)
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.inv_id)


class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_desc = models.ForeignKey('ItemDesc', on_delete=models.CASCADE)
    item_status = models.IntegerField() # Sold = 1
    item_seller = models.ForeignKey('User', on_delete=models.CASCADE)
    item_inventory = models.ForeignKey('Inventory', on_delete=models.CASCADE)
    item_location = models.ForeignKey('Location', on_delete=models.CASCADE)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.item_id)


class ItemDesc(models.Model):
    item_desc_id = models.AutoField(primary_key=True)
    age = models.IntegerField()
    name = models.CharField(max_length=30)
    comments = models.TextField()

    # pic = models.ImageField(upload_to='ENTER VALID LINK HERE')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.item_desc_id)


class Order(models.Model):
    o_id = models.AutoField(primary_key=True)
    items = models.ManyToManyField(Item)
    b_id = models.ForeignKey('User', on_delete=models.CASCADE)


class FeedBack(models.Model):
    f_id = models.AutoField(primary_key=True)
    b_id = models.ForeignKey('User',null=True, on_delete=models.CASCADE)
    comments = models.TextField(null=True)
    o_id = models.ForeignKey('Order', null = True,on_delete=models.CASCADE)


class Wallet(models.Model):
    w_id = models.AutoField(primary_key=True)
    credits = models.IntegerField()
