import gc
import os

import psutil

from hkube_python_wrapper.communication.zmq.streaming.ZMQListener import ZMQListener
from hkube_python_wrapper.util.encoding import Encoding
from hkube_python_wrapper.util.DaemonThread import DaemonThread
import time


class MessageListener(DaemonThread):

    def __init__(self, options, receiverNode, errorHandler=None):
        self.errorHandler = errorHandler
        remoteAddress = options['remoteAddress']
        encodingType = options['encoding']
        self._encoding = Encoding(encodingType)
        self.adapater = ZMQListener(remoteAddress, self.onMessage, self._encoding, receiverNode)
        self.messageOriginNodeName = options['messageOriginNodeName']

        self.messageListeners = []
        DaemonThread.__init__(self, "MessageListener-" + str(self.messageOriginNodeName))

    def registerMessageListener(self, listener):
        self.messageListeners.append(listener)

    def onMessage(self, messageFlowPattern, header, msg):
        start = time.time()
        decodedMsg = self._encoding.decode(header=header, value=msg)
        for listener in self.messageListeners:
            try:
                listener(messageFlowPattern, decodedMsg, self.messageOriginNodeName)
            except Exception as e:
                print('Error during MessageListener onMessage' + str(e))

        end = time.time()
        duration = int((end - start) * 1000)
        return self._encoding.encode({'duration': duration}, plainEncode=True)

    def run(self):
        print("Start receiving from " + self.messageOriginNodeName)
        try:
            self.adapater.start()
        except Exception as e:
            if (self.errorHandler):
                self.errorHandler.sendError(e)

    def close(self):
        self.adapater.close()
        self.messageListeners = []
counter = [0]
if __name__ == '__main__':

    def onMessage(a,b,c):
        counter[0] +=1
    listenr_config = {'remoteAddress': 'tcp://localhost:9536', 'encoding': 'msgpack', 'messageOriginNodeName': 'b'}
    for i in range(0,100):
        mListener =  MessageListener(listenr_config,receiverNode='a')
        mListener.registerMessageListener(onMessage)
        mListener.start()
        time.sleep(6)
        print('counter: ' + str(counter[0]))
        gc.collect()
        process = psutil.Process(os.getpid())
        print('before closeing lisner ****************************' + str(process.memory_info().rss))
        mListener.close()
        process = psutil.Process(os.getpid())
        print('after closeing lisner ****************************' + str(process.memory_info().rss))
