from django.shortcuts import render, redirect, get_object_or_404
from django.http import StreamingHttpResponse
from django.shortcuts import render
import json
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.contrib.admin import AdminSite
from django.http import JsonResponse
from .forms import ContactForm, UserProfileForm, UpdateProfile, AgentForm, PropertyForm, UpdateAgentForm,PropertyImagesForm, OrdersForm
from .models import UserProfile, Admin, Contact, Agent, Property, PropertyImages, AccountType,Orders
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
import json

# Create your views here.

def home(request):

    if request.method=="POST":
        request.session.flush()

        email = request.POST["email"]
        password = request.POST["password"]

        user = User.objects.filter(email__iexact=email).exists()

        if user:
            user = User.objects.filter(email__iexact = request.POST["email"])[0]
            if check_password(password,user.password):
                request.session['logged_in'] = {'username':user.first_name, 'id':user.id}

                return redirect('home')


        context = {

                'no_match':True
            }

        return render(request, 'home.html', context)

    return render(request, 'home.html')


def signup(request):

    if request.method == "POST":
        user = User.objects.create_user(request.POST["email"], request.POST["email"], request.POST["password"])
        user.first_name = request.POST["firstname"]
        user.last_name = request.POST["lastname"]

        user.save()
        form = UserProfileForm({'user_name':user, 'website':'', 'bioInfo':'', 'mobile':''})

        if form.is_valid():
            print("hello")
            instance = form.save(commit=False)
            instance.save()
        else:
            print(form.errors)
        request.session['logged_in'] = {'username':user.first_name, 'id':user.id}

        return redirect('package-list')


    request.session.flush()

    return render(request, 'signup.html')

def add_property(request):
    if 'logged_in' in request.session:
        return render(request,'add-property.html')
    else:
        return redirect('signup')

def validate_email(request):
    email = request.GET.get("email", None)

    data = {

        'exists' : User.objects.filter(email__iexact=email).exists()
    }

    return JsonResponse(data)


def package_list(request):
    if 'logged_in' in request.session:
        packages = AccountType.objects.all()
        return render(request, 'package-list.html',{'packages':packages})
    else:
        return redirect('signup')


def checkout(request):
    if 'logged_in' in request.session:
        if request.method == "POST":
            id  = request.POST['price']
            package = get_object_or_404(AccountType, id=id)
            return render(request, 'checkout.html',{'package':package})
        else:
            return redirect('package-list')
    else:
        return redirect('signup')

def my_listing(request):
    if 'logged_in' in request.session:
        return render(request, 'my-listing.html')
    else:
        return redirect('signup')

def header_search(request):
    if request.method=="POST":
        values = request.POST.copy()
        for key in values:
            if "All" in values[key] or 'bed' in values[key] or 'Bath' in values[key]:
                values[key] = ''
        print(values)


        properties = Property.objects.filter(location__icontains=values['address']) | Property.objects.filter(type__icontains=values['type']) | Property.objects.filter(state__icontains=values['state']) | Property.objects.filter(city__icontains=values['city']) | Property.objects.filter(location__icontains=values['country'])| Property.objects.filter(no_of_beds__icontains=values['bed']) | Property.objects.filter(no_of_bathrooms__icontains=values['bath'])

        if values['price-from'] != '' and values['price-to']!='':
            properties = Property.objects.filter(price__range=(values['price-form'], values['price-to']))

        return render(request, 'search-results.html', {'properties':properties})
    else:
        return redirect('home')

def orderCompleted(request):
    if 'logged_in' in request.session:
        body = json.loads(request.body)
        package_id = get_object_or_404(AccountType,id=body['id'])
        user_id = get_object_or_404(User, id=request.session['logged_in']['id'])
        method = body['method']

        form = OrdersForm({'package_id':package_id, 'user_id':user_id, 'method':method})
        if(form.is_valid()):
            instance = form.save(commit=False)
            instance.save()



        return JsonResponse({'data':'Payment Completed!'}, safe=False)
    else:
        return redirect('signup')

def success(request):
    if 'logged_in' in request.session:
        order = Orders.objects.all().order_by('-id')[0]

        return render(request, 'order_completed.html',{'order':order})

    else:
        return redirect('signup')


def account_settings(request):
    if 'logged_in' in request.session:
        user = User.objects.filter(id=request.session["logged_in"]['id'])[0]
        instance = get_object_or_404(UserProfile, user_name=user)

        if request.method == "POST":
            user.first_name = request.POST["firstname"]
            user.last_name = request.POST["lastname"]
            user.email = request.POST["email"]
            user.save()
            form = UpdateProfile({'website':request.POST['website'], 'bioInfo':request.POST['bioInfo'], 'mobile':request.POST['mobile']}, instance=instance)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.save()
            else:
                print(form.errors)


        return render(request, 'account-settings.html', {'user':user, 'profile':instance})

    else:
        return redirect('home')

def listing_emails(request):
    if 'logged_in' in request.session:
        return render(request, 'listing-emails.html')
    else:
        return redirect('home')

def change_password(request):
    if 'logged_in' in request.session:
        user = User.objects.filter(id=request.session["logged_in"]['id'])[0]
        user.password = make_password(request.POST["password"])
        user.save()
        return redirect('account-settings')
    else:
        return redirect('home')

def logout(request):
    if 'logged_in' in request.session:
        request.session.flush()

    return redirect('home')


def agents(request):
    agents = Agent.objects.all().order_by('-id')


    return render(request, 'agents.html', {'agents':agents})

def individualAgent(request, id):
    agent = get_object_or_404(Agent, id=id)
    property = Property.objects.filter(agent=agent)

    return render(request, 'individualAgent.html', {'agent':agent, 'property':property})

def properties(request, type):
    properties = Property.objects.filter(status=type)

    return render(request, 'properties.html',{'properties':properties})


def property(request, id):
    property = get_object_or_404(Property, id=id)
    property_images = PropertyImages.objects.filter(property=property)

    business_id = '4AErMBEoNzbk7Q8g45kKaQ'
    unix_time = 1546047836

    # Define my API Key, My Endpoint, and My Header
    API_KEY = 'YiBwj8bxi1Pp9-bovZxu9sYH5-X3zY21qM2xIVwREucbPjQNMzfDgL9psyKDN3fqz6c6fEXJL51GtoXN9nrIrqnrQUQWCYJ8xTC7cyLyamkrHn92OLT3CbLWXnlqXnYx'
    ENDPOINT = 'https://api.yelp.com/v3/businesses/search'.format(business_id)
    HEADERS = {'Authorization': 'bearer %s' % API_KEY}

    # Define my parameters of the search
    # BUSINESS SEARCH PARAMETERS - EXAMPLE
    hospitals = {'term': 'hospital',
                  'offset': 3,
                  'limit': 3,
                  'radius': 1000,
                  'latitude': property.latitude,
                  'longitude' : property.longitude,
                  'sort_by' : 'distance'
                 }
    malls = {'term': 'shopping',
                  'offset': 3,
                  'limit': 3,
                  'radius': 1000,
                 'latitude': property.latitude,
                 'longitude' : property.longitude,
                 'sort_by' : 'distance'
             }

    restaraunts = {'term': 'restaraunts',
             'offset': 3,
             'limit': 3,
             'radius': 1000,
            'latitude': property.latitude,
            'longitude' : property.longitude,
            'sort_by' : 'distance'}

    coffee = {'term': 'coffee',
             'offset': 3,
             'limit': 3,
             'radius': 1000,
              'latitude': property.latitude,
              'longitude' : property.longitude,
              'sort_by' : 'distance'}

    grocery = {'term': 'grocery',
             'offset': 3,
             'limit': 3,
             'radius': 1000,
            'latitude': property.latitude,
            'longitude' : property.longitude,
            'sort_by' : 'distance'}

    education = {'term': 'education',
             'offset': 3,
             'limit': 3,
             'radius': 1000,
            'latitude': property.latitude,
            'longitude' : property.longitude,
            'sort_by' : 'distance'}



    # BUSINESS MATCH PARAMETERS - EXAMPLE
    # PARAMETERS = {'name': 'Peets Coffee & Tea',
    #              'address1': '7845 Highland Village Pl',
    #              'city': 'San Diego',
    #              'state': 'CA',
    #              'country': 'US'}

    # Make a request to the Yelp API
    response = requests.get(url = ENDPOINT, params = hospitals, headers = HEADERS)
    response2 = requests.get(url = ENDPOINT, params = malls, headers = HEADERS)
    response3 = requests.get(url = ENDPOINT, params = restaraunts, headers = HEADERS)
    response4 = requests.get(url = ENDPOINT, params = coffee, headers = HEADERS)
    response5 = requests.get(url = ENDPOINT, params = grocery, headers = HEADERS)
    response6 = requests.get(url = ENDPOINT, params = education, headers = HEADERS)

    # Conver the JSON String
    business_data = [response.json(), response2.json(), response3.json(), response4.json(), response5.json(), response6.json()]


# print the response
    print(json.dumps(business_data[0], indent = 3))

    return render(request,'property.html',{'property':property, 'property_images':property_images, 'business_data':business_data})


def search_results(request):
    if request.method == "POST":
        search = request.POST["search"]

        properties = Property.objects.filter(city__icontains=search) | Property.objects.filter(state__icontains=search) | Property.objects.filter(location__icontains=search) | Property.objects.filter(title__icontains=search)
        return render(request, 'search-results.html',{'properties':properties})
    else:
        return redirect('home')

def aboutus(request):
    return render(request, 'aboutus.html')


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return render(request, 'contact.html', {'message': True})

    return render(request, 'contact.html')

def admin(request):
    request.session.flush()

    if request.method == "POST":
        ad = Admin.objects.filter(username=request.POST["username"]).exists()

        if ad:
            ad = Admin.objects.filter(username=request.POST["username"])[0]
            if check_password(request.POST["password"], ad.password):
                request.session['admin'] = ad.id
                return redirect('adminDashboard')
        return render(request, 'admin/admin-login.html', {'no_match': True})


    return render(request, 'admin/admin-login.html')

def adminDashboard(request):

    if 'admin' in request.session:
        agents = Agent.objects.all().count()
        messages = Contact.objects.all().count()
        properties = Property.objects.all().count()
        users = User.objects.all().count()

        return render(request, 'admin/admin_dashboard.html', {'agents':agents, 'messages':messages, 'properties':properties, 'users':users})
    else:
        return redirect('admin')

def adminInbox(request):
    if 'admin' in request.session:
        messages = Contact.objects.all()

        context = {

            'Messages' : messages
        }
        return render(request, 'admin/adminInbox.html', context)
    else:
        return redirect('admin')

def deleteMessage(request, id):
    if 'admin' in request.session:
        instance = get_object_or_404(Contact, id=id)
        instance.delete()
        return redirect('adminInbox')
    else:
        return redirect('admin')

def message(request, id):
    if 'admin' in request.session:
        instance = get_object_or_404(Contact, id=id)
        return render(request, 'admin/message.html', {'message': instance})
    else:
        return redirect('admin')

def addAgent(request):
    if 'admin' in request.session:
        if request.method=="POST":
            form  = AgentForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return render(request, 'admin/addAgent.html', {'message': True})
            else:
                print(form.errors)

        return render(request, 'admin/addAgent.html')
    else:
        return redirect('admin')

def updateAgent(request, id):
    if 'admin' in request.session:
        instance = get_object_or_404(Agent, id=id)

        if request.method == "POST":
            form = UpdateAgentForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                save_form = form.save(commit=False)
                save_form.save()
                return redirect('allAgents')


        return render(request, 'admin/updateAgent.html',{'agent':instance})
    else:
        return redirect('home')


def allAgents(request):
    if 'admin' in request.session:
        agents = Agent.objects.all().order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(agents, 2)
        try:
            agents = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        return render(request, 'admin/allAgents.html',{'agents':agents})
    else:
        return redirect('admin')

def allProperty(request):
    if 'admin' in request.session:
        property = Property.objects.all().order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(property, 1)
        try:
            property = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        return render(request, 'admin/allProperty.html',{'properties':property})
    else:
        return redirect('admin')




def addProperty(request):
    if 'admin' in request.session:
        agents = Agent.objects.all()

        if request.method == "POST":
            files = request.FILES.getlist("photo")

            file = {'photo':files[0]}
            form = PropertyForm(request.POST, file)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                instance = Property.objects.all().order_by('-id')[0]

                for i in range(len(files)):

                    form = PropertyImagesForm({'property':instance}, {'photo':files[i]})
                    if form.is_valid():
                        instance2 = form.save(commit=False)
                        instance2.save()
                    else:
                        print(form.errors)
                return render(request, 'admin/addProperty.html', {'agents':agents, 'message': True})
            else:
                print(form.errors)


        return render(request, 'admin/addProperty.html', {'agents':agents})
    else:
        return redirect('admin')

def deleteProperty(request, id):
    if 'admin' in request.session:
        instance = get_object_or_404(Property, id=id)
        instance.delete()
        return redirect('allProperty')
    else:
        return redirect('admin')


def individualProperty(request, id):
    if 'admin' in request.session:
        property = get_object_or_404(Property, id=id)
        property_images = PropertyImages.objects.filter(property=property)

        return render(request, 'admin/individualProperty.html', {'property':property, 'property_images':property_images})
    else:
        return redirect('admin')

def deleteAgent(request, id):
    if 'admin' in request.session:
        instance = get_object_or_404(Agent, id=id)
        instance.delete()
        return redirect('allAgents')
    else:
        return redirect('admin')


def adminLogout(request):

    if 'admin' in request.session:
        request.session.flush()

    return redirect('home')