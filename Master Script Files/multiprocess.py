import multiprocessing

cores = 0

cores = multiprocessing.cpu_count()

print('number of cores is: %s' % cores)
