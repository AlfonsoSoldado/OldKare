from django import forms            
from django.contrib.auth.models import User   # fill in custom user info then save it 
from django.contrib.auth.forms import UserCreationForm 
from .models import UserDetails, Service, Curriculum, Feedback, Order
import django_filters

class MyRegistrationForm(UserCreationForm):
    username = forms.CharField(label = "Nombre de usuario")
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Nombre")
    last_name = forms.CharField(label = "Apellidos")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')        

    def save(self,commit = True):   
        user = super(MyRegistrationForm, self).save(commit = False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user

class DateInput(forms.DateInput):
    input_type = 'date'

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('name', 'description', 'category', 'price') 

class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ('birthday', 'phone', 'postalAddress', 'gender', 'occupation', 'photo', 'socialReferences')
        widgets = {
            'birthday': DateInput(),
        } 

class CurriculumForm(forms.ModelForm):
    class Meta:
        model = Curriculum
        fields = ('personalData', 'experience', 'education', 'misc')

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('rate', 'description')

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city','service']

class ServiceFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    price__gt = django_filters.NumberFilter(name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(name='price', lookup_expr='lt')

    class Meta:
        model = Service
        fields = ['name']