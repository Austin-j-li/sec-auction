#!/usr/bin/env python3
"""The extraction sandbox's one route out. run_model.py starts it inside the sandbox, in front of the provider CLI.

The sandbox has no network of its own. This listens on the sandbox's loopback and passes each
connection through a Unix socket to the runner's allowlist proxy outside the sandbox. Then it runs
the provider command, whose HTTPS_PROXY points here, and exits with that command's exit code.

    python3 -I -S netbridge.py SOCKET PORT COMMAND...

Standard library only: the sandbox's own Python runs it with no site packages.
"""
import signal
import socket
import subprocess
import sys
import threading


def relay(source, sink):
    """Copy bytes one way until the source closes, then pass the close on."""
    try:
        while True:
            data = source.recv(65536)
            if not data:
                break
            sink.sendall(data)
    except OSError:
        pass
    try:
        sink.shutdown(socket.SHUT_WR)
    except OSError:
        pass


def bridge(client, path):
    with client:
        upstream = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        with upstream:
            try:
                upstream.connect(path)
            except OSError:
                return
            back = threading.Thread(target=relay, args=(upstream, client), daemon=True)
            back.start()
            relay(client, upstream)
            back.join()


def serve(server, path):
    while True:
        client, _ = server.accept()
        threading.Thread(target=bridge, args=(client, path), daemon=True).start()


def main():
    path, port, command = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
    server = socket.create_server(("127.0.0.1", port))
    threading.Thread(target=serve, args=(server, path), daemon=True).start()
    # close_fds=False keeps the descriptor that carries the Claude token; the listening socket is not inheritable.
    child = subprocess.Popen(command, close_fds=False)
    for signum in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
        signal.signal(signum, lambda received, frame: child.send_signal(received))
    code = child.wait()
    sys.exit(128 - code if code < 0 else code)


if __name__ == "__main__":
    main()
