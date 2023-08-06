from time import sleep

from rosetta_dispatcher.dispatch_server import DispatchServer
from rosetta_dispatcher.model.dispatch_response_model import DispatchResponseModel
from rosetta_dispatcher.model.dispatch_types import DispatchResponseStatus

host = '61.160.36.168'
port = 4032

ds = DispatchServer(redis_host=host, redis_port=port )

count = 0
while True:
    result = ds.fetch('test_rpc', batch_count=16)
    print(f'fetched: {len(result)}')
    for request in result:
        response = DispatchResponseModel(correlation_id=request.correlation_id, status=DispatchResponseStatus.OK,
                                         data=request.data)
        ds.send_response(request.reply_to, response)


