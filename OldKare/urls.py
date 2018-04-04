"""OldKare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from principal import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    path('', views.IndexView.as_view(), name='index'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('oldkare', views.OldKareListView.as_view(), name='OldKare'),
    path('oldkareall', views.OldKareAllListView.as_view(), name='OldKare'),
    path('signup', views.register_user, name='signup'),
    path('update-user-details/<int:pk>', views.userView.as_view(), name="updateUserDetails"),
    path('userDetails/<int:pk>', views.userDetailsView.as_view(), name='userDetails'),
    path('add-user-details', views.addUserDetails, name="addUserDetails"),
    path('login', auth_views.login, name='login'),
    path('logout', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('service/<int:pk>', views.ServiceDetailView.as_view(), name='details'),
    path('service/add', views.add, name='add'),
    path('service/delete/<int:pk>', views.delete, name='delete'),
    path('service/apply/<int:pk>', views.apply.as_view(), name="apply"),
    path('sobre-nosotros', TemplateView.as_view(template_name="principal/about-us.html")),
    path('terminos-y-condiciones', TemplateView.as_view(template_name="principal/termsAndConditions.html")),
)