'''
Rate Limiter: Based on a given ID and a given time window
allow_request(key, timestamp) is called  - allow max_requests for that key inside rolling window of winow_dseoncds else return False
'''

from collections import defaultdict, deque
class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.data = defaultdict(deque)

        if max_requests < 0 or window_seconds <0:
            raise ValueError("Negative Values")
        self.window_seconds = window_seconds
        self.max_requests = max_requests



    def allow_request(self, key: str, timestamp: int) -> bool:
        if timestamp < 0:
            return False
        q = self.data[key] # benifit of deque that if key doenst exist, it will create a new one
        # compare the last item in deque with incoming timestamp. For example [10] > 2 so we need to reject that one
        if q and q[-1] > timestamp:
            return False
        # 2. Evict expired timestamps (half-open window: [t - window, t))
        while q and timestamp - q[0] >= self.window_seconds:
            q.popleft()
        # finally
        if len(q) < self.max_requests:
            q.append(timestamp)
            return True
        return False

def test_rate_limiter():
    rl = RateLimiter(max_requests=2, window_seconds=10)
    assert rl.allow_request("user1", 10) is True
    assert rl.allow_request("user1", 4) is False
    assert rl.allow_request("user1", 24) is True
    assert rl.allow_request("user1", 25) is True
    assert rl.allow_request("user1", -3) is False
    assert rl.allow_request("user1", 12) is False
    print("All test cases done")

test_rate_limiter()




