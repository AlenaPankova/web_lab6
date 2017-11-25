from pyramid.config import Configurator
from pyramid.response import Response
from wsgiref.simple_server import make_server
from webob import Request, Response
from jinja2 import Environment, FileSystemLoader

assets = [
  'app.js',
  'react.js',
  'leaflet.js',
  'D3.js',
  'moment.js',
  'math.js',
  'main.css',
  'bootstrap.css',
  'normalize.css',
  ]

links = []
scripts = []

for item in assets:
  str = item.split('.')
  if str[1] == 'css':
    links.append(item)
  elif str[1] == 'js':
    scripts.append(item)

class WsgiTopBottomMiddleware(object):
  def __init__(self, app):
    self.app = app

  def __call__(self, environ, start_response):
    response = self.app(environ, start_response).decode()
    if response.find('<head>'and'<body>') > -1:
      head1, head = response.split('<head>')
      datahead, endhead = head.split('</head>')
      head2, body = endhead.split('<body>')
      databody, endbody = body.split('</body>')
   
      yield (head1 + data + endbody).encode() 
    else:
      yield (response).encode()

def index(request):
  env = Environment(loader=FileSystemLoader('.'))
  template = env.get_template('/index.html')
  return Response(template.render(javascripts=scripts, styles=links))

def about(request):
  env = Environment(loader=FileSystemLoader('.'))
  template = env.get_template('/about/aboutme.html')
  return Response(template.render(javascripts=scripts, styles=links))

if __name__ == '__main__':
  config = Configurator() 
  config.add_route('index', '/')
  config.add_view(index, route_name='index')
  config.add_route('about', '/about')
  config.add_view(about, route_name='about')
  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 8000, app)
  server.serve_forever()
  

