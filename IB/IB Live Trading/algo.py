from wrapper import IBWrapper, IBclient
from swigibpy import Contract as IBcontract
 
if __name__=="__main__":

    # connect to demo account to get market data
    callback = IBWrapper()
    client=IBclient(callback, port=4002, clientid=999)
    
    # create a contract
    ibcontract = IBcontract()
    ibcontract.secType = "FUT"
    ibcontract.expiry="201612"
    ibcontract.symbol="ES"
    ibcontract.exchange="GLOBEX"
    ibcontract.currency="USD"

    # request market data
    ans=client.get_IB_market_data(ibcontract, seconds=1)
    print "Bid size, Ask size; Bid price; Ask price"
    print ans
