from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect    
from django.contrib import auth                 
from principal.forms import MyRegistrationForm
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, View
from .models import Service, UserDetails, Curriculum, Feedback, Order
from .forms import ServiceForm, UserDetailsForm, CurriculumForm, FeedbackForm, OrderCreateForm
from django.db.models import F
from django.contrib.auth.models import User
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings



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
    def get_queryset(self, *arg, **kwargs):
        return Service.objects.all().order_by('-created')

class ServiceDetailView(DetailView):
    template_name = 'principal/details.html'
    model = Service
    context_object_name = 'service'

class updateService(UpdateView):
    template_name = 'principal/form.html'
    model = Service
    form_class = ServiceForm

class ServiceDelete(DeleteView):
    model = Service
    success_url = reverse_lazy('index')

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
    fields = []
    def form_valid(self, form):
        service = Service.objects.get(pk=self.kwargs.get('pk'))
        offerer = self.request.user
        service.offerer.add(offerer)
        return HttpResponseRedirect(self.get_success_url())

class IndexView(TemplateView):
    template_name = 'principal/index.html'

class curriculumView(DetailView):
    template_name = 'principal/curriculum.html'
    model = Curriculum
    context_object_name = 'curriculum'

class curriculumUpdate(UpdateView):
    template_name = 'principal/updateCurriculumForm.html'
    model = Curriculum
    fields = ['personalData', 'experience', 'education', 'misc']

class CurriculumDelete(DeleteView):
    model = Curriculum
    success_url = reverse_lazy('index')

class feedbackView(ListView):
    template_name = 'principal/feedback.html'
    model = Feedback
    context_object_name = 'feedback'

    def get_queryset(self, *arg, **kwargs):
        service = Service.objects.get(pk=self.kwargs.get('pk'))
        return Feedback.objects.filter(service=service)


class feedbackUpdate(UpdateView):
    template_name = 'principal/addFeedbackForm.html'
    model = Feedback
    fields = ['ranking', 'description']

class feedbackDelete(DeleteView):
    model = Feedback
    success_url = reverse_lazy('index')

class ServicePay(View):
    model = Service
    success_url = reverse_lazy('index')

@login_required
def pay(request, pk):

        service = get_object_or_404(Service, pk=pk)
        servicePrice = service.price
        request.session['service_id'] = service.id
        paypal_dict = {
        "business": settings.PAYPAL_RECIEVER_EMAIL,
        "amount": servicePrice,
        "item_name": "service",
        "invoice": "unique-invoice-id",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri('done'),
        "cancel_return": request.build_absolute_uri('canceled'),
        "custom": "premium_plan",  
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {"form": form}
        return render(request, "principal/process.html",context)


@login_required
def add(request):

    if request.method == 'POST':
        form = ServiceForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            price = form.cleaned_data['price']

            Service.objects.create(
                name=name,
                author=request.user,
                description=description,
                category=category,
                price=price,
                avaliability=1,
            ).save()

            return HttpResponseRedirect('/services')

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
            return redirect('/')

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

    return render(request, 'principal/userDetailsForm.html', {'form': form})



@login_required
def addCurriculum(request):

    if request.method == 'POST':
        form = CurriculumForm(request.POST)
        if form.is_valid():
            personalData = form.cleaned_data['personalData']
            experience = form.cleaned_data['experience']
            education = form.cleaned_data['education']
            misc = form.cleaned_data['misc']

            Curriculum.objects.create(
                user=request.user,
                personalData=personalData,
                experience=experience,
                education=education,
                misc=misc,
            ).save()

            return HttpResponseRedirect('/')

    else:
        form = CurriculumForm()

    return render(request, 'principal/addCurriculumForm.html', {'form': form})


@login_required
def addFeedback(request, pk):

    if request.method == 'POST':
        form = FeedbackForm(request.POST)

        if form.is_valid():
            ranking = form.cleaned_data['ranking']
            description = form.cleaned_data['description']

            fed = Feedback.objects.create(
                ranking=ranking,
                description=description,
            )
            
            fed.save()
            
            service = Service.objects.get(pk=pk)
            service.feedback.add(fed)
            service.save()

            return HttpResponseRedirect('/')

    else:
        form = FeedbackForm()

    return render(request, 'principal/addFeedbackForm.html', {'form': form})


def order_done(request):
    solicitante = request.user
    service_id = request.session.get('service_id')
    service  = get_object_or_404(Service, id=service_id)
    
    service.avaliability = 0
    service.offerer.add(solicitante)
    service.save()
    return HttpResponseRedirect('/services/requested')

def order_canceled(request):
    service_id = request.session.get('service_id')
    url = "/service/"+str(service_id)
    return HttpResponseRedirect(url)

class requestedListView(LoginRequiredMixin, ListView):
    template_name = 'principal/OldKare.html'
    model = Service
    context_object_name = 'services'

    def get_queryset(self, *arg, **kwargs):
        return Service.objects.filter(offerer=self.request.user)