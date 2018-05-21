# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, InvalidPage

#import paypal

from zonetable.apps.directory.models import Package, Pay
from zonetable.apps.home.models import Country
from zonetable.apps.functions.forms import WhoisForm
from zonetable.apps.functions.views import PointByScore, getUserCountry


@login_required(login_url='/')
def list_payments_view(request, page):
    try:
        country_id = request.COOKIES['gm_country']
        state_id = request.COOKIES['gm_state']
        language_id = request.COOKIES['gm_language']
    except:
        #remote_addr = request.META.get('HTTP_X_FORWARDED_FOR', "127.0.0.1")
        remote_addr = request.META['REMOTE_ADDR']
        country_id = getUserCountry(remote_addr)

    state_id = 1
    language_id = 1


    today = datetime.now()
    today = today.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    max_age = 90 * 24 * 60 * 60 # 3 meses (90 días)

    ###############################

    if request.user.is_authenticated():
        user = User.objects.get(pk=request.user.id)

        points = PointByScore(request)

        list_payments = Pay.objects.filter(user=user).order_by('-id_pay')

        # paginar los resultados a '10' por pagina
        paginator = Paginator(list_payments, 10)
        try:
            num_page = int(page)
        except:
            num_page = 1
        try:
            list_payments = paginator.page(num_page)
        except (EmptyPage, InvalidPage):
            list_payments = paginator.page(paginator.num_pages)

    pais_actual = Country.objects.all().get(id_country=country_id)

    # enviamos el ID del pais de la cookie
    formulario_whois = WhoisForm(initial={'Country': country_id})

    ctx = {
        'points': points,
        'list_payments': list_payments,
        'pais_actual': pais_actual,
        'formulario_whois': formulario_whois,
    }
    response = render_to_response('accounts/payments/payment_list.html', ctx, context_instance=RequestContext(request))
    return response


@csrf_exempt
def ok_payments_view(request):
    try:
        country_id = request.COOKIES['gm_country']
        state_id = request.COOKIES['gm_state']
        language_id = request.COOKIES['gm_language']
    except:
        #remote_addr = request.META.get('HTTP_X_FORWARDED_FOR', "127.0.0.1")
        remote_addr = request.META['REMOTE_ADDR']
        country_id = getUserCountry(remote_addr)

    state_id = 1
    language_id = 1


    today = datetime.now()
    today = today.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    max_age = 90 * 24 * 60 * 60 # 3 meses (90 días)

    ###############################

    error = msg = msg_title = pay = date_begin = date_end = ''

    txn_id = request.POST.get('txn_id')
    receiver_id = request.POST.get('receiver_id')
    invoice = request.POST.get('invoice')
    custom = request.POST.get('custom')

    error = pay_gm = False

    list_package = Package.objects.filter(status=True).order_by('order')
    total_package = Package.objects.all().aggregate(price=Sum('price'))

    points = PointByScore(request)

    if request.REQUEST.has_key('txn_id'):
        try:
            pay = Pay.objects.get(txn_id=1)
            error = True
            msg = 'Error: La transacción es Duplicada. Por favor, <a href="/contacto/">contáctenos</a>.'
            msg_title = ': Error'

        except Pay.DoesNotExist:
            try:
                pay = Pay.objects.get(pk=invoice)

                pay.txn_id = txn_id
                pay.receiver_id = receiver_id
                pay.pay_status = 3
                pay.save()
                msg = 'Tu pago se ha recibido satisfactoriamente.'
                msg_title = ': Aceptado'
                pay_gm = True

                date_begin = datetime.date(pay.date_begin)
                date_end = datetime.date(pay.date_end)

            except Pay.DoesNotExist:
                error = True
                msg = 'Error: No se registró un pago. Por favor, <a href="/contacto/">contáctenos</a>.'
                msg_title = ': Error'
    else:
        error = True
        msg = 'Error: No se recibió una transacción. Por favor, <a href="/contacto/">contáctenos</a>.'
        msg_title = ': Error'

    '''
        if request.REQUEST.has_key('tx'):
          try:
            existing = models.Purchase.objects.get( tx=tx )
            return render_to_response('error.html', { 'error': "Duplicate transaction" }, context_instance=RequestContext(request) )
          except models.Purchase.DoesNotExist:
            result = paypal.Verify( tx )
            if result.success() and resource.price == result.amount(): # valid
              purchase = models.Purchase( resource=resource, purchaser=user, tx=tx )
              purchase.save()
              return render_to_response('purchased.html', { 'resource': resource }, context_instance=RequestContext(request) )
            else: # didn't validate
              return render_to_response('error.html', { 'error': "Failed to validate payment" }, context_instance=RequestContext(request) )
        else: # no tx
          return render_to_response('error.html', { 'error': "No transaction specified" }, context_instance=RequestContext(request) )
        '''

    pais_actual = Country.objects.all().get(id_country=country_id)

    # enviamos el ID del pais de la cookie
    formulario_whois = WhoisForm(initial={'Country': country_id})

    ctx = {
        'points': points,
        'msg_title': msg_title,
        'msg': msg,
        'error': error,
        'pay_gm': pay_gm,

        'custom': custom,
        'invoice': invoice,
        'txn_id': txn_id,
        'receiver_id': receiver_id,

        'pay': pay,
        'date_begin': date_begin,
        'date_end': date_end,
        'list_package': list_package,
        'total_package': total_package,

        'pais_actual': pais_actual,
        'formulario_whois': formulario_whois,
    }

    response = render_to_response('accounts/payments/payment_ok.html', ctx, context_instance=RequestContext(request))
    return response

# Pago Cancelado: Guardamos el status y redireccionamos
def cancel_payments_view(request, id_payment):
    try:
        pay = Pay.objects.get(pk=id_payment)

        pay.pay_status = 2
        pay.save()

    except Pay.DoesNotExist:
        error = True

    return HttpResponseRedirect('/accounts/payments/cancel/')

# Pago Cancelado: Mostramos la pagina de pago cancelado
def redirect_cancel_payments_view(request):
    try:
        country_id = request.COOKIES['gm_country']
        state_id = request.COOKIES['gm_state']
        language_id = request.COOKIES['gm_language']
    except:
        #remote_addr = request.META.get('HTTP_X_FORWARDED_FOR', "127.0.0.1")
        remote_addr = request.META['REMOTE_ADDR']
        country_id = getUserCountry(remote_addr)

    state_id = 1
    language_id = 1


    today = datetime.now()
    today = today.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    max_age = 90 * 24 * 60 * 60 # 3 meses (90 días)

    ###############################

    msg = 'Su transacción no se realizó con exito. Por favor, <a href="/contacto/">contáctenos</a>.'
    msg_title = ': Cancelado'

    pais_actual = Country.objects.all().get(id_country=country_id)

    points = PointByScore(request)

    # enviamos el ID del pais de la cookie
    formulario_whois = WhoisForm(initial={'Country': country_id})

    ctx = {
        'points': points,
        'msg_title': msg_title,
        'msg': msg,

        'pais_actual': pais_actual,
        'formulario_whois': formulario_whois,
    }

    response = render_to_response('accounts/payments/payment_cancel.html', ctx, context_instance=RequestContext(request))
    return response
