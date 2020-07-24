from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

class bankUser:
    def __init__(self, name, acc_no, balance):
        self.name = name
        self.acc_no = acc_no
        self.balance = balance
    
    def withdraw(self,amount) :
        self.balance = self.balance - amount
    
    def deposit(self,amount) :
        self.balance = self.balance + amount

new_user = bankUser('Sahil', 101010, 1000)

def check_balance(request):
        return Response(str(new_user.acc_no) + " account of " + new_user.name + " has balance " + str(new_user.balance))   

    
def withdraw_amount(request):
         new_user.withdraw(100) 
         return Response("Updated Balance " + str(new_user.balance))


def deposit_amount(request):
        new_user.deposit(100) 
        return Response("Updated Balance " + str(new_user.balance))


def close_account(request):
        return Response("Account " + str(new_user.acc_no)+ " closed")
        #del new_user
        
if __name__== '__main__':
    with Configurator() as config:
        config.add_route('checkBalance','/')
        config.add_route('withdraw','/withdraw')
        config.add_route('deposit','/deposit')
        config.add_route('closeAcc','/close')
        config.add_view(check_balance,route_name='checkBalance',request_method='GET')
        config.add_view(withdraw_amount,route_name='withdraw',request_method='POST')
        config.add_view(deposit_amount,route_name='deposit',request_method='POST')
        config.add_view(close_account,route_name='closeAcc',request_method='DELETE')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 4000, app)
    server.serve_forever()