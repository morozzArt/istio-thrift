import sys
sys.path.append('./gen-py')

from country import CountryManager
from country.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift import Thrift

country_list = [
    Country('Russia', 0, 'RUB', 'Moscow'),
    Country('Germany', 1, 'EUR', 'Berlin'),
    Country('USA', 2, 'USD', 'Washington'),
]

class CountyManagerHandler:
    def __init__(self):
        pass
        #self.log = {}

    def get_country(self, name):
        for country in country_list:
            if country.name == name:
                return country
        raise Thrift.TApplicationException(
                Thrift.TApplicationException.INVALID_MESSAGE_TYPE,
                "Unknown country"
              )

handler = CountyManagerHandler()
processor = CountryManager.Processor(handler)

transport = TSocket.TServerSocket(host='0.0.0.0', port=9080)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

print ('Starting the server...')
server.serve()
print('done.')