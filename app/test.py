print('Hello World')
print('Hello World')
print('Hello World')


import time

count = 600

def print_cont(i):
    while i:
        i -= 1
        print(i)
        time.sleep(1)



print_cont(count)
