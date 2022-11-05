from dateutil import parser


def search_query(case, crit, field, s_date, e_date):
    match case:
        case '1a':
            output = {field: {'$regex': crit, '$options': 'i'}, 'Show Open': {'$lte': e_date, '$gte': s_date}}
        case '1b':
            output = {field: {'$regex': crit, '$options': 'i'},'Show Open': {'$gte': s_date}}
        case '1c':
            output = {field: {'$regex': crit, '$options': 'i'},'Show Open': {'$lte': e_date}}
        case '1d':
            output = {field: {'$regex': crit, '$options': 'i'}}
        case '2a':
            output = {'Show Open': {'$lte': e_date, '$gte': s_date}}
        case '2b':
            output = {'Show Open': {'$gte': s_date}}
        case '2c':
            output = {'Show Open': {'$lte': e_date}}
        case '2d':
            output = {}
    return output


def config_field(field):
    if field == 'Person':
        field = 'Cast_Crew.Person'

    if field == 'Genre':
        field = 'Production Type'

    if field == 'Company':
        field = 'Company.Name'

    if field == 'Date':
        field = 'Show Open'
    return field


def config_criteria(criteria):
    temp = None
    if criteria is None:
        output = 'No_Criteria'
    else:
        start = '^['
        end = ']'
        crit = criteria.split(',')

        for i in range(len(crit)):

            if i == 0:
                temp = crit[i] + '.*'
            else:
                temp = temp + '|' + crit[i] + '.*'

        output = start + temp + end
    return output


def config_sort(field):
    if field == 'Person':
        field = 'Cast_Crew.Person'

    if field == 'Genre':
        field = 'Production Type'

    if field == 'Company':
        field = 'Company.Name'

    if field == 'Date':
        field = 'Show Open'
    return field


def config_date(date):
    # Parses out the date for MongDB query
    if date is None:
        output = None
    else:
        output = parser.parse(date, fuzzy=True)
    return output


def db_find_results(db, field, criteria, sort, start_date, end_date):
    no_date = 'd'
    c_criteria = None
    c_field = None

    # Define Sort Order
    sort = config_sort(sort)

    # Find Date Case
    s1 = config_date(start_date)
    e1 = config_date(end_date)
    if (s1 is None) and (e1 is None):
        no_date = 'd'
    elif (s1 is not None) and (e1 is not None):
        no_date = 'a'
    elif (s1 is not None) and (e1 is None):
        no_date = 'b'
    elif (s1 is None) and (e1 is not None):
        no_date = 'c'

    # Find Criteria Case
    if criteria is None:
        c_case = 2
    else:
        c_case = 1
        c_criteria = config_criteria(criteria)
        c_field = config_field(field)

    # Assign Case and build query
    case = str(c_case) + no_date
    query = search_query(case, c_criteria, c_field, s1, e1)

    # Run the Search Query
    raw = [x for x in db.find(query).sort(sort)]
    return raw
