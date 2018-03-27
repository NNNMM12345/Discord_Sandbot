def get_api_token(file_name):
    try:
        token_file = open(file_name, 'r')
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print ('Failed to load {}\n{}'.format(file_name, exc))
    return token_file.readline()
