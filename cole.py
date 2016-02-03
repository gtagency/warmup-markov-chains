model = {} #dict

firstTime = True
with open("./corpora/corpora.txt", encoding="utf-16") as f:
    for char in f.read():
        if char not in model:
            model[char] = {} # init nested dict
        if not firstTime:
            if char not in model[lastChar]:
                model[lastChar][char] = 0
            model[lastChar][char] += 1
        else:
            firstTime = False
        lastChar = char
