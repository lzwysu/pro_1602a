import Queue

class Player():
    def __init__(self):
        self.msg_q = Queue.Queue()

    def getMsg(self):
        msgs = []
        for i in range(self.msg_q.qsize()):
            msg = self.msg_q.get()
            msgs.append(msg)
        return msgs