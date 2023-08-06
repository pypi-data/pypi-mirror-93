from rosetta_dispatcher.dispatch_client import DispatchClient

host = '61.160.36.168'
port = 4032

dc = DispatchClient(redis_host=host, redis_port=port)

count = 0
while True:
    result = dc.process(service_queue='test_rpc', data=str(count), timeout=1)
    print(result)
    count+=1