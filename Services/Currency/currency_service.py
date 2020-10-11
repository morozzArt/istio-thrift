import sys

sys.path.append('./gen-py')

from currency import CurrencyManager
from currency.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

coefficients = {
	"RUB": {"USD": 0.0128, "EUR": 0.0109},
	"USD": {"RUB": 78.0915, "EUR": 0.8527},
	"EUR": {"RUB": 91.5779, "USD": 1.1727}
}

class CurrencyManagerHandler:
	def __init__(self):
		pass
		#self.log = {}

	def convert(self, dest, src, value):
		if value < 0:
			raise Thrift.TApplicationException(TApplicationException.INVALID_MESSAGE_TYPE, "Value is less than zero")
		if src not in coefficients or dest not in coefficients[src]:
			raise Thrift.TApplicationException(TApplicationException.INVALID_MESSAGE_TYPE, "Unknown currency")
		return value * coefficients[src][dest]

handler = CurrencyManagerHandler()
processor = CurrencyManager.Processor(handler)
transport = TSocket.TServerSocket(port=9080)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)


print ('Starting the server...')
server.serve()
print ('done.')