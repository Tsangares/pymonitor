import time,math
from pythonping import ping
from multiprocessing import Process
import matplotlib.pyplot as plt
import statistics as stat
def isConnected(response):
    return 'Request timed out' not in str(response._responses[0])
def makeTicks(duration,delay,value):
    if duration > 10**5:
        raise Exception("Duration error.",duration)
    return [value for _ in range(int(duration/delay))]

def monitorUp(site,delay,silent=False):
    print("Starting monitor up")
    response = 1
    totalTime = time.time()
    while True:
        start = time.time()
        response = ping(site,count=1,timeout=delay)
        if not isConnected(response): break
        duration = time.time() - start
        if not silent:
            print(f"Connected. Response in {duration:.2f} sec; upTime {time.time() - totalTime:.1f} sec")
        if duration < delay:
            time.sleep(delay - duration)
    return
def monitorDown(site,delay,silent=False):
    print("Starting monitor down")
    response = 1
    totalTime = time.time()
    while True:
        response = ping(site,count=1,timeout=delay)
        if isConnected(response): break
        if not silent:
            print(f"Disconnected. Total down time {time.time() - totalTime:.1f} sec")
    return

def plotTicks(ticks):
    x = range(len(ticks))
    y = ticks
    plt.plot(x,y, label="Up Time")
    plt.legend()
    plt.show()

def monitor(site,delay=1, limit=math.inf,silent=False, plot=False):
    print("Starting Monitor")
    start = time.time()
    upTime = 0.0
    downTime = 0.0
    duration=totalDuration = 0
    ticks=[]
    up=down=None
    i=0
    try:
        response = ping(site,count=1,timeout=delay)
        connected = isConnected(response)
        while i < limit:
            i+=1
            up = Process(target=monitorUp, args=(site,delay,silent))
            if connected:
                up.start()
                up.join()
                duration = time.time() - start
                upTime += duration
                start -= duration
                print("start time:", start)
                ticks+=makeTicks(duration,delay,1)
                print(f"Server is down. Uptime was {duration:.1f} secconds")
            connected = False
            down = Process(target=monitorDown, args=(site,delay,silent))
            if not connected:
                down.start()
                down.join()
                duration = time.time() - start
                downTime += duration
                start -= duration
                ticks+=makeTicks(duration,delay,0)
            connected = True            
            print(f"Server is up. Downtime was {duration:.1f} secconds")
    except KeyboardInterrupt:
        print("Exit caught")
        if up is not None:
            up.terminate()
        if down is not None:
            down.terminate()
        if plot:
            duration = time.time() - start
            ticks+=makeTicks(duration,delay,0)
            plotTicks(ticks)
    except PermissionError:
        print("Please run as sudo.")
        quit(1)
        
        
if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Monitor some IP.')
    parser.add_argument('ip', type=str, help='The ip you want to monitor.')
    parser.add_argument('--delay', type=float, help='Delay between pings.',default=1)
    parser.add_argument('--silent', action='store_true', help='Stop most the output text.',default=False)
    parser.add_argument('--plot', action='store_true', help='Plot when you hit ctrl-c.',default=False)
    args = parser.parse_args()
    monitor(args.ip,delay=args.delay,silent=args.silent,plot=args.plot)
