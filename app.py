import deca

from deca import request

def get(): pass

def get_start():
    return 'Start page'
    
def get_page():
    print(request.get)
    return {'user': 'John Botan'}
    
def get_info():
    pass

    
def get_test(): pass

def post_test():
    print(request.post)
    
    
def plain_function():
    yield 3
    
if __name__ == '__main__':
    deca.run()