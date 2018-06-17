from tornado.ioloop import IOLoop

from jetbrains_license_server.license_server import make_app


def main():
    app = make_app()
    app.listen(1017)
    try:
        IOLoop.current().start()
    except KeyboardInterrupt:
        IOLoop.current().stop()


if __name__ == '__main__':
    main()
