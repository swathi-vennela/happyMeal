import requests 
from django.contrib import messages
from django.db.models import Q, Avg
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import *
from django.contrib.auth.models import User 
from users.models import User as AbsUser
from django.views.generic import ListView, View, DetailView, CreateView
from django.utils import timezone
from .forms import *
from users.decorators import *
import logging

deleted_reviews = 0

@login_required
def menu(request):
	if request.method == 'POST':

		filterAtt = request.POST['filter1']
		if filterAtt:
			if filterAtt == "veg":
				filter_qs = Item.objects.filter(is_veg=True, available=True)
				return render(request, 'core/menu.html',context={'items' : filter_qs})
			elif filterAtt == "nonveg":
				filter_qs = Item.objects.filter(is_veg=False, available=True)
				return render(request, 'core/menu.html',context={'items' : filter_qs})


		filterAtt = request.POST['filter2']
		if filterAtt:
			if filterAtt == "lte100":
				filter_qs = Item.objects.filter(price__range=(0,100), available=True)
				return render(request, 'core/menu.html',context={'items' : filter_qs})
			elif filterAtt == "100to200":
				filter_qs = Item.objects.filter(price__range=(101,199), available=True)
				return render(request, 'core/menu.html',context={'items' : filter_qs})
			elif filterAtt == "gte200":
				filter_qs = Item.objects.filter(price__range=(200,1000), available=True)
				return render(request, 'core/menu.html',context={'items' : filter_qs})

		sortAtt = request.POST['sort']
		if sortAtt:
			if sortAtt == "priceAsc":
				sorted_qs = Item.objects.filter(available=True).order_by('price')
				return render(request, 'core/menu.html',context={'items' : sorted_qs})
			elif sortAtt == "priceDesc":
				sorted_qs = Item.objects.filter(available=True).order_by('-price')
				return render(request, 'core/menu.html',context={'items' : sorted_qs})

	return render(request, 'core/menu.html', context={'items' : Item.objects.filter(available=True).all()})

def chefItemList(request):
	if request.method == 'POST':

		filterAtt = request.POST['filter1']
		if filterAtt:
			if filterAtt == "veg":
				filter_qs = Item.objects.filter(is_veg=True, chef = request.user)
				return render(request, 'core/chef_item_list.html',context={'items' : filter_qs})
			elif filterAtt == "nonveg":
				filter_qs = Item.objects.filter(is_veg=False, chef = request.user)
				return render(request, 'core/chef_item_list.html',context={'items' : filter_qs})


		filterAtt = request.POST['filter2']
		if filterAtt:
			if filterAtt == "lte100":
				filter_qs = Item.objects.filter(price__range=(0,100), chef = request.user)
				return render(request, 'core/chef_item_list.html',context={'items' : filter_qs})
			elif filterAtt == "100to200":
				filter_qs = Item.objects.filter(price__range=(101,199), chef = request.user)
				return render(request, 'core/chef_item_list.html',context={'items' : filter_qs})
			elif filterAtt == "gte200":
				filter_qs = Item.objects.filter(price__range=(200,1000), chef = request.user)
				return render(request, 'core/chef_item_list.html',context={'items' : filter_qs})

		sortAtt = request.POST['sort']
		if sortAtt:
			if sortAtt == "priceAsc":
				sorted_qs = Item.objects.filter(chef = request.user).order_by('price')
				return render(request, 'core/chef_item_list.html',context={'items' : sorted_qs})
			elif sortAtt == "priceDesc":
				sorted_qs = Item.objects.order_by('-price')
				return render(request, 'core/chef_item_list.html',context={'items' : sorted_qs})

	return render(request, 'core/chef_item_list.html', context={'items' : Item.objects.filter(chef = request.user).all()})



def search(request):
	template = 'core/menu.html'
	query_set = []
	query = request.GET.get('q')
	queries = query.split(" ")
	for q in queries:
		items=Item.objects.filter(
				Q(title__icontains=q) |
				Q(description__icontains=q)
			).distinct()

		for item in items:
			query_set.append(item)

	return render(request, 'core/menu.html', context={'items': list(set(query_set))})

def chef_list(request):
	chefs = AbsUser.objects.filter(is_store_owner=True)
	return render(request, 'core/chefs.html',context={'chefs':chefs})


@store_required
def create_item(request):
	if request.method == "POST":
		form = ItemForm(request.POST, request.FILES)

		if form.is_valid():
			data = form.save(commit=False)
			data.chef = request.user 
			data.slug = datetime.now().strftime("%c")
			data.save()
			return redirect("core:menu")
	else:
		form = ItemForm()
	return render(request, 'core/item_form.html',{"form":form})


class ItemListView(ListView):
	model = Item
	template_name = 'core/menu.html'
	ordering = ['-price']


class OrderSummaryView(LoginRequiredMixin, View):
	def get(self, *args, **kwargs):
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			order1 = Order.objects.get(user=self.request.user, ordered=False).items.filter(user=self.request.user,ordered=False).all()
			order2 = Order.objects.get(user=self.request.user, ordered=False).items.filter(user=self.request.user,ordered=True).all()
			context = {
				'object' : order,
				'object1' : order1,
				'object2' : order2
			}
			return render(self.request, 'core/order_summary.html', context)
		except ObjectDoesNotExist:
			messages.info(self.request, "You do not have an active order")
			return redirect("core:menu")

class OrderHistoryView(LoginRequiredMixin, View):
	def get(self, *args, **kwargs):
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			order1 = Order.objects.get(user=self.request.user, ordered=False).items.filter(user=self.request.user,ordered=False).all()
			order2 = Order.objects.get(user=self.request.user, ordered=False).items.filter(user=self.request.user,ordered=True).all()
			context = {
				'object' : order,
				'object1' : order1,
				'object2' : order2
			}
			return render(self.request, 'core/order_history.html', context)
		except ObjectDoesNotExist:
			messages.info(self.request, "You do not have an order History")
			return redirect("core:menu")

class OrderedFoodListView(LoginRequiredMixin, View):
	def get(self, *args, **kwargs):
		try:
			order = OrderedList.objects.get(chef=self.request.user).items.all()
			# order1 = Order.objects.get(user=self.request.user, ordered=False).items.filter(user=self.request.user,ordered=False).all()
			# order2 = Order.objects.get(user=self.request.user, ordered=False).items.filter(user=self.request.user,ordered=True).all()
			context = {
				'object' : order,
				
			}
			return render(self.request, 'core/ordered_food_LIST.html', context)
		except ObjectDoesNotExist:
			messages.info(self.request, "You do not have an active order")
			return redirect("core:menu")


# class ItemDetailView(DetailView):
# 	model = Item
# 	template_name = 'core/product.html'

def detail(request, slug):
	item = Item.objects.get(slug=slug)
	reviews = Review.objects.filter(item = item).order_by("-date")
	average = reviews.aggregate(Avg("rating"))["rating__avg"]
	if average == None:
		average = 0
	average = round(average,2)
	item.averageRating = average
	context = {
		"item" : item,
		"reviews" : reviews,
		"average" : average,
	}
	return render(request, 'core/product.html', context)


@login_required
def add_to_cart(request, slug):
	item = get_object_or_404(Item, slug=slug)
	order_item, created = OrderItem.objects.get_or_create(item=item, user= request.user, ordered=False)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		#check if the order item is in the order
		if order.items.filter(item__slug=item.slug, ordered = False).exists():
			order_item.quantity += 1
			order_item.save()
			messages.info(request, "This item quantity was updated.")
		else:
			messages.info(request, "This item was added to your cart.")
			order.items.add(order_item)
	else:
		ordered_date = timezone.now()
		order = Order.objects.create(user=request.user, ordered_date = ordered_date)
		order.items.add(order_item)
		messages.info(request, "This item was added to your cart.")
	return redirect("core:order-summary")

@login_required
def set_item_unavailable(request, slug):
	item = get_object_or_404(Item, slug=slug)
	item.set_unavailable()
	return redirect("core:chef-item-list")

@login_required
def set_item_available(request, slug):
	item = get_object_or_404(Item, slug=slug)
	item.set_available()
	return redirect("core:chef-item-list")



@login_required
def remove_from_cart(request, slug):
	item = get_object_or_404(Item, slug=slug)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		#check if the order item is in the order
		if order.items.filter(item__slug=item.slug).exists():
			order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
			#order.items.remove(order_item)
			order_item.delete()
			messages.info(request, "This item was removed from your cart.")
			return redirect("core:order-summary")

		else:
			#the given item is not there in the customer's order
			messages.info(request, "This item is not present in your cart.") 
			return redirect("core:product", slug=slug)
	else:
		#show a message saying that the user doesn't have an order
		messages.info(request, "You do not have an active cart")
		return redirect("core:product", slug=slug)
	return redirect("core:product", slug=slug)

@login_required
def remove_single_item_from_cart(request, slug):
	item = get_object_or_404(Item, slug=slug)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		#check if the order item is in the order
		if order.items.filter(item__slug=item.slug).exists():
			order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
			#order.items.remove(order_item)
			if order_item.quantity > 1:
				order_item.quantity -= 1
				order_item.save()
				messages.info(request, "This item quantity was updated.")
			else:
				order_item.delete()
				messages.info(request, "This item has been removed from your cart.")
			return redirect("core:order-summary")

		else:
			#the given item is not there in the customer's order
			messages.info(request, "This item is not present in your cart.") 
			return redirect("core:product", slug=slug)
	else:
		#show a message saying that the user doesn't have an order
		messages.info(request, "You do not have an active cart")
		return redirect("core:product", slug=slug)
	return redirect("core:product", slug=slug)

@login_required
def item_delivered(request, slug, chef_key):
	item = get_object_or_404(Item, slug=slug)
	order_qs = OrderItem.objects.filter(item=item, chef_key= chef_key, ordered=True)
	if order_qs.exists():
		order = order_qs[0]
		#check if the order item is in the order
		order.set_status_delivered()
		

		
	return redirect("core:product", slug=slug)

@login_required
def item_cooking(request, slug, chef_key):
	item = get_object_or_404(Item, slug=slug)
	order_qs = OrderItem.objects.filter(item=item, chef_key= chef_key, ordered=True)
	if order_qs.exists():
		order = order_qs[0]
		#check if the order item is in the order
		order.set_status_cooking()
		

		
	return redirect("core:product", slug=slug)



def filterItems(request):

	if request.method == 'POST':
		filterAtt = request.POST['filters']
		filter_qs = Item.objects.filter(category = filterAtt)
		# print(filterAtt)
		return render(request, 'core/menu.html', context = {'items' : filter_qs})

	return render(request, 'core/menu.html', context={'items' : Item.objects.all()})

def add_review(request, slug):
    if request.user.is_authenticated:
        item = Item.objects.get(slug = slug)
        review_qs = Review.objects.filter(item= item, user= request.user)
        if review_qs:
        	error = "Can't add more than one review for the same item.. Edit your review..!!"
        	return redirect("core:product", slug)
        elif (request.method == "POST") and (not review_qs) and(request.user != item.chef):
        	form = ReviewForm(request.POST or None)
        	if form.is_valid():
        		data = form.save(commit = False)
        		data.comment = request.POST["comment"]
        		data.rating = request.POST["rating"]
        		data.user = request.user 
        		data.item = item
        		global delete_reviews  
        		data.review_id = Review.objects.count()+ deleted_reviews +1
        		data.save()
        		return redirect("core:product",slug)
        else:
        	form = ReviewForm()
        return render(request, 'core/product.html',{"error":error,"form":form})
    else:
    	return redirect("users:login")

# edit the review
def edit_review(request, slug, review_id):
    if request.user.is_authenticated:
        item = Item.objects.get(slug=slug)
        # review
        review = Review.objects.get(item=item, review_id=review_id)

        # check if the review was done by the logged in user
        if request.user == review.user:
            # grant permission
            if request.method == "POST":
                form = ReviewForm(request.POST, instance=review)
                if form.is_valid():
                    data = form.save(commit=False)
                    if (data.rating > 10) or (data.rating < 0):
                    	 error = "Out of range. Please select a rating from 0 to 10"
                    	 return render(request, 'core/edit_review.html', {"error":error ,"form": form})
                    else:
                        data.save()
                        return redirect("core:product", slug)
            else:
                form = ReviewForm(instance=review)
            return render(request, 'core/edit_review.html', {"form": form})
        else:
            return redirect("core:product", slug)
    else:
        return redirect("users:login")

# delete the review
def delete_review(request, slug, review_id):
    if request.user.is_authenticated:
        item = Item.objects.get(slug=slug)
        # review
        review = Review.objects.get(item=item, review_id=review_id)

        # check if the review was done by the logged in user
        if request.user == review.user:
            # grant permission to delete
            review.delete()
            global deleted_reviews 
            deleted_reviews = deleted_reviews+1


        return redirect("core:product", slug)
    else:
        return redirect("users:login")



def edit_item(request, slug):    
	item = Item.objects.get(slug=slug)
	if request.method == "POST":
		form = ItemForm(request.POST, instance=item)
		if form.is_valid():
				data = form.save(commit=False)
				data.save()
				return redirect("core:product", slug)
	else:
		form = ItemForm(instance=item)
		return render(request, 'core/edit_review.html', {"form": form})
