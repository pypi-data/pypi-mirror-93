import json
import time
import redis

from rosetta_dispatcher import idtool
from rosetta_dispatcher.model.dispatch_request_model import DispatchRequestModel
from rosetta_dispatcher.model.dispatch_response_model import DispatchResponseModel


class DispatchServer:
    def __init__(self, redis_host: str, redis_port: int):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.pool = redis.ConnectionPool(host=redis_host, port=redis_port, decode_responses=True)

    def preprocess_request(self, strrequest: str):
        if strrequest:
            dict_request = json.loads(strrequest)
            request = DispatchRequestModel.parse_obj(dict_request)
            if request.correlation_id:
                start_time = idtool.get_timestamp(request.correlation_id)
                ts_now = time.time()
                if ts_now < start_time + request.timeout:
                    return request

        return None

    def __fetch_one__(self, r: redis.Redis, service_queue: str):

        return

    def fetch(self, service_queue: str, batch_count=16, timeout: int = 0):
        result = []

        r = redis.Redis(connection_pool=self.pool)

        # block and wait data.
        trequest = r.brpop(keys=service_queue, timeout=timeout)
        # None data fetched.
        if not trequest:
            return result

        request = self.preprocess_request(trequest[1])
        if request:
            result.append(request)

        # non block get request until batch_count or no request in queue.
        while len(result) < batch_count:
            strrequest = r.rpop(service_queue)
            if not strrequest:
                break
            request = self.preprocess_request(strrequest)
            if request:
                result.append(request)

        return result

    def send_response(self, response_queue: str, response: DispatchResponseModel):
        r = redis.Redis(connection_pool=self.pool)
        data = response.dict(exclude_none=True)
        r.lpush(response_queue, json.dumps(data, ensure_ascii=True))
        r.expire(response_queue, time=10)
