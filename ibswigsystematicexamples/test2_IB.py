from wrapper_v2 import IBWrapper, IBclient
from swigibpy import Contract as IBcontract
 
if __name__=="__main__":

    """
    This simple example returns historical data 
    """

    callback = IBWrapper()
    client=IBclient(callback, port=4002, clientid=999)
    
    ibcontract = IBcontract()
    ibcontract.secType = "FUT"
    ibcontract.expiry="201612"
    ibcontract.symbol="ES"
    ibcontract.exchange="GLOBEX"

    ans=client.get_IB_historical_data(ibcontract, durationStr="2 D", barSizeSetting="5 mins")
    print ans
     
