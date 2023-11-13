import json
import pprint
import sys

if len(sys.argv) < 3:
    print('please provide the path to the Eevee configuration file and the training data (and optionally the dev data for model selection)')
    exit(1)

machamp_types = {'seq_bio': 'seq_bio', 'seq': 'seq', 'class': 'classification'}

data = json.load(open(sys.argv[1]))
train_path = sys.argv[2]
dev_path = None
if len(sys.argv) > 3:
    dev_path = sys.argv[3]

print("Configuration of Eevee")
pprint.pprint(data)

input_indices = [x['input_index'] for x in data]
if len(set(input_indices)) != 1:
    print('error, input indices are at different columns: ', input_indices)
    exit(1)

config = {}
config['train_data_path'] = train_path
if dev_path != None:
    config['dev_data_path'] = dev_path
config['word_idx'] = int(input_indices[0])
config['tasks'] = {}
for task in data:
    task_config = {}
    eeveeName = task['type']['name']
    if eeveeName not in machamp_types:
        print("error, " + eeveeName + ' is not a known task type in Eevee')
    task_config['task_type'] = machamp_types[task['type']['name']]
    task_config['column_idx'] = task['output_index']
    taskName = task['title']
    if task_config['column_idx'].isdigit():
        task_config['column_idx'] = int(task_config['column_idx'])
    else:
        taskName = task_config['column_idx'][2:].strip()
        task_config['column_idx'] = -1
    config['tasks'][taskName] = task_config

if '.json' in sys.argv[1]:
    outPath = sys.argv[1].replace('.json', '-machamp.json')
    dataName = sys.argv[1].replace('.json', '')
else:
    outPath = sys.argv[1] + '-machamp.json'
    dataName = sys.argv[1]

print()
print("Configuration of MaChAmp")
pprint.pprint({dataName: config})

json.dump({dataName: config}, open(outPath, 'w'), indent=4)
cmd = 'python3 train.py --dataset_configs ' + outPath
print(cmd)

