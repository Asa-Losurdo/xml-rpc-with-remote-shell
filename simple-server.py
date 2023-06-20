from twisted.internet import reactor
from xmlrpc.client import Fault
from twisted.internet import defer
from twisted.web import xmlrpc
from time import sleep
import inspect
def my_delayed_stop(delay_seconds=1):
    sleep(delay_seconds)
    reactor.stop()

class my_rpc(xmlrpc.XMLRPC):
    lines = []
    def xmlrpc_shell_fetch_lines(self):
        return my_rpc.lines
    
    def xmlrpc_shell_push_line(self,line):
        my_rpc.lines.append(line)
        return "ok"
    
    def xmlrpc_shell_set_lines(self,lines):
        my_rpc.lines = lines
        return "ok"

    def xmlrpc_help(self):
        prefix = "xmlrpc_"
        out = ""
        for method, p in inspect.getmembers(my_rpc, predicate=inspect.isfunction):
            if method.startswith(prefix) and not method.startswith(prefix+"shell"):
                out = out + f" - {method[len(prefix):]}{tuple(inspect.signature(p).parameters.keys())[1:]}\n"

        return out
    
    def xmlrpc_stop(self):
        print("xmlrpc: stop sig recived")
        reactor.callInThread(my_delayed_stop)
        return "ok"



from twisted.web import server
if __name__ == "__main__":
    reactor.listenTCP(7080, server.Site(my_rpc()))
    reactor.run()
