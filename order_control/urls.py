from django.contrib import admin
from django.urls import path, include
from allauth.account.views import SignupView, LoginView, LogoutView
from backend.views import robots_txt, customers, cash, reports, profile, new_cash, close_order, one_cash
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
    path('one_cash/<int:cash_id>', one_cash, name='one_cash'),
    path('new_cash/', new_cash, name='new_cash'),
    path('reports/', reports, name='reports'),
    path('profile/', profile, name='profile'),
    path('order/<int:order_id>', retrieve_order, name='order'),
    path('new_order/', new_order, name='new_order'),
    path('orders/', orders, name='orders'),
    path('close_order/<int:order_id>', close_order, name='close_order'),
    path('edit_sum/<int:order_id>', edit_order, name='edit_order'),
    path('accounts/signup/', SignupView.as_view(), name='signup'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
]
