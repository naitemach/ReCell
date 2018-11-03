from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm, RegisterForm
from .models import User, Location, Wallet,Order
from django.db import connection


def login(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = LoginForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			email = form.cleaned_data['email']
			user_obj = User.objects.filter(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
			order_obj = Order.objects.filter(b_id=user_obj.get().u_id)
			if user_obj.exists():
				request.session['email'] = email
				request.session['first_name'] = user_obj.get().first_name
				request.session['id'] = user_obj.get().u_id
				request.session['credits'] = user_obj.get().wall.credits
				request.session['items'] = order_obj.get().items.count()
				return render(request, 'store/index.html', {'first_name': request.session['first_name'],'credits':request.session['credits'],'items':request.session['items'],'id':request.session['id']})

			return render(request, 'store/form.html', {'form': form, 'email': email})

	# if a GET (or any other method) we'll create a blank form
	else:
		form = LoginForm()

	return render(request, 'store/login.html', {'form': form})


def index(request):
	fname = request.session.get('first_name')
	credits = request.session.get('credits')
	items = request.session.get('items')
	if fname != None and credits != None:
		return render(request,'store/index.html',{'first_name':fname,'credits':credits,'items':items})
	else:
		return HttpResponse("Fname couldnt be passes succesfully")

def catResults(request):
	fname = request.session.get('first_name')
	credits = request.session.get('credits')
	items = request.session.get('items')

	if credits != None:
		return render(request, 'store/cat_results.html', {'first_name':fname,'credits':credits,'items':items})	
	else:
		return HttpResponse("Fname couldnt be passes succesfully")
	

def productDetails(request):
	fname = request.session.get('first_name')
	credits = request.session.get('credits')
	items = request.session.get('items')

	if fname != None and credits != None:
		return render(request, 'store/product_details.html', {'first_name':fname,'credits':credits,'items':items})
	else:
		return HttpResponse("Fname couldnt be passes succesfully")


def register(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            email = form.cleaned_data['email']
            user_obj = User.objects.filter(email=form.cleaned_data['email'])
            if user_obj.exists():
                error = "Account with given Email ID already exists"
                return render(request, 'store/register.html', {'error': error})
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            loci = Location.objects.create()
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

            request.session['email'] = email
            request.session['first_name'] = first_name
            request.session['id'] = id
            return render(request, 'store/register.html', {})
            # return render(request, 'store/index.html', {'username': request.session['username']})

        return render(request, 'store/form.html', {'form': form, })

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()

    # return render(request, 'store/login.html', {'form': form})
    return render(request, 'store/register.html', {'form':form})


def search(request):
	fname = request.session.get('first_name')
	credits = request.session.get('credits')
	items = request.session.get('items')

	if credits != None:
		return render(request, 'store/search_results.html', {'first_name':fname,'credits':credits,'items':items})	
	else:
		return HttpResponse("Fname couldnt be passes succesfully")


def display(request):
	fname = request.session.get('first_name')
	cursor = connection.cursor()
	cursor.execute('SELECT * FROM store_item')
	item = cursor.fetchone()
	id = item[2]
	cursor.execute('SELECT * FROM store_itemdesc where item_desc_id = %s', [id])
	itemdesc = cursor.fetchone()

	return render(request, 'store/display.html', {'item': item, 'itemdesc': itemdesc,'first_name':fname,'items':items})

def productSummary(request):
	fname = request.session.get('first_name')
	credits = request.session.get('credits')
	items = request.session.get('items')

	if credits != None:
		return render(request, 'store/product_summary.html', {'first_name':fname,'credits':credits,'items':items})	
	else:
		return HttpResponse("Fname couldnt be passes succesfully")

def productReg(request):
	fname = request.session.get('first_name')
	credits = request.session.get('credits')
	items = request.session.get('items')

	if fname != None and credits != None:
		return render(request, 'store/product_reg.html', {'first_name':fname,'credits':credits,'items':items})
