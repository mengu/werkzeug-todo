from werkzeug import Response
from jinja2 import Environment, FileSystemLoader
import os

jinja_env = Environment(loader=FileSystemLoader('/home/mengu/projects/todo/templates'))

def print_css_files():
    css_dir = "/home/mengu/projects/todo/static/css"
    html = []
    for css_file in os.listdir(css_dir):
        html.append('<link rel="stylesheet" type="text/css" href="/static/css/%s" />' % (css_file))
    return "\n\t".join(html)

jinja_env.globals["print_css_files"] = print_css_files

def render_response(template_name, **context):
    tmpl = jinja_env.get_template(template_name)
    return Response(tmpl.render(context), mimetype='text/html')

