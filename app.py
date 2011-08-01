import os
import tornado.ioloop
import tornado.web
import tornado.escape
import session

from base import BaseHandler

class Application(tornado.web.Application):
    def __init__(self):
        
        settings = dict(
            cookie_secret = "e446976943b4e8442f099fed1f3fea28462d5832f483a0ed9a3d5d3859f==78d",
            session_secret = "3cdcb1f00803b6e78ab50b466a40b9977db396840c28307f428b25e2277f1bcc",
            memcached_address = ["127.0.0.1:11211"],
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies = True,
            login_url = "/login",
        )
        
        handlers = [
            (r"/", MainHandler),
            (r"/login", LoginHandler)
        ]
        
        tornado.web.Application.__init__(self, handlers, **settings)
        self.session_manager = session.SessionManager(settings["session_secret"], settings["memcached_address"])
        
        
class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        username = tornado.escape.xhtml_escape(self.current_user)
        self.write("What's up, " + username + "?")

class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")
        self.write('')
    
    def post(self):
        self.session["user_name"] = self.get_argument("name")
        self.session.save()
        self.redirect("/")

if __name__ == "__main__":
    app = Application()
    app.listen("8080")
    print "start on port 8080..."
    tornado.ioloop.IOLoop.instance().start()
