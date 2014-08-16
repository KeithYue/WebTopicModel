# coding=utf-8
# generate the topic picture
from jinja2 import Template, FileSystemLoader, Environment
from db_helper import connect_db

def make_demo(data):
    '''
    given one topic data, generate the topic chart
    '''
    t_loader = FileSystemLoader(searchpath= './')
    env = Environment(loader = t_loader)
    t = env.get_template('simple.html')
    with open('./demo.html', 'w') as output:
        output.write(t.render(d=data))
    return

def test():
    db = connect_db()
    data = db['topics'].find_one()
    data = data['words']
    data = sorted(data, key = lambda x: x['contribution'], reverse = True)
    make_demo(data)
    return

if __name__ == '__main__':
    test()
