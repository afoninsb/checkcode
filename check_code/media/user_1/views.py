import contextlib
import json
from datetime import datetime, timedelta

import redis
from core.admin_data import get_admin_data
from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from tarifs.models import Payment as Payment_db
from yookassa import Configuration, Payment
from yookassa.domain.notification import WebhookNotification

from bots.models import Bot
from bots.tgbot.bot_class import BotTG


def index(request):
    """Тарифы ботов пользователя."""
    tgid = get_admin_data(request)
    if not tgid:
        return HttpResponseForbidden()
    bots = (
        Bot.objects.filter(admin__tgid=tgid).select_related('tarif')
        .prefetch_related('payments')
    )
    return render(request, 'tarifs/index.html', {'bots': bots, })


def pay(request, chat_id, pay_id, confirmation_token):
    r = redis.from_url(
        f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.PAY_REDIS_DB}',
        encoding='utf-8',
        decode_responses=True
    )
    data = r.get(f'{chat_id}:{pay_id}')
    data = json.loads(data)
    payment_db = Payment_db(
        user_id=chat_id,
        bot_id=data['botid'],
        tarif_id=data['tarif_id'],
        amount=data['price'],
        pay_id=pay_id,
        pay_status='created',
        payd=False,
        description=data['description'],
    )
    with contextlib.suppress(IntegrityError):
        payment_db.save()
    context = {
        'confirmation_token': confirmation_token,
        'pay_id': pay_id
    }
    return render(request, 'tarifs/pay.html', context)


def pay_status(request, pay_id):
    Configuration.account_id = settings.SHOP_ID
    Configuration.secret_key = settings.SHOP_SECRET_KEY
    payment = Payment.find_one(pay_id)
    text = 'Ваш платёж '
    text = f'{text} зачислен.' if payment.paid else f'{text} не завершён.'
    return render(request, 'tarifs/pay_status.html', {'text': text})


@csrf_exempt
def getstatus(request):
    bot = BotTG(settings.MAIN_BOT_TOKEN)
    event_json = json.loads(request.body)
    try:
        payment = WebhookNotification(event_json)
    except Exception:
        return HttpResponse(status=400)
    payment_db = get_object_or_404(Payment_db, pay_id=payment.object.id)
    if int(payment_db.amount) != int(payment.object.amount.value):
        message = {
            'chat_id': payment_db.user.tgid,
            'text': (
                'Сумма оплаты по платежу "{payment_db.description}" не '
                'совпадает с ценой тарифа. Свяжитесь с техподдержкой в '
                'админ.боте!'
            )
        }
        bot.send_message(message)
        return HttpResponse(status=400)
    payment_db.pay_status = payment.object.status
    payment_db.payd = payment.object.paid
    text = (
        f'Статус вашего платежа "{payment_db.description}" изменён.\n'
        f'Новый статус - {payment.object.status}'
    )
    if payment.object.status == 'succeeded':
        payment_db.payment_method = payment.object.payment_method.type
        cur_bot = payment_db.bot
        end_time = cur_bot.end_time or datetime.now()
        end_time += timedelta(days=payment_db.tarif.duration*31)
        cur_bot.tarif = payment_db.tarif
        cur_bot.end_time = end_time
        cur_bot.is_paid = True
        text = f'{text}\nТариф бота "{payment_db.bot}" продлён до {end_time}.'
    try:
        payment_db.save()
        cur_bot.save()
    except Exception:
        return HttpResponse(status=400)
    message = {
        'chat_id': payment_db.user.tgid,
        'text': text,
    }
    bot.send_message(message)
    return HttpResponse(status=200)
