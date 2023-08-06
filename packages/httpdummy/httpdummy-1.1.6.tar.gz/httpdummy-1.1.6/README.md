# HTTPDummy

```
                                    __________________
                                   /        ________  \
                                  /   _____|       |___\
                                 |   /  __         __   |
                                /|  |  /o \   _   /o \  |  
                               | | /           \        |
                                \|/   __           __   |
                                  \    |\_________/|   /   
                                   \___|___________|__/                  
                                        |         |
                                       /\_________/\
    _   _ _____ _____ ____  ____     _/     \ /     \_
   | | | |_   _|_   _|  _ \|  _ \ _ | _ _ __ V__  _ __|___  _   _
   | |_| | | |   | | | |_) | | | | | | | '_ ` _ \| '_ ` _ \| | | |
   |  _  | | |   | | |  __/| |_| | |_| | | | | | | | | | | | |_| |
   |_| |_| |_|   |_| |_|   |____/ \__,_|_| |_| |_|_| |_| |_|\__, |
                                                            |___/
```

HTTPDummy is a development HTTP server tool that prints information about the requests it receives to stdout.

## Installation

With PIP:

```
pip install httpdummy
```

With Docker:

```
docker pull ksofa2/httpdummy
```

## Usage

```
usage: httpdummy [-h] [-H [HEADERS]] [-B [BODY]] [-a ADDRESS] [-p PORT]
                 [-r [RESPONSE_FILE]]

A dummy http server that prints requests and responds

optional arguments:
  -h, --help            show this help message and exit
  -H [HEADERS], --headers [HEADERS]
  -B [BODY], --body [BODY]
  -a ADDRESS, --address ADDRESS
  -p PORT, --port PORT
  -r [RESPONSE_FILE], --response-file [RESPONSE_FILE]
```

  - Add the `-H` flag to print request headers.
  - Add the `-B` flag to print request body.

Use the `--response-file` to specify a YAML file to set up custom responses for arbitrary method / path combinations. For example, this command...

```
httpdummy --response-file ~/repsonses.yaml
```

... with `~/responses.yaml` contents ...

```
---
responses:
  GET /api/foo:
    status: 200
    headers:
      Foo: bar
      Sna: fu
    body: |+
      Hi there!

      How are you?

  POST /api/foo:
    status: 201
    headers:
      Content-type: application/json
    body: |+
      {"answer": 42}
```

... will make HTTPDummy respond to POST requests to `/api/foo` with the 201 status code, and the configured headers and body.

NOTE: When started with a response file, HTTPDummy will listen for changes to that file and restart when a change is detected to reload the response definitions.

## Environment Variables

These environmental variables will be used as values for their corresponding command-line options. If the command-line option is used, that value will override the one set in the environment.

  - `HTTPDUMMY_ADDRESS`
  - `HTTPDUMMY_PORT`
  - `HTTPDUMMY_HEADERS`
  - `HTTPDUMMY_BODY`
  - `HTTPDUMMY_RESPONSE_FILE`

## Docker

An image for HTTPDummy is available on DockerHub: <https://hub.docker.com/r/ksofa2/httpdummy>

```
docker run -it -p 127.0.0.1:5000:5000 ksofa2/httpdummy
```

NOTE: The `HTTPDUMMY_HEADERS` and `HTTPDUMMY_BODY` are turned on by default in the Docker image.

An example `docker-compose.yaml` file:

```
---
version: '3'

services:
  httpdummy:
    image: ksofa2/httpdummy
    environment:
      - HTTPDUMMY_RESPONSE_FILE=/srv/responses.yaml
    ports:
      - 127.0.0.1:5000:5000
    volumes:
      - .:/srv
```
