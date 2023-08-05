def format_filter(name, value):
    '''
    Convert a filter name and value into boto3 filter format
    
    :param name: filter name to search on
    :param value: filter value to search on
    :return: The formated filter dict

    Example::

        format_filter('vpc-id', 'vpc-0dbb013f82b6694e9')
        
        {
            'Name': 'vpc-id',
            'Values': [
                'vpc-0dbb013f82b6694e9'
            ]
        }
    '''
    return {'Name': name, 'Values': [value]}


def format_filters(filters: dict):
    '''
    Convert a dictionary of filters into boto3 filter format

    :param filters: A dictionary of filters
    :return: The formatted filter dict

    Example::
    
        format_filters({
            'vpc-id', 'vpc-0dbb013f82b6694e9',
            'default', 'true'
        })

        [
            {
                'Name': 'vpc-id',
                'Values': [
                    'vpc-0dbb013f82b6694e9'
                ]
            },
            {
                'Name': 'default',
                'Values': [
                    'true'
                ]
            }
        ]
    '''
    return [ format_filter(key, value) for key, value in filters.items() ]