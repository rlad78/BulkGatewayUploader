import csv
import re
import concurrent.futures


def csv_as_list(file_name: str) -> list[list[str]]:
    with open(file_name, encoding="utf-8-sig") as csv_file:
        return list(csv.reader(csv_file, delimiter=","))


def csv_as_dict_list(file_name: str) -> list[dict]:
    with open(file_name, encoding="utf-8-sig") as csv_file:
        return list(csv.DictReader(csv_file, delimiter=","))


def csv_as_hash(file_name: str, hash_key: str) -> dict[dict]:
    dict_list: list[dict] = csv_as_dict_list(file_name)
    categories: list[str] = list(dict_list[0].keys())
    hash_list = {}
    if hash_key not in categories:
        raise Exception(f'[csv_as_hash]: hash_key "{hash_key}" not found in {file_name}\n'
                        + "{" + " ".join(categories) + "}")
    for entry in dict_list:
        hash_list[entry[hash_key]] = entry
    return hash_list


def csv_dict_write(file_name: str, dict_lines: list[dict]):
    with open(file_name, mode='w') as csv_file:
        fieldnames: list[str] = list(dict_lines[0].keys())
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(dict_lines)
        print(f'Wrote {len(dict_lines)} lines to {csv_file.name}')


def csv_write(file_name: str, head: list[str], lines: list[list[str]]):
    with open(file_name, mode='w') as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(head)
        writer.writerows(lines)
        print(f'Wrote {len(lines)} lines to {csv_file.name}')


def csv_hash_write(file_name: str, hash_table: dict[dict]):
    dict_list: list[dict] = []
    for entry in hash_table:
        dict_list.append(hash_table[entry])
    csv_dict_write(file_name, dict_list)


def get_valid_filename(s: str) -> str:
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


def get_file_stack(files: list[tuple[str, str]]) -> dict:
    futures = {}
    return_dicts = {}
    getter = concurrent.futures.ThreadPoolExecutor()
    for label, file in files:
        futures[label] = getter.submit(csv_as_dict_list, file)
    for key, contents in futures.items():
        return_dicts[key] = contents.result()
    return return_dicts
