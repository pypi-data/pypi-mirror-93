import time
import sys
import threading
import subprocess
import zmq

addr = "tcp://127.0.0.1:5678"

# class Messaging(threading.Thread):

def ping():
    print("connecting zmq")
    context = zmq.Context()
    sock = context.socket(zmq.PAIR)
    sock.bind(addr)

    time.sleep(1)

    i = 0
    while True:
        #print("PING %s", i)
        try:
            sock.send_unicode("Agent create {} 100 100 0 5 ARROW (255,0,0)".format(i), zmq.NOBLOCK)
        except zmq.Again:
            pass
            
        #print("Receiving")
        try:
            req = sock.recv_unicode(zmq.NOBLOCK)
            print(req)
        except zmq.Again:
            pass
        
        i+=1

        time.sleep(0.5)

# ping()

class Launcher(threading.Thread):
    def __init__(self):
        self.stdout = None
        self.stderr = None
        self._is_running = False
        threading.Thread.__init__(self)

    def run(self):
        self.p = subprocess.Popen([sys.executable, "ui.py"],
                                  shell=False,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)

        self._is_running = True
        self.stdout, self.stderr = self.p.communicate()
        self.terminate()

    def terminate(self):
        self.p.terminate()
        self._is_running = False

launcher = None
        
def ensure_ui_process():
    global launcher
    if launcher is None:
        launcher = Launcher()
        launcher.start()

def kill_ui_process():
    global launcher
    launcher.terminate()
    launcher.join()
    launcher = None

# ensure_ui_process()

ping()


# kill_ui_process()
    
# print("sleeping 2 sec")
# time.sleep(2)
# ping()
# print("sleeping 2 sec")
# time.sleep(2)


# print(launcher.stdout)
