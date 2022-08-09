# TCP Chat

> Most of the project was generated using GitHub Copilot

This is a simple TCP Chat CLI in Python.

## Running server

```bash
$ server --help

Usage: server.py [OPTIONS]

Options:
  -h, --host TEXT              Hostname or IP address.
  -p, --port INTEGER           Port number.
  --max-connections INTEGER    Maximum number of connections.
  --max-waiting-queue INTEGER  Maximum number of waiting queue.
  --help                       Show this message and exit.
```

## Connecting to server

```bash
$ client --help
Usage: client.py [OPTIONS]

Options:
  -h, --host TEXT     Hostname or IP address.
  -p, --port INTEGER  Port number.
  --help              Show this message and exit.
```

## Setup

Install dependencies using `pipenv`.
To install exact versions from `Pipfile.lock` use `pipenv sync`.
Or install latest versions with `pipenv install`.

Then, install the package:

```bash
(tcp-chat) $ pip install -e .
...
Successfully installed tcp-chat-x.y.z
$ server --help
$ client --help
```

Or just run the files:

```bash
(tcp-chat) $ python server.py --help
(tcp-chat) $ python client.py --help
```
