from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.internet import reactor,endpoints
import cgi

class User:
    def __init__(self, name, acc_no, balance):
        self.name = name
        self.acc_no = acc_no
        self.balance = balance
    
    def withdraw(self,amount) :
        self.balance = self.balance - amount
        return self.balance
    
    def deposit(self,amount) :
        self.balance = self.balance + amount
        return self.balance

new_user = User('Sahil', 101010, 1000)


class Check(Resource):
    def render_POST(self, request):
        return (b"<!DOCTYPE html><html><head><meta charset='utf-8'>"
                b"<title></title></head><body>"
                b"Your Balance: " + str(new_user.balance).encode('utf-8'))


class Deposit(Resource):
    def render_GET(self, request):
        return (b"<!DOCTYPE html><html><head><meta charset='utf-8'>"
                b"<title></title></head><body>"
                b"<form method='POST'>Enter Amount: <input name='the-field'></form>")

    def render_POST(self, request):
        args = request.args[b"the-field"][0].decode("utf-8")
        escapedArgs = int(cgi.escape(args))
        ub = str(new_user.deposit(escapedArgs))
        return (b"<!DOCTYPE html><html><head><meta charset='utf-8'>"
                b"<title></title></head><body>"
                b"Updated Balance: " + ub.encode('utf-8'))


class Withdraw(Resource):
    def render_GET(self, request):
        return (b"<!DOCTYPE html><html><head><meta charset='utf-8'>"
                b"<title></title></head><body>"
                b"<form method='POST'>Enter Amount: <input name='the-field'></form>")

    def render_POST(self, request):
        args = request.args[b"the-field"][0].decode("utf-8")
        escapedArgs = int(cgi.escape(args))
        ub = str(new_user.withdraw(escapedArgs))
        return (b"<!DOCTYPE html><html><head><meta charset='utf-8'>"
                b"<title></title></head><body>"
                b"Updated Balance: " + ub.encode('utf-8'))

    
class Close(Resource):
        def render_DELETE(self,request):
            #del new_user
            return (b"<!DOCTYPE html><html><head><smeta charset='utf-8'>"
                    b"<title></title></head><body>"
                    b"Account Closed ")


root = Resource()
root.putChild(b"check", Check())
root.putChild(b"deposit", Deposit())
root.putChild(b"withdraw", Withdraw())
root.putChild(b"close", Close())
factory = Site(root)
endpoint = endpoints.TCP4ServerEndpoint(reactor, 8880)
endpoint.listen(factory)
reactor.run()
