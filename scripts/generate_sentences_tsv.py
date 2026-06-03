#!./.venv/bin/python
import zipfile
import sys
import os
import argparse
import io
import re


def process_file(file_stream, filename):
    sentences = []
    curr_sentence = ""
    year = None
    genres = None
    
    for line in file_stream:
        line = line.lstrip()

        try:
            tag = re.search(r'<(?:\/)?([a-zA-Z0-9]+)', line).group(1)
        except Exception as e:
            continue


        is_closing = line[1] == "/"

        if tag == "w":
            content = line[line.find('>') + 1 : line.rfind('</')]

            if content in ["?", "!", ".", ",", ":", ";", "-", "--"]:
                curr_sentence += content
            else:
                curr_sentence += " " + content
        elif is_closing and tag == "s":
            if curr_sentence:
                sentences.append(curr_sentence.strip())
                curr_sentence = ""
        
        elif tag == "year":
            year = line[line.find('>') + 1 : line.rfind('</')]
        
        elif tag == "genre":
            genres = line[line.find('>') + 1 : line.rfind('</')]

    if genres == None or "," in genres or genres == "N/A": # TODO: Removing multigenre - for easier training
        return

    if year == None:
        # Path looks like this: OpenSubtitles/xml/cs/1962/54949/1953709627.xml
        year = filename.split("/")[3]

    for sentence in sentences:
        print("\t".join([genres,year,sentence]), file=sys.stdout)


def process_zip(zip_path):

    if not os.path.exists(zip_path):
        print(f"Error: File {zip_path} not found.", file=sys.stderr)
        return

    with zipfile.ZipFile(zip_path, 'r') as z:
        for name in z.namelist():
            if name.endswith('/') or not name.lower().endswith('.xml'):
                continue
            
            try:
                with z.open(name) as f: 
                    text_stream = io.TextIOWrapper(f, encoding='utf-8')
                    process_file(text_stream, name)
            
            except Exception as e:
                print(f"Error processing {name}: {e}", file=sys.stderr)
                continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a specific ZIP file.")
    parser.add_argument("zip_path", help="Path to the ZIP file")
    args = parser.parse_args()

    process_zip(args.zip_path)