from webob import Request, Response

from little_api.api import API
from little_api.middleware import Middleware

app = API()


# After request example
@app.after_request
def after_response(request, response):
    if response.json:
        response.json = {
            "data": response.json,
            "success": response.status_code // 100 == 2,
        }


# Function based handler examples
@app.route("/home/{name:w}", allowed_methods=["get"])
def home(request: Request, response: Response, name) -> None:
    response.text = f"Hello, {name}"


@app.route("/about")
def about(request: Request, response: Response) -> None:
    response.text = "Hello from the ABOUT page"


# Class based handler examples
@app.route("/book")
class BookResource:
    def get(self, req: Request, resp: Response):
        resp.text = "Get Books Page"

    def post(self, req: Request, resp: Response):
        resp.text = "Create Books Page"


# template example
@app.route("/template")
def template_render(req: Request, resp: Response):
    resp.body = app.template(
        "index.html", context={"name": "Little-Api", "title": "Best Framework"}
    )


# exception example


def custom_exception_handler(req: Request, resp: Response, exc_cls: Exception):
    resp.text = str(exc_cls)


app.add_exception_handler(AttributeError, custom_exception_handler)


@app.route("/exception")
def throw_exception(req: Request, resp: Response):
    raise AssertionError("This route should not be used")


# Non decorator example
def index(req: Request, resp: Response):
    resp.text = "This is the index page"


app.add_route("/", index)


# Adds example middleware
class SimpleCustomMiddleware(Middleware):
    def process_request(self, req):
        print("Processing request", req.url)

    def process_response(self, req, res):
        print("Processing response", req.url)


app.add_middleware(SimpleCustomMiddleware)


@app.route("/json")
def json_handler(req, resp):
    resp.json = {"name": "data", "type": "JSON"}


@app.route("/text")
def text_handler(req, resp):
    resp.text = "This is a simple text"


# Enable JWT Login
def validate_user(request: Request):
    return {"user": "foo"}


app.config["SECRET"] = "my_secret"
app.config["JWT_EXPIRE_SECONDS"] = 100
app.enable_jwt_login(validate_user_func=validate_user)

if __name__ == "__main__":
    from little_api.debug_server import DebugServer

    DebugServer(application=app, port=8080).run()
