import uuid

MAGICS = {
    'priority': (int, 0, int, None),
    'tags': (list, [], set, None),
    'untags': (list, [], set, None),
    'variables': (dict, {}, dict, None),
    'global': (dict, {}, dict, None),
    'services': (dict, {}, dict, None),
}

SERVICE_MAGICS = {
    'plugin_id': (str, '', str, None),
    'tags': (list, [], set, None),
    'variables': (dict, {}, dict, None),
}

INTERNALS = {
    '__uuid__': lambda d: uuid.uuid4(),
}


def parse_template(d: dict = {}, magics: dict = {}, internals: dict = {}) -> dict:
    """
    Ensure incoming dict 
    """
    magics_ = magics if magics else MAGICS

    for mkey, value in magics_.items():

        type_, default_, converterf_, allowed_ = value

        value_from_template = d.get(mkey)

        if mkey == 'plugin_id':
            print(value_from_template)

        if value_from_template and not isinstance(value_from_template, type_):
            raise ValueError

        current_ = value_from_template or default_

        if not isinstance(current_, converterf_):                    
            current_ = converterf_(current_)

        if allowed_ and current_ not in allowed_:
            raise ValueError

        d[mkey] = current_

    internals_ = internals if internals else INTERNALS

    for mkey, func in internals_.items():
        d[mkey] = func(d)

    return d
        


        
    


    
