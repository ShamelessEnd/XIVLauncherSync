import datetime

def print_with_timestamp(s):
    now = datetime.datetime.now()
    print(f'{str(now)}: {s}')
