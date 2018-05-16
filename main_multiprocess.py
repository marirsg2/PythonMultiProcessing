
from multiprocessing import Process
import os


main_storage = ["a","b","c"]

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(name):
    info('function f')
    print('hello', name)
    main_storage[0] = "d"
    print(main_storage)#will not change original copy, as Process() does sys.fork()

if __name__ == '__main__':
    info('main line')
    p = Process(target=f, args=('bob',))
    p.start()
    print(main_storage)
    p.join()
    print(main_storage)