from fabric.api import local
def push_to_github():
    local("git push -u origin master")

def hello():
    print 'hello, This is test!'
