import os
import sys

from tornado.web import RequestHandler, Application

from jetbrains_license_server.signature import sign

# Template String
RELEASE_CONTENT = '<ReleaseTicketResponse>' \
                  '<message></message>' \
                  '<responseCode>OK</responseCode>' \
                  '<salt>{salt}</salt>' \
                  '</ReleaseTicketResponse>'
OBTAIN_CONTENT = '<ObtainTicketResponse>' \
                 '<message></message>' \
                 '<prolongationPeriod>{period}</prolongationPeriod>' \
                 '<responseCode>OK</responseCode>' \
                 '<salt>{salt}</salt>' \
                 '<ticketId>1</ticketId>' \
                 '<ticketProperties>licensee={name}\tlicenseType=0\t</ticketProperties>' \
                 '</ObtainTicketResponse>'
BODY = '<!-- {} -->\n{}'


class ReleaseTicketHandler(RequestHandler):
    def get(self):
        salt = self.get_argument('salt', '')
        content = RELEASE_CONTENT.format(salt=salt)
        signature = sign(content)
        body = BODY.format(signature, content)
        self.write(body)


class ObtainTicketHandler(RequestHandler):
    def get(self):
        salt = self.get_argument('salt', '')
        if os.path.basename(sys.argv[0]) == 'main_single.py':
            name = self.get_argument('userName', '')
        else:
            from jetbrains_license_server.db import get_username_by_port
            port = self.request.host.split(':')[1]
            try:
                name = get_username_by_port(port)
            except Exception:
                return
        period = '607875500'
        content = OBTAIN_CONTENT.format(salt=salt, name=name, period=period)
        signature = sign(content)
        body = BODY.format(signature, content)
        self.write(body)


def make_app():
    urls = [
        (r'/rpc/releaseTicket.action', ReleaseTicketHandler),
        (r'/rpc/obtainTicket.action', ObtainTicketHandler),
    ]
    return Application(urls)
