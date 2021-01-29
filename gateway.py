from csv_io import *
import re


class Gateway:
    def __init__(self, mac: str, hostname: str, model: str):
        self.mac = mac
        self.hostname = hostname
        self.model = model
        self.domain_name = str("SKIGW" + mac[2:]).upper()
        self.description = self.domain_name + " // " + hostname
        self.__max_ports: int = 0
        if model == "VG204":
            self.__max_ports = 4
            self.__subunit_count = 4
        elif model == "VG310":
            self.__max_ports = 24
            self.__subunit_count = 24
        elif model == "VG320":
            self.__max_ports = 48
            self.__subunit_count = 24
        else:
            raise Exception(f'Invalid gateway model: {model}')

        self.lines: list[dict] = []
        self.savename = get_valid_filename(hostname + "_" + model + ".csv")

    # returns false if gway is full
    def add_line(self, line: dict) -> bool:
        if line and self.count() < self.__max_ports:
            for key in line.keys():
                if re.search(r'name', key, re.IGNORECASE):
                    match = str(key)
                    break
            else:
                raise Exception('No NAME field found in file')
            line_name = line[match]

            entry: dict = {"DOMAIN NAME": self.domain_name, "DESCRIPTION": self.description, "SLOT": "0",
                           "SUBUNIT": str(int(self.count() / self.__subunit_count)),
                           "PORT NUMBER": str(self.count() % self.__subunit_count),
                           "PORT DESCRIPTION": self.hostname + " // " + line_name}
            try:
                entry["PORT DIRECTORY NUMBER"] = line["DN"]
            except KeyError:
                try:
                    entry["PORT DIRECTORY NUMBER"] = line["Phone Number"]
                except KeyError:
                    raise Exception("DN or Phone Number not found in line")
            entry.update({"DISPLAY": line_name, "LINE DESCRIPTION": line_name})
            self.lines.append(entry)
            return True

        elif self.count() < self.__max_ports:
            print(f"tried to insert a blank line... (count: {len(self.lines)})")
            return False

        else:
            return False

    def count(self) -> int:
        return len(self.lines)

    def export_to_csv(self):
        csv_dict_write(self.savename, self.lines)

    def debug_print(self):
        print(", ".join(list(self.lines[0].keys())))
        for line in self.lines:
            print(", ".join(list(line.values())))


def standarize_name(name: str) -> str:
    # escape from anything with a number in it
    if any(x.isnumeric() for x in name):
        return name
    # Last Jr, First Middle
    elif re.search(r'\w, *\w', name):
        parts: list[str] = re.split(r', *', name)
        if len(parts) != 2:  # escape if we're dealing with something abnormal
            return name
        return parts[1].split(" ")[0] + ' ' + parts[0].split(" ")[0]
    # First M Last Jr
    elif re.search(r'\w+ \w \w+', name):
        return name.split(" ")[0] + ' ' + name.split(" ")[2]
    # ends with Jr, Sr, II, III, etc
    elif any(x in name.split(" ")[-1] for x in ['Jr', 'JR', 'Sr', 'SR', 'II', 'III', 'IV']):
        return " ".join(name.split(" ")[:-1])
    else:
        return name
