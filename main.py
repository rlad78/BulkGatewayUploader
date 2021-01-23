import re
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from data import Data
from gateway import Gateway


def shape_mac(address: str) -> str:
    mac = ""
    alphanums = ''.join([x for x in address if x.isalnum()])
    for c in alphanums:
        is_octal = re.search(r'[a-fA-F0-9]', c)
        if not is_octal:
            return c
        mac = mac + c
    if len(mac) != 12:
        return str(len(mac))
    return mac


def get_filename() -> str:
    Tk().withdraw()
    return askopenfilename()


def example_csv_format():
    def center(s, width):
        adjusted = s
        for i in range(width - len(s)):
            if i % 2 == 0:
                adjusted = adjusted + ' '
            else:
                adjusted = ' ' + adjusted
        return ' ' + adjusted + ' '

    def left(s, width):
        return ' ' + s + (' ' * (width - len(s))) + ' '


    example: dict = {
        "Name": "Richard Carter",
        "Phone Number": "8646569969",
        "...   ": "...   "
    }
    # |========================================|
    # |      Name      | Phone Number | ...    |
    # |----------------------------------------|
    # | Richard Carter | 8646569969   | ...    |
    # | ...            | ...          | ...    |
    # |========================================|
    column_widths: dict = {}
    for k, v in example.items():
        column_widths[k] = len(k) if len(k) > len(v) else len(v)
    border: str = ('|' +
                   '=' * sum(column_widths) +
                   '=' * (len(dict) * 2) +
                   '=' * (len(dict) - 1))

    print("This program uses a .csv file that has the following format:\n\n")
    print(border)
    print('|'.join([center(x, column_widths[x]) for x in example.keys()]))
    print(border.replace('=', '-'))
    # TODO: print the rest please


# get data file location
print("Opening file picker for .csv...")
csv_file: str = get_filename()
if not csv_file:
    print("No file chosen. Exiting...")
data = Data(csv_file)

# get gateway type
gateway_types: dict = {
    "1": {"model": "VG204", "ports": 4},
    "2": {"model": "VG310", "ports": 24},
    "3": {"model": "VG320", "ports": 48}
}
print('Please choose a gateway type:\n')
for index in gateway_types:
    print(f'({index}) {gateway_types[index]["model"]} [{gateway_types[index]["ports"]} ports]')
choice: str = input("Choice: ")
while choice not in gateway_types:
    choice = input("Invalid choice, please try again: ")
gateway_model: str = gateway_types[choice]["model"]
gateway_max: int = gateway_types[choice]["ports"]
gateway_count: int = 1 + (int((data.count() - 1) / gateway_max))

# get gateway info
print(f'For the {data.count()} lines provided, {gateway_count} gateways will be needed.')

gateways: list = []
for n in range(gateway_count):
    gateway_mac: str = ""
    gateway_hostname = ""
    while len(gateway_mac) != 12:
        gateway_mac = shape_mac(input(f"[Gateway {n + 1}]: Enter the full 12-digit MAC address: "))
        if gateway_mac.isnumeric() and len(gateway_mac) != 12:
            print(
                f'Sorry, that MAC is only {gateway_mac} characters long. MAC addresses need to be 12 characters long.')
        elif len(gateway_mac) == 1:
            print(f'The following character is invalid: {gateway_mac}')
        elif any(g.mac == gateway_mac for g in gateways):
            print(f'Sorry, "{gateway_mac}" is already a MAC address in use')
            gateway_mac = ""

    while len(gateway_hostname) == 0:
        gateway_hostname = input(f"[Gateway {n + 1}]: Enter the desired hostname: ")
        if any(g.hostname == gateway_hostname for g in gateways):
            print(f'Sorry, "{gateway_hostname}" is already a hostname in use')
            gateway_hostname = ""

    gateways.append(Gateway(gateway_mac, gateway_hostname, gateway_model))
    print(f'{gateway_hostname} [{gateway_mac}] added!')
    time.sleep(0.7)

gateways.reverse()
current_gateway: Gateway = gateways.pop()
finished_gateways: list[Gateway] = []
for line in data:
    if not current_gateway.add_line(line):
        finished_gateways.append(current_gateway)
        current_gateway = gateways.pop()
        current_gateway.add_line(line)

finished_gateways.append(current_gateway)
for gateway in finished_gateways:
    gateway.export_to_csv()
