from threading import Thread
import time
from datetime import datetime, timedelta
import random
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


class Server(Thread):
  def __init__(self, identifier, servers):
    super(Server, self).__init__()
    self.identifier = identifier
    self.running = True
    self.servers = servers

  def latest(self):
    value = 0
    for item in self.servers[self.identifier]["value"]:
      if item["timestamp"] < datetime.now() and self.servers[self.identifier]["timestamp"][item["origin"]] >= item["timestamp"]:
        value = item["value"]
    return value
  
  def run(self):
    while self.running:
      for server in range(len(self.servers)):
        self.servers[server]["timestamp"][self.identifier] = datetime.now()
      snapshot = datetime.now() + timedelta(milliseconds=50)
      nextvalue = self.latest() + random.randint(0, 15)
      for server in range(len(self.servers)):
          
          self.servers[server]["value"].append({
            "origin": self.identifier,
            "timestamp": snapshot,
            "value":
            nextvalue
          })
    

threads = []
for r in range(len(servers)):
  server = Server(r, servers)
  threads.append(server)

for thread in threads:
  thread.threads = threads

for thread in threads:
  thread.start()


time.sleep(15)
for thread in threads:
  thread.running = False

from pprint import pprint
# pprint(servers)
for thread in threads:
  print(thread.latest())