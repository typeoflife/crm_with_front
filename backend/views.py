import datetime

from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET

from backend.forms import OrderForm, EditOrderForm
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
    orders = Order.objects.filter(user_id=request.user.id).order_by('-order_number')
    context = {'orders': orders}
    return render(request, 'backend/orders.html', context)


def retrieve_order(request, order_id):
    order = Order.objects.get(id=order_id)
    check_order_owner(order.user, request)
    context = {'order': order}
    return render(request, 'backend/order.html', context)


def new_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.date_added = datetime.datetime.now()
            print(order.date_added)
            counter = Order.objects.filter(user_id=request.user.id).count() + 1
            order.order_number = counter
            order.save()
            return redirect('order', order_id=order.pk)
    else:
        form = OrderForm()
    return render(request, 'backend/new_order.html', {'form': form})


def edit_order(request, order_id):
    """"Редактирует запись конкретного заказа"""
    order = Order.objects.get(id=order_id)
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


def warehouse(request):
    return render(request, 'backend/warehouse.html')

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
