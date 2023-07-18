import random
import json
import sys,os

global stock_data

with open('stocks.json') as f:
    global stock_data
    data = f.read()
    stock_data = json.loads(data)


def random_price(mmin=3,mmax=1000):
    price = random.randint(mmin,mmax)
    price *= random.random()
    price = round(price,2)
    if price < 10:
        price = '000' + str(price)
    elif price < 100:
        price = '00' + str(price)
    elif price < 1000:
        price = '0' + str(price)

    if len(price) < 7:
        price = price + '0'
    return price

def generate_stock():
    global stock_data
    random.shuffle(stock_data)
    return {'stock':stock_data[0],'price':random_price()}

def random_id(digits=4):
    uid = ""
    for i in range(digits):
        uid += str(random.randint(0,9))
    return uid

def is_json_str(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True

def is_json_obj(myjson):
  try:
    json_str = json.dumps(myjson)
  except ValueError as e:
    return False
  return True
  

def mykwargs(argv):
    '''
    Processes argv list into plain args and kwargs.
    Just easier than using a library like argparse for small things.
    Example:
        python file.py arg1 arg2 arg3=val1 arg4=val2 -arg5 -arg6 --arg7
        Would create:
            args[arg1, arg2, -arg5, -arg6, --arg7]
            kargs{arg3 : val1, arg4 : val2}
        
        Params with dashes (flags) can now be processed seperately
    Shortfalls: 
        spaces between k=v would result in bad params
    Returns:
        tuple  (args,kargs)
    '''
    args = []
    kargs = {}

    for arg in argv:
        if '=' in arg:
            key,val = arg.split('=')
            kargs[key] = val
        else:
            args.append(arg)
    return args,kargs


if __name__=='__main__':
    print(generate_stock())
    print(random_id())
