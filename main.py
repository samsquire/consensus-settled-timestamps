from multiprocessing import Process, Queue
import time
from datetime import datetime, timedelta
import random
import operator
thismoment = datetime.now()
servers = [

]
servercount = 10
for i in range(0, servercount):
  servdata = {
    "name": "server{}".format(len(servers)),
    "value": [],
    
  }
  timestamp = {}
  servdata["timestamp"] = timestamp
  for n in range(servercount):
    timestamp[n] = thismoment
  servers.append(servdata)


class Server(Process):
  def __init__(self, identifier, servers, queue, mainthread):
    super(Server, self).__init__()
    self.identifier = identifier
    self.running = True
    self.servers = servers
    self.queue = queue
    self.otherqueues = []
    self.mainthread = mainthread

  def latest(self, me):
    value = 0
    self.servers[self.identifier]["value"].sort(key=operator.itemgetter("timestamp"), reverse=False)
    for item in self.servers[self.identifier]["value"]:
      if me is None:
        me = self.servers[self.identifier]["timestamp"][self.identifier]
      if item["timestamp"] <= me and self.servers[self.identifier]["timestamp"][item["origin"]] >= item["timestamp"]:
        
        value = item["value"]
        
    return value

  def consistentread(self):
    timestamps = []
    for server in self.servers:
      for timestamp in server["timestamp"].values():
        timestamps.append(timestamp)
    
    
    
    return min(timestamps)
      
  
  def run(self):
    stopping = False
    stoppings = 0
    sent_stopping = False
    while self.running:
      
      try:
        # print("trying to read")
        for i in range(0, 10000):
          item = self.queue.get_nowait()
          
          # print("received from", item[0], item[1])
          if item is not None:
            if item[0] == "ask":
              
              mainthread.put(("update", self.latest(self.consistentread())))
            if item[0] == "stop":
              
              stopping = True
              
              stoppings = stoppings + 1      

              #print("asked to stop")
              
              # print("asked to stop")
            if item[0] == "receivedstopping":
              stoppings = stoppings + 1
              #print(stoppings)
              if stoppings >= len(self.otherqueues) - 1:
                print("finished")
                self.running = False
                break
              
              # print(stoppings)
              # print("someone finished")
              
              
              
            if item[0] == "timestamp":
              self.servers[self.identifier]["timestamp"][item[1]] = item[2]
              
              self.servers[item[1]]["timestamp"] = item[3]
            elif item[0] == "update":
              self.servers[self.identifier]["value"].append(item[2])
      except:
        if stopping:
                        self.mainthread.put(("receivedstopping",self.identifier))
      
      me = datetime.now()  
      snapshot = me + timedelta(milliseconds=50)
      nextvalue = self.latest(self.consistentread()) + random.randint(1, 15)
      
      self.servers[self.identifier]["timestamp"][self.identifier] = me
      for server in range(len(self.servers)):
        if server != self.identifier:
          self.otherqueues[server].put(("timestamp", self.identifier, me, self.servers[self.identifier]["timestamp"]))
          # print("wrote to {}".format(server))
        
        

      
      
            #print("sent received")
                 
      
      
      if not stopping:
      
      
        
        for server in range(len(self.servers)):
          if server == self.identifier:
            self.servers[self.identifier]["value"].append({
              "origin": self.identifier,
              "timestamp": snapshot,
              "key": "{}{}".format(snapshot.strftime('%s'), self.identifier), 
              "value":
              nextvalue
            })
          else:
            self.otherqueues[server].put(("update", self.identifier, {
              "origin": self.identifier,
              "timestamp": snapshot,
              "key": "{}{}".format(snapshot.strftime('%s'), self.identifier),
              "value":
              nextvalue
            }))
    
    #print("sending to mainthread")
    self.mainthread.put(("update", self.latest(self.consistentread())))
    print("ending")
    

threads = []
queues = []
mainthread = Queue()
for r in range(len(servers)):
  queues.append(Queue())
for r in range(len(servers)):
  server = Server(r, servers, queues[r], mainthread)
  threads.append(server)

for thread in range(len(threads)):
  threads[thread].threads = threads
  threads[thread].otherqueues = queues

for thread in threads:
  thread.start()


time.sleep(10)
for queue in queues:
  queue.put(("ask", datetime.now()))
print("asked")
received = []
for thread in threads:
  serverdata = mainthread.get()
  if serverdata[0] == "receivedstopping":
    for queue in range(len(queues)):
      if queue != serverdata[1]:
          queues[queue].put(("receivedstopping",))
  if serverdata[0] == "update":
    received.append(serverdata[1])

for item in received:
  print(item)
print("sleeping")
time.sleep(3)

for queue in queues:
  queue.put(("stop",))
time.sleep(1)  
print("Stopping")

print("Joined")
from pprint import pprint
# pprint(servers)
received = []

while len(received) < len(servers):
  try:
      serverdata = mainthread.get_nowait()
      # print(serverdata)
      if serverdata[0] == "receivedstopping":
        for queue in range(len(queues)):
          if queue != serverdata[1]:
              queues[queue].put(("receivedstopping",))
      if serverdata[0] == "update":
        
        received.append(serverdata[1])
  except:
    pass
print("finished queue")
for item in received:
  print(item)
