from django.contrib import admin
from django.urls import path, include
from allauth.account.views import SignupView, LoginView, LogoutView
from backend.views import robots_txt, customers, cash, reports, profile
from backend.views import index, home, warehouse, orders, retrieve_order, new_order, edit_order

urlpatterns = [
    path('', index),
    path("robots.txt", robots_txt),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('home/', home, name='home'),
    path('warehouse/', warehouse, name='warehouse'),
    path('customers/', customers, name='customers'),
    path('cash/', cash, name='cash'),
    path('reports/', reports, name='reports'),
    path('profile/', profile, name='profile'),
    path('order/<order_id>', retrieve_order, name='order'),
    path('new_order/', new_order, name='new_order'),
    path('orders/', orders, name='orders'),
    path('edit_sum/<int:order_id>', edit_order, name='edit_order'),
    path('accounts/signup/', SignupView.as_view(), name='signup'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
]
