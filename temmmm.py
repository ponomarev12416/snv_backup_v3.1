def f(n):
    if n == 3 or n == 7:
        raise Exception('FAILED: ', n)
    print('n ===== ', n)

for i in range(10):
    try:
        f(i)
    except Exception as e:
        print(e.args)
        print('fixed')
    print('After except i = ', i)