import argparse
import socket
import time
from dataclasses import dataclass
from random import random
from uuid import uuid4

RETRIES: int = 3


@dataclass
class InputArgs:
    ip: str
    port: 38888


@dataclass
class ScanInput:
    person_id: str
    expiration: int


def _parse_input() -> InputArgs:
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', '-i', type=str, help="The gate's ip")
    parser.add_argument('--port', '-p', type=int, help="The port the gate is listening on")
    return InputArgs(**vars(parser.parse_args()))


def _wait_for_scan() -> ScanInput:
    time.sleep(int(random() * 10))
    return ScanInput(
        person_id=str(uuid4()),
        expiration=int(time.time() + 10),
    )


def _report_enter(person_id: str, gate_open_time: float, gate_close_time: float) -> None:
    print(f"Person {person_id} entered the store. Gate was open between {gate_open_time} and {gate_close_time}")


def wait_for_state(open_socket: socket.socket, state: bytes) -> None:
    open_socket.send(b's')
    current_state = open_socket.recv(1)
    while current_state != state:
        time.sleep(.1)
        open_socket.send(b's')
        current_state = open_socket.recv(1)


def _main():
    input_args: InputArgs = _parse_input()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as gate_socket:
        gate_socket.connect((input_args.ip, input_args.port))

        while True:
            scan: ScanInput = _wait_for_scan()

            if time.time() > scan.expiration:
                print("Error: QR expired")
                continue

            gate_socket.sendall(b's')
            gate_state = gate_socket.recv(1)
            if gate_state == b'1':
                print("Error: scanned while gate is open")
                continue

            for i in range(RETRIES):
                gate_socket.sendall(b'o')
                response = gate_socket.recv(1)
                if response != b'0':
                    print(f"Couldn't open gate. Retrying ({i + 1} / {RETRIES})...")
                else:
                    break
            else:
                print("Error: problem with the gate! Please contact support")
                continue

            wait_for_state(open_socket=gate_socket, state=b'o')
            gate_open_time: float = time.time()

            wait_for_state(open_socket=gate_socket, state=b'c')
            gate_close_time: float = time.time()

            _report_enter(person_id=scan.person_id, gate_open_time=gate_open_time, gate_close_time=gate_close_time)


if __name__ == '__main__':
    _main()
