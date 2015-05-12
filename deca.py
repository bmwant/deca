from wsgiref.simple_server import make_server
import os
import inspect
import importlib
from pybars import Compiler
compiler = Compiler()

class Request:

    def __init__(self, raw_get_data='', raw_post_data='', method=''):
        self.method = method
        self.get = {'getparam1': 'val1'}
        self.post = {'postparam1': 'val1'}


class Deca:
    def __init__():
        pass
        
mappings = {}
request = Request()


def simple_app(environ, start_response):
    global request
    status = '200 OK'
    headers = []
    method = environ['REQUEST_METHOD'].lower()
    path = environ['PATH_INFO'].lower()[1:]  # without leading slash
    get_data = environ['QUERY_STRING']
    post_data = environ['QUERY_STRING']
    request = Request(get_data, post_data, method)
    key = (method, path)
    if key in mappings:
        func_res = mappings[key]()
        if type(func_res) is str:
            result = [func_res.encode('utf-8')]
            headers.append(('Content-type', 'text/plain'))
        elif type(func_res) is dict or func_res is None:
            if path == '':
                html_template = 'index'
            else:
                html_template = path
            with open('templates/{name}.html'.format(name=html_template)) as fin:
                source = fin.read()
            template = compiler.compile(source)
            result = template(func_res)
            headers.append(('Content-type', 'text/html'))
        else:
            print(type(func_res))
            headers.append(('Content-type', 'text/plain'))
            result = 'result'
        #result = [mappings[key]().encode('utf-8')]
    else:
        result = 'Not found'
        
    #headers.append(('Content-type', 'text/plain'))
    #ret = [('%s: %s\n' % (key, value)).encode('utf-8') for key, value in environ.items()]
    
    start_response(status, headers)
    #return ret
    return [bytes(result, 'utf-8')]

    
def parse_name(func_name):
    ALLOWED_METHODS = ('get', 'post')
    if '_' in func_name:
        method, path = func_name.split('_')
    else:
        method, path = func_name, ''
    
    if method not in ALLOWED_METHODS:
        return None
        #maybe this is just plain function in code don't touch it
        #raise SyntaxError('Invalid name of view function')
        
    return method, path
    
    
def print_all_func(module_name):
    just_name = os.path.splitext(module_name)[0]
    module = __import__(just_name)
    for member in inspect.getmembers(module):
        if inspect.isfunction(member[1]):
            #print(member[0])
            signature = parse_name(member[0])
            if signature is not None:
                mappings[signature] = member[1]
            
def run(host='127.0.0.1', port=8000):
    module_name = inspect.stack()[1][1]
    print_all_func(module_name)
    httpd = make_server(host, port, simple_app)
    print('Serving on port %s...' % port)
    httpd.serve_forever()