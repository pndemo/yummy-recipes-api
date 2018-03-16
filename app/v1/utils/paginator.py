""" Paginator function for category and recipe modules. """

def get_paginated_results(request, results, url):
    """ Returns previous and next pagination links. """
    paginated = {}

    try:
        if request.values.get('page'):
            page = int(request.values.get('page'))
        else:
            page = 1
        if request.values.get('limit'):
            limit = int(request.values.get('limit'))
        else:
            limit = 6

        count = len(results)
        start = page * limit - limit + 1

        paginated['is_good_query'] = True

        if count < start:
            paginated['previous_link'] = ''
            paginated['next_link'] = ''
        else:
            if page == 1:
                paginated['previous_link'] = ''
            else:
                paginated['previous_link'] = url + 'page=%d&limit=%d' % (page - 1, limit)
            if start + limit > count:
                paginated['next_link'] = ''
            else:
                paginated['next_link'] = url + 'page=%d&limit=%d' % (page + 1, limit)
        paginated['results'] = results[(start - 1):(start - 1 + limit)]
    except ValueError:
        paginated['is_good_query'] = False
    return paginated
