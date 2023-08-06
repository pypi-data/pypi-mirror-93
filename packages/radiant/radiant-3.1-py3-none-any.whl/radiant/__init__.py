"""
Radiant

"""
# Prevent this file to be imported from Brython
import sys
try:
    import browser
    sys.exit()
except:
    pass

import os
import json
import jinja2
import pathlib
import importlib.util
from xml.etree import ElementTree
from typing import Union, List, Tuple

from tornado.web import Application, url, RequestHandler, StaticFileHandler
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer

RadiantAPI = object
DEBUG = True
PATH = Union[str, pathlib.Path]
URL = str


########################################################################
class PythonHandler(RequestHandler):
    def post(self):
        name = self.get_argument('name')
        args = tuple(json.loads(self.get_argument('args')))
        kwargs = json.loads(self.get_argument('kwargs'))

        if v := getattr(self, name, None)(*args, **kwargs):
            if v is None:
                data = json.dumps({'__RDNT__': 0, })
            else:
                data = json.dumps({'__RDNT__': v, })
        self.write(data)

    # ----------------------------------------------------------------------
    def test(self):
        """"""
        return True


########################################################################
class ThemeHandler(RequestHandler):

    # ----------------------------------------------------------------------
    def get(self):
        theme = self.get_theme()
        loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates'))
        env = jinja2.Environment(autoescape=True, loader=loader)
        env.filters['vector'] = self.hex2vector
        stylesheet = env.get_template('theme.css.template')
        self.write(stylesheet.render(**theme))

    # ----------------------------------------------------------------------
    @staticmethod
    def hex2vector(hex_: str):
        return ', '.join([str(int(hex_[i:i + 2], 16)) for i in range(1, 6, 2)])

    # ----------------------------------------------------------------------
    def get_theme(self):
        theme = self.settings['theme']

        if (not theme) or (not os.path.exists(theme)):
            theme = os.path.join(os.path.dirname(__file__), 'templates', 'default_theme.xml')

        tree = ElementTree.parse(theme)
        theme_css = {child.attrib['name']: child.text for child in tree.getroot()}
        return theme_css


########################################################################
class RadiantHandler(RequestHandler):

    def initialize(self, **kwargs):
        self.initial_arguments = kwargs

    def get(self):
        variables = self.settings.copy()
        variables.update(self.initial_arguments)

        variables['argv'] = json.dumps(variables['argv'])
        self.render(f"{os.path.realpath(variables['template'])}", **variables)


# ----------------------------------------------------------------------
def make_app(class_: str, /,
             template: PATH = os.path.join(os.path.dirname(__file__), 'templates', 'index.html'),
             environ: dict = {},
             mock_imports: Tuple[str] = [],
             handlers: Tuple[URL, Union[List[Union[PATH, str]], RequestHandler], dict] = (),
             python: Tuple[PATH, str] = (),
             theme: PATH = None,
             path: PATH = None,
             autoreload: bool = False):
    """
    Parameters
    ----------
    class_ :
        The main class name as string.
    template :
        Path for HTML file with the template.
    environ :
        Dictionary with arguments accessible from the template and main class.
    mock_imports :
        List with modules that exist in Python but not in Brython, this prevents
        imports exceptions.
    handlers :
        Custom handlers for server.
    python :
        Real Python scripting handler.
    theme :
        Path for the XML file with theme colors.
    path :
        Custom directory accesible from Brython PATH.
    autoreload :
        Activate the `autoreload` Tornado feature.
    """

    settings = {
        "debug": DEBUG,
        'static_path': os.path.join(os.path.dirname(__file__), 'brython'),
        'static_url_prefix': '/static/',
        "xsrf_cookies": False,
        'autoreload': autoreload,
    }

    environ.update({
        'class_': class_,
        'python_': python if python else (None, None),
        'module': os.path.split(sys.path[0])[-1],
        'file': os.path.split(sys.argv[0])[-1].removesuffix('.py'),
        'theme': theme,
        'argv': sys.argv,
        'template': template,
        'mock_imports': mock_imports,
        'path': path,
    })

    app = [
        url(r'^/$', RadiantHandler, environ),
        url(r'^/theme.css$', ThemeHandler),
        url(r'^/root/(.*)', StaticFileHandler, {'path': sys.path[0]}),
    ]

    if python:
        spec = importlib.util.spec_from_file_location('.'.join(python).replace('.py', ''), os.path.abspath(python[0]))
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        app.append(url(r'^/python_handler', getattr(foo, python[1])))

    for handler in handlers:
        if isinstance(handler[1], tuple):
            spec = importlib.util.spec_from_file_location('.'.join(handler[1]).replace('.py', ''), os.path.abspath(handler[1][0]))
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            app.append(url(handler[0], getattr(foo, handler[1][1]), handler[2]))
        else:
            app.append(url(*handler))

    if path:
        app.append(url(r'^/path/(.*)', StaticFileHandler, {'path': path}),)

    settings.update(environ)

    return Application(app, **settings)


# ----------------------------------------------------------------------
def RadiantServer(class_: str, /,
                  host: str = 'localhost',
                  port: str = '5000',
                  template: PATH = os.path.join(os.path.dirname(__file__), 'templates', 'index.html'),
                  environ: dict = {},
                  mock_imports: Tuple[str] = [],
                  handlers: Tuple[URL, Union[List[Union[PATH, str]], RequestHandler], dict] = (),
                  python: Tuple[PATH, str] = (),
                  theme: PATH = None,
                  path: PATH = None,
                  autoreload: bool = False):
    """Python implementation for move `class_` into a Bython environment.

    Configure the Tornado server and the Brython environment for run the
    `class_` in both frameworks at the same time.

    Parameters
    ----------
    class_ :
        The main class name as string.
    host :
        The host for server.
    port :
        The port for server.
    template :
        Path for HTML file with the template.
    environ :
        Dictionary with arguments accessible from the template and main class.
    mock_imports :
        List with modules that exist in Python but not in Brython, this prevents
        imports exceptions.
    handlers :
        Custom handlers for server.
    python :
        Real Python scripting handler.
    theme :
        Path for the XML file with theme colors.
    path :
        Custom directory accesible from Brython PATH.
    autoreload :
        Activate the `autoreload` Tornado feature.

    """

    print("Radiant server running on port {}".format(port))
    application = make_app(class_, python=python, template=template,
                           handlers=handlers, theme=theme, environ=environ,
                           mock_imports=mock_imports, path=path)
    http_server = HTTPServer(application)
    http_server.listen(port, host)
    IOLoop.instance().start()


