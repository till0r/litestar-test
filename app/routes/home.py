from litestar import Request, get
from litestar.contrib.htmx.response import HTMXTemplate


@get(path="/", name="home")
async def home(request: Request) -> HTMXTemplate:
    return HTMXTemplate(
            template_name="home.html",
            context={
                "username": request.session.get("username"),
                "displayname": request.session.get("displayname")
            },
        )
