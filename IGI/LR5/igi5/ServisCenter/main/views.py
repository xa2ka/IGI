from django.shortcuts import render, redirect
from .models import FAQ, Contaсts, News, Vacancion, Discount, User,  Comment, Supplier, Detail, Order,OrderItem,Time,PickupAddresses
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime
import re
import pytz
from datetime import datetime
import calendar
import requests
from loguru import logger

from collections import Counter


logger.add("debug.log", format="{time} {level} {message}", level="DEBUG")


def get_cat_fact():
    url = 'https://catfact.ninja/fact'

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def CheckOrders(request):
    suppliers = list(Supplier.objects.all().order_by('name'))
    orders = list(Order.objects.all().order_by('-purchase_date'))
    order_items = list(OrderItem.objects.all().order_by('OrderId'))
    details = list(Detail.objects.all())
    pickup_addresses = list(PickupAddresses.objects.all()) 
    context = {
        'suppliers': suppliers,
        'orders': orders,
        'order_items': order_items,
        'details': details,
        'pickup_addresses': pickup_addresses,
        'userId': int(request.session.get('user_id'))
    }
    return render(request, 'main/orders.html', context)

# def information(request):
#     suppliers = list(Supplier.objects.all().order_by('name'))
#     orders = list(Order.objects.all().order_by('-purchase_date'))
#     order_items = list(OrderItem.objects.all().order_by('OrderId'))

#     context = {
#         'suppliers': suppliers,
#         'orders': orders,
#         'order_items': order_items
#     }
#     return render(request, 'main/employee.html', context)


def employee(request):
    suppliers = list(Supplier.objects.all().order_by('name'))
    orders = list(Order.objects.all().order_by('-purchase_date'))
    order_items = list(OrderItem.objects.all().order_by('OrderId'))

    # Count the number of times each detail name appears in OrderItem
    detail_name_counts = Counter(item.NameOfDetail for item in order_items)

    # Get the detail name that appears most often
    most_ordered_detail_name = max(detail_name_counts, key=detail_name_counts.get)

    context = {
        'suppliers': suppliers,
        'orders': orders,
        'order_items': order_items,
        'most_ordered_detail': most_ordered_detail_name,
    }
    return render(request, 'main/employee.html', context)

def index(request):
    logger.debug("Rendering index page")
    # suppliers = list(Supplier.objects.all().order_by('name'))
    # orders = list(Order.objects.all().order_by('-purchase_date'))
    # order_items = list(OrderItem.objects.all().order_by('OrderId'))


    suppliers = list(Supplier.objects.all().order_by('name'))
    details = list(Detail.objects.all().order_by('name'))
    discounts = list(Discount.objects.all().order_by('min_quantity'))

    # context = {
    #     'suppliers': suppliers,
    #     'orders': orders,
    #     'order_items': order_items
    # }

    return render(request, 'main/main.html',{'suppliers': suppliers, 'details': details, 'discounts': discounts})

def about(request):
    logger.debug("Rendering about page")
    return render(request, 'main/about.html')

def about2(request):
    logger.debug("Rendering about2 page")
    print(int(request.session.get('user_id')))
    return render(request, 'main/userabout.html')

def login(request):
    logger.debug("Rendering login page")
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')

        try:
            user = User.objects.get(login=login, password=password)
            request.session['user_id'] = user.id
            if user.IsEmployee:
                return redirect('employee')
            else:
                return redirect('usermain')
        except User.DoesNotExist:
            messages.error(request, 'Неправильный логин или пароль')

    return render(request, 'main/login.html')

def registration(request):
    logger.debug("Rendering registration page")
    return render(request, 'main/registration.html')

def news(request):
    logger.debug("Rendering news page")
    new = News.objects.all()
    return render(request, 'main/news.html', {'new': new})

def contacts(request):
    logger.debug("Rendering contacts page")
    Contact = Contaсts.objects.all()
    return render(request, 'main/contacts.html', {'Contact': Contact})

def contacts2(request):
    logger.debug("Rendering contacts2 page")
    Contact = Contaсts.objects.all()
    return render(request, 'main/usercontacts.html', {'Contact': Contact})

def policy(request):
    logger.debug("Rendering policy page")
    return render(request, 'main/policy.html')

def policy2(request):
    logger.debug("Rendering policy2 page")
    return render(request, 'main/userpolicy.html')

def vacancies(request):
    logger.debug("Rendering vacancies page")
    vacancion = Vacancion.objects.all()
    return render(request, 'main/vacancies.html',{'vacancion': vacancion})

def vacancies2(request):
    logger.debug("Rendering vacancies2 page")
    vacancion = Vacancion.objects.all()
    return render(request, 'main/uservacancies.html',{'vacancion': vacancion})

def feedback(request):
    logger.debug("Rendering feedback page")
    comments = reversed(Comment.objects.all())
    return render(request, 'main/feedback.html',{'comments': comments})

def feedback2(request):
    if request.method == 'POST':
        obj = User.objects.get(id=int(request.session.get('user_id')))
        name = obj.fullName
        comment = request.POST.get('comment')
        mark = request.POST.get('mark')

        if comment != '':
            Comment.objects.create(UserName=name, text=request.POST.get('comment'), data=datetime.now(), mark=request.POST.get('mark'))
    comments = reversed(Comment.objects.all())
    return render(request, 'main/userfeedback.html',{'comments': comments})


def discount(request):
    discounts = Discount.objects.all()
    return render(request, 'main/discounts.html',{'discounts': discounts})


def discount2(request):
    discounts = Discount.objects.all()
    return render(request, 'main/userdiscounts.html',{'discounts': discounts})


def contact_view(request):
    if request.method == 'POST':
        age_check = request.POST.get('ageCheck')
        if age_check == 'on':
            login = request.POST.get('login')
            password = request.POST.get('password')
            fullName = request.POST.get('secondName') + ' ' + request.POST.get('frstName') + ' ' + request.POST.get('lastName')
            phone = request.POST.get('phone')
            is_employee = request.POST.get('is_employee') == 'true'  # Получаем значение is_employee из формы
            phone_pattern = re.compile(r'^\+375 \(29\) \d{3}-\d{2}-\d{2}$')

            if not phone_pattern.match(phone):
                error_message = "Введите телефон в формате +375 (29) XXX-XX-XX"
                return render(request, 'main/registration.html', {'error_message': error_message})

            # Создаем запись в базе данных
            User.objects.create(login=login, password=password, fullName=fullName, phone=phone, IsEmployee=is_employee)

            last_obj = User.objects.order_by('-id').first()
            last_id = last_obj.id if last_obj else 0
            request.session['user_id'] = last_id
        else:
            return redirect('usermain')  # Перенаправление на страницу успеха после сохранения
    return render(request, 'main/registration.html')


def MyRequest(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('records')
        selected_details = Detail.objects.filter(id__in=selected_ids)

        # Вычисляем общую сумму заказа без скидки
        total_sum = sum(detail.price for detail in selected_details)

        # Находим подходящую скидку
        discount = Discount.objects.filter(min_quantity__lte=selected_details.count()).order_by('-min_quantity').first()
        if discount:
            discounted_sum = total_sum * (1 - discount.discount / 100)
        else:
            discounted_sum = total_sum

        # Создаем один заказ
        order = Order.objects.create(
            UserId=int(request.session.get('user_id')),
            quantity=selected_details.count(),
            purchase_date=timezone.now(),
            sum=discounted_sum
        )

        # Создаем записи в OrderItem для каждой детали
        for selected_detail in selected_details:
            supplier = Supplier.objects.get(id=selected_detail.SupplierId)
            OrderItem.objects.create(
                NameOfSupplier=supplier.name,
                NameOfDetail=selected_detail.name,
                OrderId=order.id,
                SupplierId=supplier.id,
                DetailId=selected_detail.id
            )

    suppliers = list(Supplier.objects.all().order_by('name'))
    details = list(Detail.objects.all().order_by('name'))
    discounts = list(Discount.objects.all().order_by('min_quantity'))

    return render(request, 'main/request.html', {'suppliers': suppliers, 'details': details, 'discounts': discounts})


def userTime(request):
    # Получаем текущую дату и время в UTC
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)

    # Предположим, что тайм зона пользователя хранится в настройках пользователя
    # Здесь для примера используем тайм зону 'Europe/Moscow'
    user_timezone = pytz.timezone('Europe/Moscow')
    user_time = utc_now.astimezone(user_timezone)

    # Получаем данные из базы данных
    data = Time.objects.all().values('name', 'created_at', 'updated_at')

    # Преобразуем даты для тайм зоны пользователя и для UTC
    data_list = []
    for item in data:
        created_at_utc = item['created_at']
        updated_at_utc = item['updated_at']
        item['created_at_user'] = created_at_utc.astimezone(user_timezone).strftime('%d/%m/%Y')
        item['created_at_utc'] = created_at_utc.strftime('%d/%m/%Y')
        item['updated_at_user'] = updated_at_utc.astimezone(user_timezone).strftime('%d/%m/%Y')
        item['updated_at_utc'] = updated_at_utc.strftime('%d/%m/%Y')
        data_list.append(item)

    # Генерация календаря на текущий месяц для тайм зоны пользователя
    cal = calendar.HTMLCalendar(calendar.SUNDAY)
    calendar_html = cal.formatmonth(user_time.year, user_time.month)

    # Формируем контекст для передачи в шаблон
    context = {
        'user_timezone': user_timezone,
        'user_time': user_time.strftime('%d/%m/%Y %H:%M:%S'),
        'utc_time': utc_now.strftime('%d/%m/%Y %H:%M:%S'),
        'data_list': data_list,
        'calendar_html': calendar_html,
    }

    return render(request, 'main/time.html', context)


def get_weather_data(lat, lon, api_key):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def index2(request):
    let = 53.893009
    lon = 27.567444
    api_key = '866a6fbfa627aefa1cdbbcbfcb2e3e90'
    data = get_weather_data(let, lon, api_key)
    data1 = get_cat_fact()
    context = {
        'data': data,
        'data1': data1
    }

    return render(request, 'main/usermain.html', context)


    

def news2(request):
    logger.debug("Rendering news2 page")
    new = News.objects.all()
    return render(request, 'main/usernews.html', {'new': new})

def faq(request):
    logger.debug("Rendering faq page")
    Qanswer = FAQ.objects.all()
    return render(request, 'main/faq.html', {'Qanswer': Qanswer})

def faq2(request):
    logger.debug("Rendering faq2 page")
    Qanswer = FAQ.objects.all()
    return render(request, 'main/userfaq.html', {'Qanswer': Qanswer})
