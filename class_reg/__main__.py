import scraper
import json
import sys

possible_params = set(("txt_courseNumber", "s2id_txt_instructor"))

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

    
sys.exit(0)

scraper.check_classes({})