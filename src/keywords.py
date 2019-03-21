import re
import sys

def extract_keywords(filename,config):
    text = ""
    searchable = ""
    try:
        with open(filename,'r') as f:
            text = f.read()
        searchable = text.lower()
    except Exception as e:
        return e

    results = {}
    if config['text']:
        results['pdf_text'] = text
    for word in config['keywords']:
        results[word] = []
        if config['snippets']:
            for sentence in re.split(r'\.|\n\n',searchable):
                if word.lower() in sentence:
                    results[word].append(sentence)
        else:
            occurences = re.findall(word.lower(),searchable)
            results[word] = len(occurences)
    
    return results