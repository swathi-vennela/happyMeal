from django.db import models
from django.conf import settings
from PIL import Image
from django.urls import reverse
from datetime import datetime

STATUS_CHOICES = (
    ('O', 'Order Request Accepted'),
    ('C', 'Cooking'),
    ('D', 'Deliverd')
)

class Item(models.Model):
    chef = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    is_veg = models.BooleanField(default=True)
    available = models.BooleanField(default=True)
    # status = models.CharField(choices=STATUS_CHOICES, max_length=1)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    calories = models.FloatField(default=0)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='item_pics')


    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Item.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })
    def get_review_item_url(self):
        return reverse("core:add_review", kwargs={
                'slug' : self.slug
            })

    def get_chef(self):
        return self.chef

    def set_unavailable(self):
        self.available = False
        super().save()      


    def set_available(self):
        self.available = True
        super().save()


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    timestampStr = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
    status = models.CharField(choices=STATUS_CHOICES, max_length =1, default = 'O')
    chef_key = models.CharField(max_length=100 , default = timestampStr)
    
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
    	if self.item.discount_price:
    		return self.get_total_discount_item_price()
    	return self.get_total_item_price()
    def set_change_order_status(self):
        self.ordered = True
        super().save()
    def set_status_delivered(self):
        self.status = 'D'
        super().save()

    def set_status_cooking(self):
        self.status = 'C'
        super().save()



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now = True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.filter(ordered=False).all():
            total += order_item.get_final_price()
        # if self.coupon:
        #     total -= self.coupon.amount
        return total
    def set_change_order_status(self):
        self.ordered = True
        super().save()


class Review(models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    rating = models.FloatField(default=0)
    date = models.DateTimeField(auto_now = True) #date when the review is added for the first time
    review_id = models.IntegerField(default= 0)

    def __str__(self):
        return self.user.username 


class OrderedList(models.Model):
    chef = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField(OrderItem)

    def __str__(self):
        return self.chef.username
