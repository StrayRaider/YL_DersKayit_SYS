import time

activeTime = 0

def clockT(seconds,parent):
    global activeTime
    start = time.time()
    while activeTime < seconds:
        activeTime = int(time.time() - start)
        print(" seconds count: {}".format(activeTime)) 
        parent.activeTime = activeTime
        time.sleep(1)  
    parent.isEnded = True
    #ended

#stopwatch(20)
