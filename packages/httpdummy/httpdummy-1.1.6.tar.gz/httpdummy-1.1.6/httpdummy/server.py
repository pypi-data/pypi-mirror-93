from os import getenv
from yaml import safe_load as yaml_safe_load


from colorama import Fore, Style
from werkzeug.serving import WSGIRequestHandler, is_running_from_reloader
from werkzeug.wrappers import Request, Response


def print_logo():
    '''Print the HTTPDummy logo. uses is_running_from_reloader to prevent
    double printing on startup and reprinting on reload.'''

    LOGO = '''
                                    __________________
                                   /        ________  \\
                                  /   _____|       |___\\
                                 |   /  __         __   |
                                /|  |  /o \   _   /o \  |  
                               | | /           \        |
                                \|/   __           __   |
                                  \    |\_________/|   /   
                                   \___|___________|__/                  
                                        |         |
                                       /\_________/\\
    _   _ _____ _____ ____  ____     _/     \ /     \_
   | | | |_   _|_   _|  _ \|  _ \ _ | _ _ __ V__  _ __|___  _   _
   | |_| | | |   | | | |_) | | | | | | | '_ ` _ \| '_ ` _ \| | | |
   |  _  | | |   | | |  __/| |_| | |_| | | | | | | | | | | | |_| |
   |_| |_| |_|   |_| |_|   |____/ \__,_|_| |_| |_|_| |_| |_|\__, |
                                                            |___/
'''
    if not is_running_from_reloader():
        for line in LOGO.splitlines():
            print(f'{Fore.CYAN}{line}{Fore.RESET}')


class HttpDummy(object):
    def __init__(self, conf):
        self.conf = conf
        self._responses = {}
        if self.conf['response_file']:
            try:
                self._responses = yaml_safe_load(
                    self.conf['response_file'])['responses']
            except Exception as exc:
                raise exc

    def get_response(self, path, method='GET'):
        r = Response()
        r.status_code = 200
        r.headers.set('Server', 'HTTPDummy')
        r.data = 'HTTPDummy'

        fresp = (self._responses.get(f'{method} {path}', None) or
                 self._responses.get(path, None))

        if fresp:
            r.status_code = int(fresp.get('status', r.status_code))
            for (k, v) in fresp.get('headers', {}).items():
                r.headers.set(k, v)
            r.data = fresp.get('body', r.data)

        return r

    def dispatch_request(self, request):
        print(
            f'{Style.BRIGHT}{request.method}{Style.NORMAL} '
            f'{request.environ.get("RAW_URI")}'
        )

        if self.conf.get('headers'):
            for (k, v) in request.headers:
                print(f'{Style.DIM}{k}: {v}{Style.NORMAL}')
            if self.conf.get('body') and len(request.data) > 0:
                print()

        if self.conf.get('body') and len(request.data) > 0:
            for line in request.data.decode('utf-8').splitlines():
                print(f'{Style.DIM}{line}{Style.NORMAL}')

        return self.get_response(request.path, request.method)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


class NoLogRequestHandler(WSGIRequestHandler):
    '''This class just supresses the standard werkzeug request logging.'''
    def log_request(self, *args, **kwargs):
        pass


def main():
    import argparse

    from werkzeug.serving import run_simple

    def str2bool(val):
        return str(val).lower() in ('true', 'yes', 'y', 'on', '1')

    parser = argparse.ArgumentParser(
        description='A dummy http server that prints requests and responds')

    parser.add_argument('-H', '--headers', type=str2bool, nargs='?',
                        const=True, default=getenv('HTTPDUMMY_HEADERS'))
    parser.add_argument('-B', '--body', type=str2bool, nargs='?',
                        const=True, default=getenv('HTTPDUMMY_BODY'))
    parser.add_argument('-a', '--address', type=str,
                        default=getenv('HTTPDUMMY_ADDRESS', '127.0.0.1'))
    parser.add_argument('-p', '--port', type=int,
                        default=getenv('HTTPDUMMY_PORT', 5000))
    parser.add_argument('-r', '--response-file', type=argparse.FileType('r'),
                        nargs='?',
                        default=getenv('HTTPDUMMY_RESPONSE_FILE', None))
    args = parser.parse_args()

    use_reloader = (
        str2bool(getenv('HTTPDUMMY_RELOADER', '0')) or args.response_file)
    if args.response_file:
        extra_files = [args.response_file.name]
    else:
        extra_files = None

    app = HttpDummy(vars(args))

    print_logo()

    run_simple(
        args.address, args.port, app,
        request_handler=NoLogRequestHandler,
        use_debugger=str2bool(getenv('HTTPDUMMY_DEBUGGER', '0')),
        reloader_type=getenv('HTTPDUMMY_RELOADER_TYPE', 'watchdog'),
        use_reloader=use_reloader,
        extra_files=extra_files,
    )
