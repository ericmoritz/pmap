from threading import Thread
from Queue import Queue, Empty
import sys

def pmap_thread_target(result_queue, function, index, value):
    try:
        result = function(value)
        result_queue.put((index, result))
    except Exception, e:
        # send the error to the result queue so that
        # the main thread will know an error occurred
        result_queue.put(("error", sys.exc_info()))
        # Reraise for exception reporting
        raise

def pmap(function, sequence):
    results = []
    
    result_queue = Queue()
    size = 0
    result_counter = 0
    
    for index, value in enumerate(sequence):
        size += 1
        results.append(None)
        t = Thread(target=pmap_thread_target, args=(result_queue,
                                                    function,
                                                    index, value))
        t.start()
        
    # Collect results
    while result_counter < size:
        index, result = result_queue.get()

        # If an error occurred in a thread, crash the main thread
        if index == "error":
            raise result[1], None, result[2]

        results[index] = result
        result_counter += 1

    return results
