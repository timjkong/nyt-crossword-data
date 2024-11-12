import argparse
import json
import os


def process_data(data):
    data = data["body"][0]
    cells = data["cells"]
    clues = [clue["text"][0]["plain"] for clue in data["clues"]]
    words = [[] for _ in range(len(clues))]
    for cell in cells:
        if "clues" not in cell:
            continue
        for i in cell["clues"]:
            words[i].append(cell["answer"])
    return [{
        "word": ''.join(word).lower(),
        "clue": clue.lower()
    } for word, clue in zip(words, clues)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Transform raw crossword data into word-to-clue pairs and saves the "
                                                 "data to a specified jsonl file")
    parser.add_argument("input_dir", type=str, help="Directory containing raw data input")
    parser.add_argument("output_path", type=str, help="Output path of transformed data")
    args = parser.parse_args()
    if not args.output_path.endswith('.jsonl'):
        parser.error("output_path should be a path to a .jsonl file")

    output_data = []
    for filename in os.listdir(args.input_dir):
        file_path = os.path.join(args.input_dir, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                raw_data = json.load(file)
                output_data.extend(process_data(raw_data))
    jsonl_data = '\n'.join(json.dumps(entry) for entry in output_data) + '\n'
    with open(args.output_path, 'w') as output_file:
        output_file.write(jsonl_data)