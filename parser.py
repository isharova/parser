import os
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('libraries_path', type=str)
parser.add_argument('--platform', type=str, required=False, choices=['win', 'lin', 'mac'])
args = parser.parse_args()

folders = []
if args.platform == "win":
    folders = ["windows"]
elif args.platform == "lin":
    folders = ["linux"]
elif args.platform == "mac":
    folders = ["macosx"]
else:
    folders = ["windows", "linux", "macosx"]

domains = ['ippcc', 'ippch', 'ippdc']

with open('result.csv', 'w', newline='') as csvfile:
    headers = ['OS', 'Domain', 'Optimization', 'Pass rate']
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()

    for folder in folders:
        data_dir = os.path.join(args.libraries_path, folder)
        for root, dirs, _ in os.walk(data_dir):
            for dir in dirs:
                if dir not in domains:
                    continue
                files = os.listdir(os.path.join(root, dir))
                if not files:
                    output_line = {'OS': folder[0].upper() + folder[1:],
                                   'Domain': dir,
                                   'Optimization': 'n/a',
                                   'Pass rate': 'n/a'}
                    writer.writerow(output_line)
                    continue
                for file in files:
                    filename_splitted = os.path.splitext(file)
                    if filename_splitted[1] == '.txt' and os.path.exists(os.path.join(root, dir, filename_splitted[0] + '.end')):
                        number_of_tests = None
                        sucesses = None
                        for line in open(os.path.join(root, dir, file), 'r').read().split('\n'):
                            if 'Number of tests' in line:
                                number_of_tests = int(line.split(':')[1].strip('|'))
                            if 'Successes' in line:
                                sucesses = int(line.split(':')[1].strip('|'))
                        if number_of_tests is not None and sucesses is not None and number_of_tests:
                            percent = str(int(float(sucesses/number_of_tests) * 100)) + '%'
                        else:
                            percent = 'aborted'
                        optimization = filename_splitted[0].split('_')[-1].upper()
                        output_line = {'OS': folder[0].upper() + folder[1:],
                                       'Domain': dir,
                                       'Optimization': optimization,
                                       'Pass rate': percent}
                        writer.writerow(output_line)
