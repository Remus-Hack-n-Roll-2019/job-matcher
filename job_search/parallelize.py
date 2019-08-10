

# TODO: Parallelize the requests
def parallelize_requests(f, requests):
    results = []
    for request in requests:
        results.append(f(request))
    return results
