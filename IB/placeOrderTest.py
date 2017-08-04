from ib.opt import Connection, message
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from time import sleep, strftime

def make_contract(symbol, sec_type, exch, prim_exch, curr):
    contract = Contract()
    contract.m_symbol = symbol
    contract.m_secType = sec_type
    contract.m_exchange = exch
    contract.m_primaryExch = prim_exch
    contract.m_currency = curr
    return contract

def make_order(action, quantity, price=None):
    order = Order()
    if price is not None:
        order.m_orderType = 'LMT'
        order.m_totalQuantity = quantity
        order.m_action = action
        order.m_lmtPrice = price
    else:
        order.m_orderType = 'MKT'
        order.m_totalQuantity = quantity
        order.m_action = action
    return order

def error_handler(msg):
    print "Server Error: %s" % msg

def reply_handler(msg):
    print "Server Response: %s, %s" % (msg.typeName, msg)

def order_id_handler(msg):
    global oid
    oid = msg.orderId
    print 'Next Valid ID is ' + str(oid)

con = Connection.create(port=7497, clientId=999)
con.registerAll(reply_handler)
con.register(order_id_handler, 'NextValidId')
con.connect()

contract = make_contract('TSLA', 'STK', 'SMART', 'SMART', 'USD')
order = make_order('BUY', 1, 190)
con.reqIds(0)
#con.placeOrder(oid, contract, order)

con.disconnect()