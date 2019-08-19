import tornado.ioloop
import tornado.web
import zip_push
import bot_telegram


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        args = {}
        for x in self.request.arguments:
            args[x] = self.request.arguments[x][0].decode('utf-8')

        files_p = args.get('filespath')
        yad_p = args.get('yandpath')
        zip_p = args.get('zippath')
        tok = args.get('token')
        f = zip_push
        b = bot_telegram

        if f.main(files_p, zip_p, yad_p, tok) == 0:
            self.write('Files uploaded')
            b.reminder_message('Archive with files is uploaded')
        else:
            b.reminder_message('Today files are missing!')
            self.write('Today files are not received')
            self.set_status(500)
            return


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
