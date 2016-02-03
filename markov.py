import os
import string

file_list = os.listdir("./corpora/comedies")
whole_string = ""

with open("./corpora/corpora.txt") as f:
    whole_string = f.read()
    print len(whole_string)

# model = dict.fromkeys(string.ascii_lowercase, dict.fromkeys(string.ascii_lowercase, 0))
model = {}
last = whole_string[0]

for char in whole_string[1:]:
    current = char

    if current not in model:
        model[current] = {}

    if current not in model[last]:
        model[last][current] = 0

    model[last][current] += 1
    # if char in string.ascii_uppercase:
    #     current = current.lower()

    # if current.lower() in model:
    #     model[last][current] += 1

    last = current

print model