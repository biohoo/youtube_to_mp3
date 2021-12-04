
from concurrent import futures

'''
Only exits the entire block when all 
pending futures are completed
'''
def results_as_we_go(func, iterable):
    with futures.ThreadPoolExecutor() as executor:
        jobs = [executor.submit(func, x) for x in iterable]
        '''These jobs (futures) are submitted to 
        the as_completed function and iterated through as 
        they complete.
        '''
        for comp_job in futures.as_completed(jobs):
            print(comp_job.result())
