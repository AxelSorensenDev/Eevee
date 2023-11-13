import datasets
import ast
import copy
import sys

def load_dataset(name1, name2=None):
    print('Loading ' +name1.strip() + ('' if name2 == None else '-' + name2) + '...')
    args = [name1]
    if name2 != None:
        args.append(name2)
    try:
        dataset = datasets.load_dataset(*args, beam_runner='DirectRunner')
        return dataset
    except (TypeError, ValueError):
        dataset = datasets.load_dataset(*args)
        return dataset

def clean(value):
    if type(value) == str:
        return value.replace('\t', ' ')
    return str(value)
    

def save_sent_level(dataset, gold_columns, name):
    for split in dataset:
        outPath = name + '-' + split + '.conll'
        print('Writing to: ' + outPath + '...')
        outFile = open(outPath, 'w')
        for item in dataset[split]:
            conll_data = []
            for column in gold_columns:
                if column in item:
                    conll_data.append(clean(item[column]))
                else:
                    conll_data.append('_')
 
            outFile.write('\t'.join(conll_data) + '\n')
        outFile.close()

def save_word_level(dataset, gold_columns, name):
    for split in dataset:
        outPath = name + '-' + split + '.conll'
        print('Writing to: ' + outPath + '...')
        outFile = open(outPath, 'w')
        for item in dataset[split]:
            # item = {'id': '0', 'tokens': ['EU', 'rejects', 'German', 'call', 'to', 'boycott', 'British', 'lamb', '.'], 'pos_tags': [22, 42, 16, 21, 35, 37, 16, 21, 7], 'chunk_tags': [11, 21, 11,
# 12, 21, 22, 11, 12, 0], 'ner_tags': [3, 0, 7, 0, 0, 0, 7, 0, 0]}

            sent_data = []
            conll_data = []
            for column in gold_columns:
                if column in item:
                    if type(item[column]) != list:
                        sent_data.append('# ' + column + ' = ' + clean(item[column]))
                    else:
                        conll_data.append(item[column])
            # Should probably check dimensions here
            conll_data = list(zip(*conll_data))
            outFile.write('\n'.join(sent_data) + '\n')
            for line in conll_data:
                outFile.write('\t'.join([str(x) for x in line]) + '\n')
            outFile.write('\n')
        outFile.close()     

def save(dataset, name):
    print('Saving ' + name + '...')
    dataset_parts = dataset.column_names
    if 'train' in dataset_parts:
        main_split = 'train'
    else:
        main_split = next(iter(dataset_parts))
    gold_columns = dataset_parts[main_split]

    # put idx in front
    for id_name in ['id', 'idx', 'index']:
        if id_name in gold_columns:
            del gold_columns[gold_columns.index(id_name)]
            gold_columns = [id_name] + gold_columns
    print('Found columns:')
    print(gold_columns)

    # We use the number of columns that are lists to identify
    # whether this is a sentence or word level annotated dataset
    num_lists = sum([type(val) == list for val in dataset[main_split][0].values()])
    if num_lists >= len(gold_columns)/2:
        save_word_level(dataset, gold_columns, name)
    else:
        save_sent_level(dataset, gold_columns, name)
    print()
    
    

def convert(name1, name2=None):
    if name2 != None:
        dataset = load_dataset(name1, name2)
        save(dataset, name1 + '-' + name2)
    else:
        # It is unclear to me how to get the list of subsets from 
        # the dataset library. So we use the trown exception, which
        # gives exactly this information.
        subsets = []
        try:
            dataset = load_dataset(name1)
            save(dataset, name1)
        except ValueError as e:
            subsets = str(e).split('\n')[1].replace('Please pick one among the available configs: ', '')
            subsets = ast.literal_eval(subsets)
            for subcorpus in subsets:
                dataset = load_dataset(name1, subcorpus)
                save(dataset, name1 + '-' + subcorpus)


if len(sys.argv) < 2:
    print('Usage: please provide the name of the dataset (and optionally the subset) you want to download. Examples:')
    print('python3 hf2conll.py glue')
    print('python3 hf2conll.py glue mrpc')
    print('\n')
    print('You can find the dataset names on https://huggingface.co/datasets')
    exit(1)

convert(*sys.argv[1:])
#convert('glue')
#convert('glue', 'mrpc')
#convert('conll2003')

