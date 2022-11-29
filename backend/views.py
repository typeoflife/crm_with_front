import datetime

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET

from backend.forms import EditOrderForm, CustomerForm, DeviceForm
from backend.models import Order


def check_order_owner(owner, request):
    if owner != request.user:
        raise Http404


def index(request):
    if request.user.is_authenticated:
        return render(request, 'backend/base.html')
    return render(request, 'backend/index.html')


def home(request):
    return render(request, 'backend/base.html')


@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /admin/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def orders(request):
    orders = Order.objects.select_related('device').select_related('customer').filter(
        user_id=request.user.id).order_by('-order_number')
    paginator = Paginator(orders, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'backend/orders.html', context)


def retrieve_order(request, order_id):
    order = Order.objects.select_related('device').get(id=order_id)
    check_order_owner(order.user, request)
    context = {'order': order}
    return render(request, 'backend/order.html', context)


def new_order(request):
    if request.method == "POST":
        customerform = CustomerForm(request.POST)
        deviceform = DeviceForm(request.POST)
        if deviceform.is_valid() and customerform.is_valid():
            device = deviceform.save(commit=False)
            customer = customerform.save(commit=False)
            device.save()
            customer.user_id = request.user.id
            customer.save()
            order = Order.objects.create(user=request.user, date_added=datetime.datetime.now(),
                                         order_number=Order.objects.filter(user_id=request.user.id).count() + 1,
                                         device_id=device.id, customer_id=customer.id)
            return redirect('order', order_id=order.id)
        else:
            context = {
                'customerform': customerform,
                'deviceform': deviceform,
            }
    else:
        context = {
            'customerform': CustomerForm(),
            'deviceform': DeviceForm(),
        }
    return render(request, 'backend/new_order.html', context)


def edit_order(request, order_id):
    """"Редактирует запись конкретного заказа"""
    order = Order.objects.select_related('device').get(id=order_id)
    # Проверка того, что тема принадлежит текущему пользователю
    check_order_owner(order.user, request)
    if request.method != 'POST':
        """Исходный запрос, форма заполняется данными текущей записи"""
        form = EditOrderForm(instance=order)
    else:
        """Отправка данных POST"""
        form = EditOrderForm(instance=order, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('order', order_id=order.id)

    context = {'order': order, 'form': form}
    return render(request, 'backend/edit_order.html', context)


def customers(request):
    user = User.objects.filter(username=request.user).first()
    customers = user.customers.all()
    paginator = Paginator(customers, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}

    return render(request, 'backend/customers.html', context)


def warehouse(request):
    return render(request, 'backend/warehouse.html')


def reports(request):
    return render(request, 'backend/reports.html')


def cash(request):
    return render(request, 'backend/cash.html')


def profile(request):
    return render(request, 'backend/profile.html')


# class NewOrders(APIView):
#     renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
#     template_name = 'backend/new_order.html'
#     queryset = Order.objects.all()
#     serializer_class = OrdersSerializer
#
#     def get(self, request):
#         orders = Order.objects.all().order_by('-order_number')
#         serializer = OrdersSerializer(orders)
#         return Response({'orders': orders, 'serializer': serializer})
#
#     def get_object(self, request, order_id, format=None):
#         order = Order.objects.get(id=order_id)
#         serializer = OrderSerializer(order)
#         if format == None:
#             return Response({'order': order, 'serializer': serializer}, template_name="contact/contact_detail.html")
