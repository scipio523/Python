from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import ibConnection, message
from time import sleep, strftime, localtime
from datetime import datetime

## Global variables
shares = 3
action = 'BUY' 
orderID = 30
last = 0
prev_last = 0
sym = 'YM'

## Contract Creation Function
def makeStkContract(sym):
    contract = Contract()
    contract.m_symbol = 'YM'
    contract.m_secType = 'FUT'
    contract.m_expiry = '20130315'
    contract.m_exchange = 'ECBOT'
    contract.m_currency = 'USD'
    return contract

## Order Creation Function
def makeStkOrder(shares,action):
    order = Order()
    order.m_minQty = shares
#    order.m_lmtPrice = limit_price
    order.m_orderType = 'MKT'
    order.m_totalQuantity = shares
    order.m_action = str(action).upper()
    return order

## Tick Handler
def my_tick_handler(msg):
    global last
    global prev_last
    #print msg
    if msg.field == 4:
        prev_last = last
        last = float(msg.price)
    print msg

##Connect
con = ibConnection()
con.register(my_tick_handler, message.TickSize, message.TickPrice)
con.connect()

## Make your contract
stkContract = makeStkContract(sym)
## Request tick data
con.reqMktData(orderID, stkContract, '', False)
sleep(1)
print last

## Prints last price as long as between 13070 and 13100
while (last > 13070 and last < 13100):
    print last

#### A possible execution plan. Remove '##' to initiate.
#### A paper trading account is recommended for testing and debugging trade execution code.
##    if (last > 13083):
##        action = 'BUY'
##        stkOrder = makeStkOrder(shares,action)
##        con.placeOrder(orderID,stkContract,stkOrder)
##    elif (last < 13082):
##        action = 'SELL'
##        stkOrder = makeStkOrder(shares,action)
##        con.placeOrder(orderID,stkContract,stkOrder)
    sleep(.5)

##Stop receiving tick values
con.cancelMktData(orderID)

##Disconnect from TWS
con.disconnect()