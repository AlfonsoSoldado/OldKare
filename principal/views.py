from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect    
from django.contrib import auth                 
from principal.forms import MyRegistrationForm
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from .models import Service, UserDetails
from .forms import ServiceForm, UserDetailsForm
from django.db.models import F
from django.contrib.auth.models import User

# Create your views here.

class OldKareListView(LoginRequiredMixin, ListView):
    template_name = 'principal/OldKare.html'
    model = Service
    context_object_name = 'services'

    def get_queryset(self, *arg, **kwargs):
        return Service.objects.filter(author=self.request.user)

class OldKareAllListView(ListView):
    template_name = 'principal/OldKareAll.html'
    model = Service
    context_object_name = 'services'

class ServiceDetailView(DetailView):
    template_name = 'principal/details.html'
    model = Service
    context_object_name = 'service'

class userDetailsView(DetailView):
    template_name = 'principal/userDetailsView.html'
    model = UserDetails
    context_object_name = 'userDetails'

class userView(UpdateView):
    template_name = 'principal/userDetailsForm.html'
    model = UserDetails
    form_class = UserDetailsForm

class apply(UpdateView):
    template_name = 'principal/applyServiceForm.html'
    model = Service
    fields = ['offerer']
    

class IndexView(TemplateView):
    template_name = 'principal/index.html'

@login_required
def add(request):

    if request.method == 'POST':
        form = ServiceForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            avaliability = form.cleaned_data['avaliability']

            Service.objects.create(
                name=name,
                author=request.user,
                description=description,
                price=price,
                avaliability=avaliability,
            ).save()

            return HttpResponseRedirect('/oldkare')

    else:
        form = ServiceForm()

    return render(request, 'principal/form.html', {'form': form})

@login_required
def delete(request, pk):

    if request.method == 'DELETE':
        service = get_object_or_404(Service, pk=pk)
        service.delete()

    return HttpResponseRedirect('/')

def register_user(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)     # create form object
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/add-user-details')

    else:
        form = MyRegistrationForm()

    return render(request, 'registration/signup.html', {'form': form})

@login_required
def addUserDetails(request):

    if request.method == 'POST':
        form = UserDetailsForm(request.POST)
        if form.is_valid():
            birthday = form.cleaned_data['birthday']
            phone = form.cleaned_data['phone']
            postalAddress = form.cleaned_data['postalAddress']
            gender = form.cleaned_data['gender']
            occupation = form.cleaned_data['occupation']
            photo = form.cleaned_data['photo']
            socialReferences = form.cleaned_data['socialReferences']

            UserDetails.objects.create(
                user=request.user,
                birthday=birthday,
                phone=phone,
                postalAddress=postalAddress,
                gender=gender,
                occupation=occupation,
                photo=photo,
                socialReferences=socialReferences
            ).save()

            return HttpResponseRedirect('/')

    else:
        form = UserDetailsForm()

    return render(request, 'principal/AddUserDetailsForm.html', {'form': form})