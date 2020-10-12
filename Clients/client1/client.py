import sys
import os
sys.path.append('./src')

from country import CountryManager
from country.ttypes import *

from currency import CurrencyManager
from currency.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift import Thrift
from flask import Flask
app = Flask(__name__)

countryHostname = "country" if (os.environ.get("COUNTRY_HOSTNAME") is None) else os.environ.get("COUNTRY_HOSTNAME")
currencyHostname = "currency" if (os.environ.get("CURRENCY_HOSTNAME") is None) else os.environ.get("CURRENCY_HOSTNAME")

# def country_service():
#     try:
#         transport = TSocket.TSocket(countryHostname, 9080)
#         transport = TTransport.TBufferedTransport(transport)
#         protocol = TBinaryProtocol.TBinaryProtocol(transport)
#         client = CountryManager.Client(protocol)
#         transport.open()

#         country = client.get_country('USA')
#         info = "{}:\n\tCapital is {}\n\tCurrency is {}".format(country.name,
#                                                                 country.capital,
#                                                                 country.currency)
#     except Thrift.TException as tx:
#         info = tx.message
#     finally:
#         transport.close()
#         return info

def currency_service():
    try:
        transport = TSocket.TSocket(currencyHostname, 9080)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = CurrencyManager.Client(protocol)
        transport.open()

        val = str(client.convert("RUB", "USD", 100))

    except Thrift.TException as tx:
        val = tx.message
    finally:
        transport.close()
        return val

def do_thrift_connection():
    # retval_country = country_service()
    retval_cuurency = currency_service()
    retval = "{}\n{}".format(retval_cuurency)
    return retval


@app.route('/hello_world')
def hello_world():
    info = do_thrift_connection()
    return info


if __name__ == '__main__':
    app.run('0.0.0.0', port=9080)

