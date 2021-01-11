import time

def date(n):
    year = time.strftime("%Y-%m-", time.localtime())
    day = int(time.strftime("%d", time.localtime()))+n

    print(year+str(day))


date(1)