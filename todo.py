from actions import index, signup, signin, signout, new_todo, view_todo, edit_todo, delete_todo
from werkzeug import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, MethodNotAllowed
from werkzeug.contrib.sessions import FilesystemSessionStore

url_map = Map([
    Rule('/', endpoint=index),
    Rule('/signup', endpoint=signup),
    Rule('/signin', endpoint=signin),
    Rule('/signout', endpoint=signout),
    Rule('/todo/new', endpoint=new_todo),
    Rule('/todo/<int:todoid>', endpoint=view_todo),
    Rule('/todo/<int:todoid>/edit', endpoint=edit_todo),
    Rule('/todo/<int:todoid>/delete', endpoint=delete_todo)
])

session_store = FilesystemSessionStore()

@Request.application
def application(request):
    adapter = url_map.bind_to_environ(request.environ)
    try:
        endpoint, values = adapter.match()
        if not callable(endpoint):
            raise MethodNotAllowed()
        sid = request.cookies.get('todosid')
        if sid is None:
            request.session = session_store.new()
        else:
            request.session = session_store.get(sid)
        response = endpoint(request, **values)
        if request.session.should_save:
            session_store.save(request.session)
            response.set_cookie('todosid', request.session.sid)
        return response
    except HTTPException, e:
        return e

if __name__ == "__main__":
	from werkzeug import run_simple
	run_simple('localhost', 4000, application)

