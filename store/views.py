from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm, RegisterForm, ProdRegistration, PriceForm
from .models import *
from django.db import connection
from collections import Counter
locs = Location.objects.all()
def login(request):
	request.session.flush()
	if request.method == 'POST':
		request.session.flush()
		form = LoginForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			user_obj = User.objects.filter(email=form.cleaned_data['email'], password=form.cleaned_data['password'])

			if user_obj.exists():
				id = user_obj.get().u_id
				order_obj = Order.objects.filter(b_id=id)
				request.session.flush()
				cart = []
				clicked = {}
				request.session['cart'] = cart
				request.session['visited'] = clicked
				request.session['email'] = email
				request.session['first_name'] = user_obj.get().first_name
				request.session['id'] = user_obj.get().u_id
				request.session['credits'] = user_obj.get().wall.credits
				request.session['items'] = len(cart)
				request.session['is_seller'] = user_obj.get().is_seller
				prods=Item.objects.all()
				fprods = []
				inv_id = 1
				inv = request.session.get('visited')
				if (inv) :
					inv_id = max(inv,key=inv.get)
				if request.session.get('cart') is not None:
					items = len(request.session.get('cart'))
				fprods=Item.objects.filter(item_inventory=inv_id)
				if request.session['is_seller'] == 1:
					seller_obj = User.objects.get(u_id=id)
					prods = Item.objects.filter(item_seller=seller_obj)
					return render(request, 'store/sales.html',
								  {'first_name': request.session['first_name'], 'credits': request.session['credits'], 'is_seller': 1,
								   'prods': prods,'id':request.session['id'],'fprods':fprods,'locs':locs})

				else:
					if order_obj.exists():
						return render(request, 'store/index.html', {'first_name': request.session['first_name'],
																	'credits': request.session['credits'],
																	'items': len(cart),
																	'id': request.session['id'],
																	'is_seller': request.session['is_seller'],
																	'prods': prods,'fprods':fprods,'locs':locs})
					else:
						request.session['items'] = 0
						return render(request, 'store/index.html', {'first_name': request.session['first_name'],
																	'credits': request.session['credits'],
																	'items': len(cart),
																	'id': request.session['id'],
																	'is_seller': request.session['is_seller'],
																	'prods': prods,'fprods':fprods,'locs':locs})
			error = "Account does not exists. Please register"
			return render(request, 'store/login.html', {'form': form, 'error': error})
	else:
		form = LoginForm()
	return render(request, 'store/login.html', {'form': form})


def index(request):
	fname = request.session.get('first_name')
	credits = request.session.get('credits')
	items = 0
	prods=[]
	fprods = []
	inv_id = 1
	inv = request.session.get('visited')
	if inv != {} :
		print(inv)
		inv_id = int(max(inv,key=inv.get))
		print(inv)
	if request.session.get('cart') is not None:
		items = len(request.session.get('cart'))
	id = request.session.get('id')
	is_seller = request.session.get('is_seller')
	prods=Item.objects.all()
	fprods=Item.objects.filter(item_inventory=inv_id)
	if fname != None and credits != None:
		return render(request, 'store/index.html',
					  {'first_name': fname, 'credits': credits, 'items': items, 'is_seller': is_seller, 'id': id,
					   'prods': prods,'fprods':fprods,'locs':locs})
	else:
		return render(request, 'store/index.html',{'prods': prods,'fprods':fprods})


def catResults(request):
	fname = request.session.get('first_name')
	credits = request.session.get('credits')
	items = len(request.session.get('cart'))
	id = request.session.get('id')
	if request.method == 'GET':
		inv_id = request.GET.get('inv_id')
		inv= Inventory.objects.get(inv_id=inv_id)
		if inv_id:
			prods=Item.objects.filter(item_inventory=inv_id)
			return render(request, 'store/cat_results.html', {'first_name': fname, 'credits': credits, 'items': items, 'prods':prods, 'inv':inv,'id':id,'locs':locs})
	else:
		return HttpResponse("Fname couldnt be passes succesfully")

def locResults(request):
	fname = request.session.get('first_name')
	credits = request.session.get('credits')
	items = len(request.session.get('cart'))
	id = request.session.get('id')
	if request.method == 'GET':
		loc_id = request.GET.get('loc_id')
		if loc_id:
			prods=Item.objects.filter(item_location_id=loc_id)
			return render(request, 'store/cat_results.html', {'first_name': fname, 'credits': credits, 'items': items, 'prods':prods,'id':id,'locs':locs})
	else:
		return HttpResponse("Fname couldnt be passes succesfully")

def priceResults(request):
	fname = request.session.get('first_name')
	credits = request.session.get('credits')
	items = len(request.session.get('cart'))
	id = request.session.get('id')
	if request.method == 'POST':
		prods=[]
		form = PriceForm(request.POST)
		if form.is_valid():
			minp=form .cleaned_data['minPrice']
			maxp=form.cleaned_data['maxPrice']
			prods_desc=ItemDesc.objects.filter(price__gte=minp,price__lte=maxp)
			for pd in prods_desc:
				prods.append(Item.objects.get(item_desc=pd))
			return render(request, 'store/cat_results.html', {'first_name': fname, 'credits': credits, 'items': items, 'prods':prods,'id':id,'locs':locs})
	else:
		return HttpResponse("Fname couldnt be passes succesfully")

def productDetails(request):
	fname = request.session.get('first_name')
	credits = request.session.get('credits')
	items = len(request.session.get('cart'))
	id = request.session.get('id')
	if request.method == 'GET':
		a = request.session.get('visited')
		item_id = request.GET.get('item')
		if not item_id:
			if fname != None and credits != None:
				return render(request, 'store/product_details.html',
							  {'first_name': fname, 'credits': credits, 'items': items,'id':id})
			else:
				return HttpResponse("Fname couldnt be passes succesfully")
		else:
			item_obj = Item.objects.get(item_id=item_id)
			inv_id = str(item_obj.item_inventory.inv_id)
			if request.session['visited'] == {}:
				request.session['visited'][inv_id] = 1
				print(request.session['visited'],"1")
			else:
				if inv_id not in list(request.session['visited'].keys()):
					request.session['visited'][inv_id] = 1
					print(request.session['visited'],"2")
				else:
					request.session['visited'][inv_id] += 1
					print(request.session['visited'],"3")
			request.session.modified = True
			return render(request, 'store/product_details.html',
							  {'first_name': fname, 'credits': credits, 'items': items, 'prod':item_obj,'id':id})

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			user_obj = User.objects.filter(email=form.cleaned_data['email'])
			if user_obj.exists():
				error = "Account with given Email ID already exists"
				return render(request, 'store/register.html', {'form':form,'error': error})
			first_name = form.cleaned_data['first_name']
			loci = Location.objects.create()
			loci.city_name = form.cleaned_data['city']
			loci.zip_code = form.cleaned_data['zip_code']
			loci.address = form.cleaned_data['address']
			loci.save()

			wallet = Wallet.objects.create(credits=10000)
			wallet.save()

			obj = User.objects.create(is_seller=False, loc=loci, wall=wallet)
			obj.email = email
			obj.first_name = form.cleaned_data['first_name']
			obj.last_name = form.cleaned_data['last_name']
			obj.password = form.cleaned_data['password']
			obj.dob = form.cleaned_data['dob']
			if form.cleaned_data['seller'] == "1":
				obj.is_seller = True
			else:
				obj.is_seller = False
			obj.save()


			request.session.flush()
			request.session['email'] = email
			request.session['first_name'] = first_name
			request.session['id'] = obj.u_id
			request.session['is_seller'] = obj.is_seller
			return render(request, 'store/index.html',
						  {'first_name': first_name, 'credits': credits, 'items': 0, 'is_seller': obj.is_seller,
						   'id': obj.u_id})

	else:
		form = RegisterForm()
	return render(request, 'store/register.html', {'form': form})


def search(request):
	item=[]
	id = request.session.get('id')
	fname = request.session.get('first_name')
	credits = request.session.get('credits')
	if request.method == 'GET':  # If the form is submitted
		search_query = request.GET.get('search', None)
		desc = ItemDesc.objects.filter(name=search_query)
		for d in desc:
			item.append(Item.objects.get(item_desc_id=d.item_desc_id))
	items = 0
	if request.session.get('cart') is not None:
		items = len(request.session.get('cart'))

	if credits != None:
		return render(request, 'store/search_results.html',{'id':id,'first_name': fname, 'credits': credits, 'items': items, 'search': search_query, 'desc': desc, 'item':item})
	else:
		return HttpResponse("Fname couldnt be passes succesfully")


def sales(request):
	fname = request.session.get('first_name')
	credits = request.session.get('credits')
	items = len(request.session.get('cart'))
	id = request.session.get('id')
	is_seller = request.session.get('is_seller')
	seller_obj = User.objects.get(u_id=id)
	prods = Item.objects.filter(item_seller=seller_obj)

	if fname != None and credits != None:
		return render(request, 'store/sales.html',
					  {'first_name': fname, 'credits': credits, 'items': items, 'is_seller': is_seller, 'id': id,
					   'prods': prods})
	else:
		return HttpResponse("Fname couldnt be passes succesfully")


def orders(request):
	fname = request.session.get('first_name')
	credits = request.session.get('credits')
	items = len(request.session.get('cart'))
	id = request.session.get('id')
	is_seller = request.session.get('is_seller')
	buy_obj = User.objects.get(u_id=id)
	orders = Order.objects.filter(b_id=buy_obj)
	if fname != None and credits != None:
		return render(request, 'store/orders.html',
					  {'first_name': fname, 'credits': credits, 'items': items, 'is_seller': is_seller, 'id': id,
					   'orders': orders})
	else:
		return HttpResponse("Fname couldnt be passed succesfully")


def display(request):
	fname = request.session.get('first_name')
	cursor = connection.cursor()
	cursor.execute('SELECT * FROM store_item')
	item = cursor.fetchone()
	id = item[2]
	cursor.execute('SELECT * FROM store_itemdesc where item_desc_id = %s', [id])
	itemdesc = cursor.fetchone()

	return render(request, 'store/display.html',
				  {'item': item, 'itemdesc': itemdesc, 'first_name': fname, 'items': item})


def cart(request):
	fname = request.session.get('first_name')
	items = len(request.session.get('cart'))
	cart = request.session.get('cart')
	id1 = request.session.get('id')
	credits = request.session.get('credits')
	prods = []
	inv_ids = []
	total=0
	for id in cart:
		it = Item.objects.get(item_id=id)
		prods.append(it)
		total+=it.item_desc.price
	if request.method == 'GET':
		item_id = request.GET.get('item')
		checkout = request.GET.get('checkout')
		cancel = request.GET.get('cancel')
		if checkout:
			if int(checkout) == 1 and credits >= total:
				ord = Order.objects.create(b_id_id=request.session['id'])
				for it in prods:
					ord.items.add(it)
					it.item_status = 1
					seller_id = it.item_seller.u_id
					seller = User.objects.get(u_id=seller_id)
					seller.wall.credits += total
					seller.save() 
					it.save()
				ord.save()

				request.session['cart'] = []
				cart = []
				user = User.objects.get(u_id=id1)
				user.wall.credits -= total
				credits = user.wall.credits
				user.save()
				user.wall.save()
				return index(request)
			else:
				mssg = "Insufficient Credits! Order not placed."
				return render(request, 'store/cart.html',
							  {'first_name': fname, 'credits': credits, 'items': items,'prods': prods,'total':total,'id':id1,'mssg':mssg})
				#return HttpResponse("Insufficient Credits! Order not placed.")

		if cancel:
			if int(cancel) == 1:
				cart.remove(item_id)
				request.session['cart'] = cart
				items=len(cart)	
				it = Item.objects.get(item_id=item_id)
				prods.remove(it)
				total -= it.item_desc.price
				return render(request, 'store/cart.html',
							  {'first_name': fname, 'credits': credits, 'items': items, 'prods': prods, 'total': total,'id':id1})


		if not item_id:
			if fname != None and credits != None:
				return render(request, 'store/cart.html',
							  {'first_name': fname, 'credits': credits, 'items': items,'prods': prods,'total':total,'id':id1})
			else:
				return HttpResponse("Fname couldnt be pass succesfully")

		else:
			item_obj = Item.objects.get(item_id=item_id)
			inv_id = str(item_obj.item_inventory.inv_id)
			if request.session['visited'] == {}:
				request.session['visited'][inv_id] = 1
				print(request.session['visited'],"1")
			else:
				if inv_id not in list(request.session['visited'].keys()):
					request.session['visited'][inv_id] = 1
					print(request.session['visited'],"2")
				else:
					request.session['visited'][inv_id] += 1
					print(request.session['visited'],"3")
			request.session.modified = True
			if item_id not in cart:
				cart.append(item_id)
				request.session['cart'] = cart
				items=len(cart)	
				it = Item.objects.get(item_id=item_id)
				prods.append(it)
				total+=it.item_desc.price
			return render(request, 'store/cart.html',
						  {'first_name': fname, 'credits': credits, 'items': items, 'prods': prods,'total':total,'id':id1, 'item':item_id})



def productReg(request):
	if request.method == 'POST':
		form = ProdRegistration(request.POST)
		if form.is_valid():

			desc = ItemDesc.objects.create(age=form.cleaned_data['age'], name=form.cleaned_data['product_name'],
										   comments=form.cleaned_data['additional_information'],
										   price=form.cleaned_data['price'])
			desc.save()

			loc = Location.objects.create(zip_code=form.cleaned_data['zip_code'], city_name=form.cleaned_data['city'],
										  address=form.cleaned_data['address'])
			loc.save()

			inv = Inventory.objects.create(category=form.cleaned_data['category'])
			inv.save()

			seller_obj = User.objects.get(u_id=request.session['id'])

			itemObj = Item.objects.create(item_desc=desc, item_status=0, item_seller=seller_obj, item_location=loc,
										  item_inventory=inv)
			itemObj.save()
			request.session['items'] = len(request.session.get('cart')) + 1
			prods = Item.objects.filter(item_seller=seller_obj)
			return render(request, 'store/sales.html',
						  {'first_name': request.session['first_name'], 'credits': request.session['credits'],
						   'id': request.session['id'], 'is_seller': request.session['is_seller'], 'prods': prods})
	else:
		form = ProdRegistration()
		fname = request.session.get('first_name')
		credits = request.session.get('credits')
		items = len(request.session.get('cart'))
		id = request.session.get('id')
		is_seller = request.session.get('is_seller')
		return render(request, 'store/product_reg.html',
				  {'form': form, 'first_name': fname, 'credits': credits, 'items': items, 'is_seller': is_seller,
				   'id': id})
