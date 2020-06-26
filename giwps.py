import argparse
import itertools
import concurrent.futures
from math import factorial, log
import multiprocessing
from pandas import DataFrame
import timeit


class WilsonPrimeSearch:
    def __init__(self, search_floor, search_ceiling):
        self.search_floor = search_floor
        self.search_ceiling = search_ceiling

    def erat2(self):
        D = {}
        yield 2
        for q in itertools.islice(itertools.count(3), 0, None, 2):
            p = D.pop(q, None)
            if p is None:
                D[q*q] = q
                yield q
            else:
                x = p + q
                while x in D or not (x&1):
                    x += p
                D[x] = p

    def get_primes_erat(self, n):
        return list(itertools.takewhile(lambda p: p<n, self.erat2()))

    def wilson_prime_remainder(self, x):
        return x, (factorial(x-1)+1) % (x**2)

    def run_search(self):
        print('search zone: {:.2e} -> {:.2e}'.format(self.search_floor, self.search_ceiling))
        print('conjectured estimate # of Wilson Primes: {}'.format(self.conjectured_num_wp))
        print('searching in parallel on {} cores'.format(multiprocessing.cpu_count()))
        print('\n')
        print('primes  |  remainders')

        df = DataFrame()

        with concurrent.futures.ProcessPoolExecutor() as executor:
            search_zone = self.get_primes_erat(self.search_ceiling)
            search_zone = [x for x in search_zone if x > self.search_floor]
            results = executor.map(self.wilson_prime_remainder, search_zone)

            for result in results:
                df = df.append([result])
                print(result)
        
        df = df.rename(columns={0: 'primes', 1: 'remainders'})
        df.to_csv('/usr/src/data/test_output1.csv', index=False)
    

    @property
    def conjectured_num_wp(self):
        return log(log(self.search_ceiling)/log(self.search_floor))

parser = argparse.ArgumentParser(description='search for wilson primes within a given search zone')
parser.add_argument('-floor', type=int, help='start of search zone')
parser.add_argument('-ceiling', type=int, help='end of search zone')
args = parser.parse_args()

def main(search_floor, search_ceiling):
    start = timeit.default_timer()

    wps = WilsonPrimeSearch(search_floor, search_ceiling+1)
    wps.run_search()

    stop = timeit.default_timer()

    print(f'search runtime: {stop-start}')

if __name__ == '__main__':
    main(args.floor, args.ceiling)
    