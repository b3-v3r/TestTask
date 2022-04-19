from pydantic import BaseModel, constr


class PaymentParams( BaseModel ):
    amount : float
    currency : str
    desc : str


class BillRequest( BaseModel ):
    description : str
    payer_currency : int 
    shop_currency : int 
    shop_id : int
    shop_amount : float 
    shop_order_id : constr(max_length=255)
    sign : str


class InvoceRequest( BaseModel ):
    amount : float
    currency: str
    description : str
    shop_id : int 
    shop_order_id : constr(max_length=255)
    sign : str
    payway : str