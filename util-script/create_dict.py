def create_dict_from_csv(filename):
    import csv
    lookup = {}
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = row['hazard'].lower() + "-" + row['demand_type'].lower()
            lookup[key] = row
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(lookup)

if __name__ == "__main__":
    create_dict_from_csv("range.csv")