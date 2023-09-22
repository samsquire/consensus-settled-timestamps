from multiprocessing import Process, Queue
import time
from datetime import datetime, timedelta
import random
import operator
thismoment = datetime.now()
servers = [
  {
    "name": "server1",
    "value": [],
    "timestamp": {
      0: thismoment,
      1: thismoment,
      2: thismoment,
      3: thismoment,
      4: thismoment
    }
  },
  {
    "name": "server2",
    "value": [],
        "timestamp": {
      0: thismoment,
      1: thismoment,
      2: thismoment,
      3: thismoment,
      4: thismoment
    }
  },
    {
    "name": "server3",
      "value": [],
      "timestamp": {
      0: thismoment,
      1: thismoment,
      2: thismoment,
      3: thismoment,
      4: thismoment
    }
  },
  {
    "name": "server4",
    "value": [],
    "timestamp": {
      0: thismoment,
      1: thismoment,
      2: thismoment,
      3: thismoment,
      4: thismoment
    }
  }
]


class Server(Process):
  def __init__(self, identifier, servers, queue, mainthread):
    super(Server, self).__init__()
    self.identifier = identifier
    self.running = True
    self.servers = servers
    self.queue = queue
    self.otherqueues = []
    self.mainthread = mainthread

  def latest(self):
    value = 0
    self.servers[self.identifier]["value"].sort(key=operator.itemgetter("timestamp"), reverse=False)
    for item in self.servers[self.identifier]["value"]:
      if item["timestamp"] < datetime.now() and self.servers[self.identifier]["timestamp"][item["origin"]] >= item["timestamp"]:
        value = item["value"]
    return value
  
  def run(self):
    stopping = False
    stoppings = 0
    while self.running:
      
      try:
        # print("trying to read")
        for i in range(0, 100):
          item = self.queue.get_nowait()
          # print("received from", item[0], item[1])
          if item is not None:
            if item[0] == "stop":
              stopping = True
              
            if item[0] == "receivedstopping":
              stoppings = stoppings + 1
              if stoppings == len(self.otherqueues) - 1:
                self.running = False
                break
              
            if item[0] == "timestamp":
              self.servers[self.identifier]["timestamp"][item[1]] = item[2]
            elif item[0] == "update":
              self.servers[self.identifier]["value"].append(item[2])
      except:
        pass
      me = datetime.now()
      for server in range(len(self.servers)):
        if server != self.identifier:
          self.otherqueues[server].put(("timestamp", self.identifier, me))
          # print("wrote to {}".format(server))
        else:
          self.servers[server]["timestamp"][self.identifier] = me
      snapshot = datetime.now() + timedelta(milliseconds=50)
      nextvalue = self.latest() + random.randint(0, 15)
      if stopping:
        stoppings = stoppings + 1
        for queue in range(len(self.otherqueues)):
          if queue != self.identifier:
            self.otherqueues[queue].put(("receivedstopping",))
        
      if stopping:
        break
      for server in range(len(self.servers)):
        if server == self.identifier:
          self.servers[self.identifier]["value"].append({
            "origin": self.identifier,
            "timestamp": snapshot,
            "value":
            nextvalue
          })
        else:
          self.otherqueues[server].put(("update", self.identifier, {
            "origin": self.identifier,
            "timestamp": snapshot,
            "value":
            nextvalue
          }))
    self.mainthread.put(self.latest())

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
  queue.put(("stop",))
  
print("Stopping")
for thread in threads:
  thread.join()
print("Joined")
from pprint import pprint
# pprint(servers)
for thread in threads:
  serverdata = mainthread.get()
  print(serverdata)