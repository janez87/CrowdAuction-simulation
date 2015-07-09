class Bid():
  """docstring for Bid"""
  def __init__(self, worker,task,amount):
    self.worker = worker 
    self.task = task 
    self.amount = amount 
    task.receiveBid(self)

  def __repr__(self):
    return "worker: "+self.worker.name+" bid: "+ str(self.amount)
    