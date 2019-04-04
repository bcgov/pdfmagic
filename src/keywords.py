import re
import sys

def extract_keywords(filename,config):
    text = ""
    searchable = ""

    with open(filename,'r') as f:
        text = f.read()
    
    # print(text)
    searchable = text.lower()

    results = {}
    if config['text']:
        results['pdf_text'] = text
    for word in config['keywords']:
        results[word] = []

        ## Snippets mode returns snippets of text around the keywor
        if config['snippets']:
            for sentence in re.split(r'\.|\n\n',searchable):
                if word.lower() in sentence:
                    results[word].append(sentence)

        ## Normal mode returns the wordcount of each word
        else:
            occurences = re.findall(word.lower(),searchable)
            results[word] = len(occurences)
    
    return results