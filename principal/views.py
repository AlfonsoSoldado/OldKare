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
from django.views.generic import TemplateView, ListView, DetailView
from .models import Service
from .forms import ServiceForm

# Create your views here.

class OldKareListView(LoginRequiredMixin, ListView):
    template_name = 'principal/OldKare.html'
    model = Service
    context_object_name = 'services'

    def get_queryset(self, *args, **kwargs):
        return Service.objects.filter(author=self.request.user)


class ServiceDetailView(LoginRequiredMixin, DetailView):
    template_name = 'principal/details.html'
    model = Service
    context_object_name = 'service'

class IndexView(TemplateView):
    template_name = 'principal/index.html'

@login_required
def add(request):

    if request.method == 'POST':
        form = ServiceForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            date = form.cleaned_data['date']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            avaliability = form.cleaned_data['avaliability']

            Service.objects.create(
                name=name,
                author=request.user,
                date=date,
                description=description,
                price=price,
                avaliability=avaliability,
            ).save()

            return HttpResponseRedirect('/')

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
            birthday = form.cleaned_data['birthday']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/OldKare')

    else:
        form = MyRegistrationForm()

    return render(request, 'registration/signup.html', {'form': form})