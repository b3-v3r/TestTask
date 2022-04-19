# -*- coding: utf-8 -*-
import logging
from flask import Flask, redirect, render_template, request 
import random

import requests
from .models_db import Payment

from .utils import sign_params
from .config import CurrencyCodes, SHOP_ID
from .models import BillRequest, InvoceRequest, PaymentParams

import uuid
import pydantic 

from .models_db import session
from loguru import logger


app = Flask( __name__ )

@app.route("/", methods=["GET"])
def index():
    payments = session.query(Payment).all()
    
    if payments is None:
        payments = []

    return render_template("index.html", payments=payments)


@app.route("/payment", methods=["POST"])
def payment():

    try:
        body = PaymentParams( **request.form )
    except pydantic.ValidationError:
        return "<h1>Неверные параметры, проверьте введенные данные!</h1>"


    amount = round( body.amount, 2 )

    currency = body.currency
    desc = body.desc

    order_id = str(random.randint(0, 100))

    payment = Payment( id=order_id, amount=amount, currency=currency, desciption=desc )
    session.add(payment)
    session.commit()


    logger.info( "Amount {}, currency {}, desc {} , order_id {}".format(amount, currency, desc, order_id) )

    if currency == "eur":

        sign = sign_params(
            amount=amount, 
            currency=CurrencyCodes.EUR, 
            shop_id=SHOP_ID,
            shop_order_id= order_id )

        return render_template("payment_pay.html", 
            amount   = amount, 
            currency = CurrencyCodes.EUR, 
            shop_id  = SHOP_ID,
            desc     = desc, 
            sign     = sign,
            order_id = order_id
        )

    elif currency == "usd":

        sign = sign_params( 
            payer_currency = CurrencyCodes.USD,
            shop_amount = amount,
            shop_currency = CurrencyCodes.USD,
            shop_id = SHOP_ID,
            shop_order_id = order_id 
        )

        bill_params = BillRequest(
            description=desc, 
            payer_currency=CurrencyCodes.USD,
            shop_currency=CurrencyCodes.USD,
            shop_amount=amount,
            shop_order_id = order_id,
            shop_id=SHOP_ID,
            sign=sign
        )
       
        bill_request = requests.post("https://core.piastrix.com/bill/create", 
            data=bill_params.json(),
            headers={
                "Content-type": 'application/json'
            }
        )
        
        result = bill_request.json()

        if not result["result"]:
            logging.error( result["message"] )
            return result["message"]
        
        return redirect( result["data"]["url"] )

    elif currency == "rub":

        sign = sign_params(
            amount = amount,
            currency = CurrencyCodes.RUB,
            shop_id = SHOP_ID,
            payway = "advcash_rub",
            shop_order_id = order_id
        )

        invoce_params = InvoceRequest(
            amount=amount,
            currency=CurrencyCodes.RUB,
            shop_id=SHOP_ID,
            description=desc, 
            shop_order_id = order_id,
            payway = "advcash_rub",
            sign=sign
        )

        invoce_request = requests.post("https://core.piastrix.com/invoice/create", 
            data=invoce_params.json(),
            headers={
                "Content-type": 'application/json'
            }
        )
        
        result = invoce_request.json()

        if not result["result"] :
            logging.error( result["message"] )
            return result["message"]
        
        # Всегда падает ошибка(Payway (alias = advcash_rub) is not available for shop), 
        # Возможно больше advcash_rub не поддерживаеться данным api или у тестовому айди магазана(5) закрыли доступ к этой функции

        return ""
        
