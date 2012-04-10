from threading import Thread
from Queue import Queue, Empty


def pmap_thread_target(result_queue, function, index, value):
    try:
        result = function(value)
        result_queue.put((index, result))
    except Exception, e:
        result_queue.put(("error", e))
    

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

        if index == "error":
            raise result

        results[index] = result
        result_counter += 1

    return results
