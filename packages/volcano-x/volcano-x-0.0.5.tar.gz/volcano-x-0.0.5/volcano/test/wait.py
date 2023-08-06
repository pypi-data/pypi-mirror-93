import time
import socket


def wait_tcp(addr: str, port: int, nb_attempts: int = 5) -> None:

    for _i in range(nb_attempts):
        sock = None
        try:
            sock = socket.create_connection((addr, port), timeout=5.0)
            return
        except Exception:
            time.sleep(2.0)
        finally:
            if sock is not None:
                try:
                    sock.close()
                except Exception:
                    pass
    raise Exception("Failed waiting connection to {}:{}".format(addr, port))
