from fcp import CANMessage, Fcp, Spec
from colored import fg, bg, attr
from termcolor import colored, cprint
from .console import print_console
import sys
import json
import socket
import time

class Supervisor:
    def __init__(self, cfg):
        self.signals = {}
        self.spec = Spec()
        with open(cfg["root"]+"/lib/can-ids-spec/fst10e.json", "r") as f:
            self.spec.decompile(json.loads(f.read()))
        self.fcp_obj = Fcp(spec=self.spec)

        hello_msg = bytes(json.dumps({
            "sid": 1,
            "dlc": 1,
            "data": [0, 1, 2, 3],
            "timestamp": 0
        }), "ascii")
        udp_ip = cfg["vsniffer_ip"]
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        # Initialize
        for port in cfg["vsniffer_ports"]:
            print_console("Contacting vsniffer ---> Port: " + str(port), False, cfg)
            self.udp_sock.sendto(hello_msg, (udp_ip, int(port)))


    def register_signal(self, msg):
        for signal in msg[1]:
            #print("Registering -> " + signal)
            self.signals[signal] = msg[1][signal]

    def get_signal(self, sig_name):
        # Check for value changes
        previous_value = None
        matches = 0
        null_matches = 0
        while matches < 5:
            current_value_err = 100
            while current_value_err > 1e-3:
                if self.signals[sig_name] == 0:
                    null_matches += 1
                    if null_matches > 100:
                        break
                    continue
                null_matches = 0
                if previous_value is not None:
                    current_value_err = abs(round(previous_value - self.signals[sig_name], 2))
                previous_value = self.signals[sig_name]
                if current_value_err > 1e-3:
                        matches = 0
            matches += 1
            time.sleep(0.02)
        return self.signals[sig_name]

    def terminate(self):
        self._run = False


    def run(self):
        self._run = True
        self.udp_sock.settimeout(10)
        while self._run:
            try:
                data, _ = self.udp_sock.recvfrom(1024) # buffer size is 1024 bytes
                new_msg = CANMessage.decode_json(data)
                decoded_msg = self.fcp_obj.decode_msg(new_msg)
                self.register_signal(decoded_msg)
                self.udp_sock.settimeout(0.1)
            except socket.timeout:
                if (self._run):
                    print('%s[ERROR] Socket timeout! %s' % (fg(196), attr(0)))
                break