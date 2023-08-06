from serverhttp import *
app_resp = '''\
<?xml version="1.0">
<text>Hello World!</text>'''
demo_app = app.App('demo')
@demo_app.route('/', ['GET'])
def demo_app_hello(request):
    yield Response('200 OK', 'application/rss+xml', app_resp)

def run_demo_app(addr=("127.0.0.1", 60000)):
    try:
        serv = srv.AsyncHTTPServer(app=demo_app)
        print("Using AsyncHTTPServer")
    except:
        print("Using ThreadedHTTPServer")
        serv = srv.ThreadedHTTPServer(app=demo_app)
    serv.serve_forever(*addr)

