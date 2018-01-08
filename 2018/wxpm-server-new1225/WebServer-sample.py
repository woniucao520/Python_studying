import bcrypt
import concurrent.futures
import os.path
import markdown

import tornado
from tornado import escape,gen,httpserver,ioloop,web
from tornado.options import define, options

import re
import unicodedata


define("port", default=8887, type=int)


# A thread pool to be used for password hashing with bcrypt
executor = concurrent.futures.ThreadPoolExecutor(2)

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/archive", ArchiveHandler),
            (r"/feed", FeedHandler),
            (r"/entry/([^/]+)", EntryHandler),
            (r"/compose", ComposeHandler),
            (r"/auth/create", AuthCreateHandler),
            (r"/auth/login", AuthLoginHandler),
            (r"/auth/logout", AuthLogoutHandler),
        ]

        settings = dict(
            blog_title=u"Tornado Blog",
            tempate_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={"Entry": EntryModule},
            xsrf_cookie=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/auth/login",
            debug=True,
        )

        super(Application, self).__init__(handlers, **settings)

        self.db = None



class BaseHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("blog_user")
        if not user_id:
            return None

        return self.db.get('sql to get user')

    def any_author_exists(self):
        return bool(self.db.get('sql to check'))



class HomeHandler(BaseHandler):

    def get(self):
        entries = self.db.query('get entries sql')

        if not entries:
            self.redirect("/compose")
            return

        self.render("home.html", entries=entries)

class EntryHandler(BaseHandler):

    def get(self, slug):
        entry = self.db.query('sql et entry by slug')
        if not entry: raise tornado.web.HTTPError(404)

        self.render("entry", entry=entry)

class ArchiveHandler(BaseHandler):

    def get(self):
        entries = self.db.query('sql to get all entries')

        self.render("archive.html", entries=entries)

class FeedHandler(BaseHandler):

    def get(self):
        entries = self.db.query('sql to get all entries recent published')
        self.set_header("Content-Type", "application/atom+xml")
        self.render("feed.xml", entries=entries)

class ComposeHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id", None)
        entry = None
        if id:
            entry = self.db.get("sql to get the entry")

        self.render("compose.html", entry=entry)

    @tornado.web.authenticated
    def post(self):
        id = self.get_argument("id", None)
        title = self.get_argument("title")
        text = self.get_argument("markdown")
        html = markdown.markdown(text)

        if id:
            entry = self.db.get("sql to get the entry by id")
            if not entry: raise tornado.web.HTTPError(404)
            slug = entry.slug
            self.db.execute('sql to update data')
        else:
            slug = unicodedata.normalize("NFKD", title).encode("ascii", "ignore")
            slug = re.sub(r"[^\w]+"," ", slug)
            slug = "-".join(slug.lower().strip().split())
            if not slug: slug = 'entry'
            while True:
                #sql to check slug is exist
                slug += "-2"

            self.db.execute("sql to insert this entry")

        self.redirect("/entry/" + slug)

class AuthCreateHandler(BaseHandler):

    def get(self):
        self.render("create_author.html")

    @gen.coroutine
    def post(self):
        if self.any_author_exists():
            raise tornado.web.HTTPError('400', 'author already created')

        hashed_password = yield executor.submit(bcrypt.hashpw, tornado.escape.utf8(self.get_argument("password")), bcrypt.gensalt())
        author_id = self.db.execute("sql to insert author")

        self.set_secure_cookie("blogdemo_user", str(author_id))
        self.redirect(self.get_argument("next", "/"))


class AuthLoginHandler(BaseHandler):

    def get(self):
        if not self.any_author_exists():
            self.redirect("/auth/create")
        else:
            self.render("login.html", error=None)

    @gen.coroutine
    def post(self):
        author = self.db.get("sql to query user by email or id")

        if not author:
            self.render("login.html", error="email not found")
            return

        hashed_password = yield executor.submit(
            bcrypt.hashpw, tornado.escape.utf8(self.get_argument("password")),
            tornado.escape.utf8(author.hashed_password)
        )

        if hashed_password == author.hashed_password:
            self.set_secure_cookie("blogdemo_user", str(author.id))
            self.redirect(self.get_argument("next", "/"))
        else:
            self.render("login.html", error="incorrect password")

class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("blogdemo_user")
        self.redirect(self.get_argument("next", "/"))

class EntryModule(tornado.web.UIModule):

    def render(self, entry):
        return self.render_string("modules/entry.html", entry=entry)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()