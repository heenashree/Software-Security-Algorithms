from collections import deque, defaultdict
def process_requests(
    requests: list[dict],
    permissions: dict[str, set[str]],
    max_requests: int = 100,
    window_seconds: int = 60,
) -> list[str]:
    '''
    requests [{
    request_id:"req_1"
    client_id = "client_1"
    endppoint = s"/transactions/get"
    timestamp  = int # increasing
    }]
    permissions: Mapping of client_id -> set of allowed endpoints.
    permissions = {client_id : set("endpiint_1", endpint_2")
    if client_id does not permissions or enpiints dont ecist in clinet if request is not allowed

    :param requests:
    :param permissions:
    :return:list of denied request_ids (list[str]).
    Do NOT add its timestamp to that client's sliding-window deque.
    '''
    res = []
    client_mapping = defaultdict(deque)
    for single_request in requests:
        client_id = single_request["client_id"]
        endpoint = single_request["endpoint"]
        request_id = single_request["request_id"]
        timestamp = single_request["timestamp"]
        if client_id not in permissions or endpoint not in permissions[client_id]:
            res.append(request_id)
            continue

        if client_id in client_mapping:
            all_val = client_mapping[client_id]
            while all_val and all_val[0] <=timestamp - window_seconds: # the first index will always keep on being compared as we are popping
                all_val.popleft()
        if len(client_mapping[client_id]) >= max_requests: # we just need atmost so its fine that we check lenght after we checked timestamps
            res.append(request_id)
            continue
        client_mapping[client_id].append(timestamp)
    return res
perms = {
    "client_a": {"/accounts/get", "/transactions/get"},
    "client_b": {"/accounts/get"},
}

reqs_m2 = [
    {"request_id": "r1", "client_id": "client_a", "endpoint": "/accounts/get", "timestamp": 10},      # Allowed (window:)
    {"request_id": "r2", "client_id": "client_a", "endpoint": "/auth/get", "timestamp": 11},          # Denied (perm) - does not enter window
    {"request_id": "r3", "client_id": "client_a", "endpoint": "/transactions/get", "timestamp": 12},  # Allowed (window:)
    {"request_id": "r4", "client_id": "client_a", "endpoint": "/accounts/get", "timestamp": 15},      # Denied (rate limit: 2 in [6..15])
    {"request_id": "r5", "client_id": "client_a", "endpoint": "/accounts/get", "timestamp": 20},      # Allowed (10 expired; window:)
    {"request_id": "r6", "client_id": "client_b", "endpoint": "/accounts/get", "timestamp": 20},      # Allowed (separate client_b window:)
]

assert process_requests(reqs_m2, perms, max_requests=2, window_seconds=10) == ["r2", "r4"]
print("Milestone 2 passed!")


