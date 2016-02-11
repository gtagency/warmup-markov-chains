import string
import collections
import os

class Polo(object):

    def __init__(self, n, order):
        self.n = n
        self.ngrams = dict()
        self.order = order

    def tokenize(self, text):
        import re
        re.sub('^\x00\x08\x0B\x0C\x0E-\x1F', "", text)
        if self.order == 1:
            return text.split(" ")
        else:
            return text

    def ngrammify(self, text):
        words = self.tokenize(text)
        for i in range(len(words) - self.n):
            ngram = tuple(words[i:i+self.n])
            after = words[i+self.n]
            if ngram in self.ngrams:
                self.ngrams[ngram].append(after)
            else:
                self.ngrams[ngram] = [after]

class Marco(object):

    def __init__(self, n, maximum, order):
        self.n = n
        self.maximum = maximum
        self.ngram = Polo(n, order)
        self.order = order

    def populate(self, text):
        self.ngram.ngrammify(text)

    def generate(self):
        from random import choice
        import re

        current = choice(list(self.ngram.ngrams.keys()))
        output = list(current)
        output_str = ""
        
        for i in range(self.maximum):
            if current in self.ngram.ngrams:
                possible_next = self.ngram.ngrams[current]
                next = choice(possible_next)
                output.append(next)
                current = tuple(output[-self.n:])
            else:
                break
        output_str = self.concatenate(output)
        output_str = '.'.join(output_str.split('.')[1:])
        output_str = output_str.strip()
        #output_str = re.sub("^\\s+[A-Za-z,;'\"\\s]+[.\\s?\\s!\\s]$", "", output_str)
        return output_str

    def concatenate(self, li):
        import re
        output = ""
        for token in li:
            #re.sub('[^a-zA-Z\d\s:]', "", token)
            if self.order == 1:
                output += " " + token
            else:
                output += "" + token
        return output

def main():
    with open('./corpora/agency.txt', encoding='utf-8') as f:
        all_text = f.read()
    marco = Marco(1, 200, 1)
    marco.populate(all_text)
    output_str = marco.generate()
    print(output_str)
if __name__ == "__main__": main()
