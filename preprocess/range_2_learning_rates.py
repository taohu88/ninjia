def range_2_learning_rates(init, start, stop=None, step=1, decay=0.618):
    if stop is None:
        stop = start
        start = 0

    r = []
    for i in range(start, stop, step):
        r.append('{:9.7f}*{}'.format(init, step))
        init = init * decay
    return ':'.join(r)


print(range_2_learning_rates(0.2/256, 124, step=10))
