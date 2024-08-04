import json
import glob
import os
import argparse

parser = argparse.ArgumentParser(description='Process some files.')

parser.add_argument('--input_path', type=str, required=True, help='Path to the input CSV file')
parser.add_argument('--output_path', type=str, required=True, help='Path to the output JSON file')

args = parser.parse_args()

input_path = args.input_path
output_path = args.output_path

with open(input_path) as jsonfile:
    data = json.load(jsonfile)

for key, split in data.items():
    for idx, ele in enumerate(split):
        image_path = os.path.join('images', ele['id'])
        ele['image'] = glob.glob(os.path.join(image_path, '*.png'))
        ele["system_prompt"] =  "You are a helpful assistant."
        ele["conversations"] = [
            {
                "from": "human",
                "value": "<image>"*len(ele['image']) +  "Write a report about the images."
            },
            {
                "from": "gpt",
                "value": json.dumps(ele['report'])
            },
        ]
        del ele['report']
        data[key][idx] = ele
    

with open(os.path.join(output_path, 'annotation_quiz_all_train.json'), 'w') as jsonfile:
    json.dump(data['train'], jsonfile)

with open(os.path.join(output_path,'annotation_quiz_all_val.json'), 'w') as jsonfile:
    json.dump(data['val'], jsonfile)

with open(os.path.join(output_path, 'annotation_quiz_all_test.json'), 'w') as jsonfile:
    json.dump(data['test'], jsonfile)