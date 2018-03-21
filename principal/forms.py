from django import forms            
from django.contrib.auth.models import User   # fill in custom user info then save it 
from django.contrib.auth.forms import UserCreationForm 
from .models import UserDetails

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

class ServiceForm(forms.Form):
    name = forms.CharField(max_length=100)
    date = forms.DateTimeField()
    description = forms.CharField(widget=forms.Textarea)
    price = forms.DecimalField(max_digits=20, decimal_places=2)
    avaliability = forms.IntegerField()

class UserDetailsForm(forms.ModelForm):
    birthday = forms.DateTimeField()
    phone = forms.CharField(max_length=100)
    postalAddress = forms.CharField(max_length=100)
    gender = forms.CharField(max_length=100)
    occupation = forms.CharField(max_length=100,widget=forms.Textarea)
    photo = forms.CharField(max_length=100)
    socialReferences = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = UserDetails
        fields = ('birthday', 'phone', 'postalAddress', 'gender', 'occupation', 'photo', 'socialReferences') 