from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop, PeriodicCallback

from jetbrains_license_server.db import get_port_set
from jetbrains_license_server.license_server import make_app


def sync_user_callback():
    print('sync user')
    # get the latest user port list
    ports = get_port_set()
    ports_listening = set(listeners.keys())
    # add listener for the new port
    for new_port in ports - ports_listening:
        print('new port:' + str(new_port))
        listeners[new_port] = HTTPServer(make_app())
        listeners[new_port].listen(new_port)
    # delete past port
    for past_port in ports_listening - ports:
        print('del port:' + str(past_port))
        listeners[past_port].close_all_connections()
        listeners[past_port].stop()
        del listeners[past_port]


def main():
    global listeners
    listeners = {}  # port:app_instance
    io_loop = IOLoop.instance()
    sync_user = PeriodicCallback(sync_user_callback, 1000 * 30)
    sync_user_callback()  # first sync
    sync_user.start()
    try:
        io_loop.start()
    except KeyboardInterrupt:
        sync_user.stop()
        io_loop.stop()


if __name__ == '__main__':
    main()
