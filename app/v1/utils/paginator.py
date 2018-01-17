""" Paginator function for category and recipe modules. """

def get_paginated_results(request, results, url):
    """ Returns previous and next pagination links. """
    if request.values.get('start'):
        start = int(request.values.get('start'))
    else:
        start = 1
    if request.values.get('limit'):
        limit = int(request.values.get('limit'))
    else:
        limit = 20
    count = len(results)
    paginated = {}
    if count < start:
        paginated['previous_link'] = ''
        paginated['next_link'] = ''
    else:
        if start == 1:
            paginated['previous_link'] = ''
        else:
            previous_start = max(1, start - limit)
            previous_limit = start - 1
            paginated['previous_link'] = url + '?start=%d&limit=%d' % \
                    (previous_start, previous_limit)
        if start + limit > count:
            paginated['next_link'] = ''
        else:
            next_start = start + limit
            paginated['next_link'] = url + '?start=%d&limit=%d' % (next_start, limit)
    paginated['results'] = results[(start - 1):(start - 1 + limit)]
    return paginated
