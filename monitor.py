import time,math
from pythonping import ping
from multiprocessing import Process
import matplotlib.pyplot as plt
import statistics as stat
def makeTicks(duration,delay,value):
    return [1 for _ in range(int(duration/delay))]

def monitorUp(site,delay):
    response = 1
    while True:
        response = ping(site,count=1)
        print(response.responses)
        print(vars(response))
        time.sleep(delay)
    return
def monitorDown(site,delay):
    print(ping(site,count=1))

def plot(ticks):
    x = range(len(ticks))
    y = ticks
    plt.plot(x,y, label="Up Time")
    plt.legend()
    plt.show()

def monitor(site,delay=1, limit=math.inf):
    start = time.time()
    upTime = 0.0
    downTime = 0.0
    totalDuration = 0
    ticks=[]
    up = Process(target=monitorUp, args=(site,delay))
    down = Process(target=monitorDown, args=(site,delay))
    i=0
    try:
        while i < limit:
            i+=1
            up.start()
            up.join()
            duration = time.time()
            upTime += duration
            start -= duration
            ticks+=makeTicks(duration,delay,1)
            print(f"Server is down. Uptime was {upTime}")
            down.start()
            down.join()
            downTime += duration
            duration = time.time()
            start -= duration
            ticks+=makeTicks(duration,delay,0)
            print(f"Server is up. Downtime was {downTimeTime}")
    except KeyboardInterrupt:
        print("Exit caught")
        #up.terminate()
        #down.terminate()
        
        
if __name__=="__main__":
    monitor('iotabet.pw',delay=.5)
