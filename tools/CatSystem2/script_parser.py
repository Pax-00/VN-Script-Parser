import os
import re
import json
from library.regex import regex_dict

# Notes:
# Lines with multiple speakers such as Yumiko+Michiru+Amane: That's weird..., will be converted to Yumiko: That's weird...
# Since narration is anything without a speaker, there can occasionally be dialogue lines that are labeled as narration.

# Settings
input_extension = ".txt"
output_extension = ".txt"
input_folder = "raw"
out_folder_txt = "formatted_TXT"
out_folder_json = "formatted_JSON"

# Script processing
narrator_label = "Narration"  # Label narration lines
date_label = "Date"  # Label date lines, usually the first line

drop_japanese = False  # Drop ENTIRE FILES that have japanese in them
turn_drop_threshold = 3  # If a script has less than this number of turns, don't convert it to json
drop_dates = False
write_full_text = True  # Create text file with all dialogue lines, mostly for debugging regex

# Regex
# Replace patterns will be applied to the raw files. Order is important!
re_replace = {
    # Patterns to format dialogue lines
    "dates": [re.compile(r'^\*(\w+) (.{1,2}), (\d{4})', re.MULTILINE), f'{date_label}: *\\1 \\2, \\3'],  # Apply a label to date lines
    "speaker": [re.compile(r'^\*\*(.+)\*\*<br\/>\n', re.MULTILINE), '\\1: '],  # Format speaker lines, remove <br/> and merging with next dialogue
    "split_lines": [re.compile(r'\*?<br\/>\n\*?', re.MULTILINE), ' '],  # Merge lines that are split by <br/> to spaces
    "separator": [re.compile(r'\n\*\*\*\n\n', re.MULTILINE), ''],  # Remove *** and extra newlines, just used for separation?
    "file_labels": [re.compile(r'^\#.+$\n', re.MULTILINE), ''],  # Remove the file labels at the top of the file
    "narration": [re.compile(r'^\* ?', re.MULTILINE), f'{narrator_label}: *'],  # * indicates text displayed with no sprite, this is almost always narration
    "multiple_speakers": [re.compile(r"^(\w+)\+\w+(\+\w+)*", re.MULTILINE), r'\1'],  # For lines with multiple speakers, remove all but first speaker
    "backtick": [re.compile(r'\\`', re.MULTILINE), '\''],  # Backtick often used for apostrophes
    "escape_characters": [re.compile(r'\\', re.MULTILINE), ''],  # Clean up escape characters
    "empty_lines": [re.compile(r'\n\n', re.MULTILINE), '\n']
    # Final Cleanup
    # "japanese": [re.compile(r'[\u3040-\u30ff\u4e00-\u9fff]+', re.MULTILINE), ''],  # Shouldn't be needed?
}
re_search = {
    "japanese": re.compile(r'[\u3040-\u30ff\u4e00-\u9fff]+', re.MULTILINE),
}

root_path = os.path.dirname(os.path.abspath(__file__))


def clean_with_regex(content, file_path, vn_title):
    for key, value in re_replace.items():
        content = re.sub(value[0], value[1], content)
    # Load regex_dict based on game name
    if vn_title in regex_dict:
        for key, value in regex_dict[vn_title].items():
            # print(f'Applying {value[1]} to {vn_title}')
            content = re.sub(value[0], value[1], content)
    return content


def format_dialogue_lines(dialogue_lines):
    # Format dialogue lines further line by line if needed
    return dialogue_lines


def convert_to_json(dialogue_lines, file_path):
    # Convert dialogue lines to json
    dialogue_lines = dialogue_lines.splitlines()
    message_list = []
    speaker_list = []
    for line in dialogue_lines:
        # Every line should be formatted as speaker: dialogue, so simple split is fine. Anything without a : is dropped.
        split = line.split(': ', 1)
        if len(split) > 1:
            speaker, dialogue = line.split(': ', 1)
            if speaker is date_label and drop_dates:
                continue
            json_dict = {
                "speaker": speaker,
                "utterance": dialogue
            }
            message_list.append(json_dict)
            if speaker not in speaker_list:
                speaker_list.append(speaker)
    converted_json_path = os.path.join(root_path, out_folder_json, file_path.replace(input_extension, '.json'))
    if not os.path.exists(os.path.dirname(converted_json_path)):
        os.makedirs(os.path.dirname(converted_json_path))
    # Write json to file
    if len(message_list) > turn_drop_threshold:
        with open(converted_json_path, "w", encoding="utf-8") as json_file:
            json_schema = {
                "characters": speaker_list,
                "messages": message_list
            }
            json.dump(json_schema, json_file, ensure_ascii=False, indent=4)


def write_full_text_file(processed_vn_list):
    for key, value in processed_vn_list.items():
        with open(f'./{out_folder_txt}/[Script]{key}.txt', "w", encoding="utf-8") as dialogue_file:
            dialogue_file.write(value)
            convert_to_json(value, f'./[Script]{key}.json')


# Get paths to each script file in current directory and subdirectories
script_files = []
for root, dirs, filenames in os.walk(f'./{input_folder}'):
    for filename in filenames:
        if filename.endswith(".txt"):
            script_files.append(os.path.join(root, filename))

processed_vn_list = {}
# Convert each script file to json as well as a formatted txt file (for regex debugging)
for f in script_files:
    with open(f, "r", encoding="utf-8") as file:
        content = file.read()
        # Only process English files
        # if (not drop_japanese or not re_search['japanese'].search(content)):
        # Get second folder from top level of f. This is the vn name.
        vn_title = f.split(os.sep)[1]
        if vn_title not in processed_vn_list:
            processed_vn_list[vn_title] = ''
        clean_content = clean_with_regex(content, f, vn_title)
        content = clean_content.splitlines(True)
        dialogue_lines = format_dialogue_lines(content)
        file_path = f.replace(input_extension, output_extension).replace(f'./{input_folder}\\', '')
        converted_file_path = os.path.join(root_path, out_folder_txt, file_path)
        if not os.path.exists(os.path.dirname(converted_file_path)):
            os.makedirs(os.path.dirname(converted_file_path))
        # Write formatted dialogue lines to txt and json files
        with open(converted_file_path, "w", encoding="utf-8") as dialogue_file:
            dialogue_lines = ''.join(dialogue_lines)
            dialogue_file.write(dialogue_lines)
            convert_to_json(dialogue_lines, file_path)
            print('Finished', converted_file_path)
            processed_vn_list[vn_title] += dialogue_lines

if write_full_text:
    write_full_text_file(processed_vn_list)
