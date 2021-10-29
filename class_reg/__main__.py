import scraper
import json
import sys

possible_params = set(("txt_courseNumber", "s2id_txt_instructor"))

# TODO: Let user input max number from each search

if len(sys.argv) != 2:
    print("ERR: wrong number of arguments \nUsage: python3 class_reg <path_to_json>")
    sys.exit(1)

try:
    data_string = open(sys.argv[1], 'r').read()
    data_dict = json.loads(data_string)
except OSError as err:
    print(err)
    sys.exit(1)
except json.decoder.JSONDecodeError as err:
    print(f"ERR: malformed JSON \n{err}")
    sys.exit(1)
if len(data_dict.keys()) <= 0:
    print("ERR: requires at least one class")
    sys.exit(1)

# Assert we have a valid search param for each class
for class_name in data_dict.keys():
    given_params = set(data_dict[class_name].keys())
    if (given_params.isdisjoint(possible_params)):
        print(f"ERR: class '{class_name}' has no valid search parameters")
        sys.exit(1)

# List of the returned dictionaries from the search
capacities = []

for class_name in data_dict.keys():
    capacities.extend(scraper.check_classes(data_dict[class_name]))

for class_dict in capacities:
    print()
    print(class_dict['course_name'])
    room = class_dict['seats_left']
    print(f"{'CLASS FULL: ' if not int(room) else ''}{room} out of {class_dict['total_seats']} total seats available")
    print()