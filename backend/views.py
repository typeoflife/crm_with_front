import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET

from backend.forms import EditOrderForm, CustomerForm, DeviceForm, CashForm
from backend.models import Order, Cash


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
    cash = Cash.objects.filter(user_id=request.user.id)
    check_order_owner(order.user, request)
    context = {'order': order, 'cash': cash}
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
            messages.success(request, 'Заказ создан')
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
    order = Order.objects.select_related('device').get(id=order_id)
    # Проверка того, что заказ принадлежит текущему пользователю
    check_order_owner(order.user, request)
    if request.method != 'POST':
        """Исходный запрос, форма заполняется данными текущей записи"""
        form = EditOrderForm(instance=order)
    else:
        """Отправка данных POST"""
        form = EditOrderForm(instance=order, data=request.POST)
        if form.is_valid():
            form.save()
            messages.warning(request, 'Заказ изменен')
            return redirect('order', order_id=order.id)

    context = {'order': order, 'form': form}
    return render(request, 'backend/edit_order.html', context)


def close_order(request, order_id):
    try:
        order = Order.objects.select_related('device').exclude(status='close').get(
            id=order_id, user_id=request.user.id)
        if request.method == "POST":
            cash = request.POST.get('cash')
            if not cash:
                messages.error(request, 'Выберите кассу')
                return redirect('order', order_id=order.id)
            else:
                user_cash = Cash.objects.get(name=cash, user_id=request.user)
                user_cash.money += order.summ
                order.status = 'close'
                user_cash.save()
                order.save()
                messages.success(request, 'Заказ закрыт')
                return redirect('order', order_id=order.id)
    except Order.DoesNotExist:
        messages.error(request, 'Заказ уже закрыт')
        return redirect('order', order_id=order_id)


def customers(request):
    user = User.objects.filter(username=request.user).first()
    customers = user.customers.all()
    paginator = Paginator(customers, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}

    return render(request, 'backend/customers.html', context)


def cash(request):
    cash = Cash.objects.filter(user_id=request.user)
    context = {'cash': cash}
    return render(request, 'backend/cash.html', context)


def one_cash(request, cash_id):
    cash = Cash.objects.get(user_id=request.user.id, id=cash_id)
    # check_order_owner(order.user, request)
    context = {'cash': cash}
    return render(request, 'backend/one_cash.html', context)


def new_cash(request):
    if request.method == "POST":
        form = CashForm(request.POST)
        if form.is_valid():
            cash = form.save(commit=False)
            cash.user = request.user
            all_user_cash = Cash.objects.filter(user_id=request.user).values_list('name', flat=True)
            if cash.name in all_user_cash:
                messages.error(request, 'Касса с таким именем уже существует')
                return redirect('cash')
            cash.save()
            return redirect('cash')
    else:
        form = CashForm()
    return render(request, 'backend/new_cash.html', {'form': form})


def warehouse(request):
    return render(request, 'backend/warehouse.html')


def reports(request):
    return render(request, 'backend/reports.html')


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
