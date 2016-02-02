import numpy as np
import random
from collections import defaultdict
def text(file):
    with open (file, "r") as f:
        t = f.read().replace('\n', ' ')
    return t

class Markov:
    def __init__(self, text, n = 1, replace_chars = [["."],[" ."]]):
        self.replacements = replace_chars
        self.order = n
        self.raw = text
        self.chain(text)
        
    def chain(self, text):
        self.states = defaultdict(list)
        words = self.replace(text,*self.replacements).split()
        for x in range(0, len(words)-self.order):
            self.states[tuple(words[x:x+self.order])].append(words[x+self.order])
        self.states[tuple(words[-self.order:])].append(words[0])
    def replace(self,string, olds, news):
        for o, n in zip(olds, news):
            string = string.replace(o, n)
        return string

    def getnext(self, seed):
        return random.choice(self.states[seed])
        
    def generate(self, sentences = 1
,                 _seed_state = lambda x : random.choice([a for a in x.states if a[-1]=="."]),
                 break_state = ".",
                 join_state = " "):
        seed_state = _seed_state(self)
        seed_state = tuple(seed_state)
        out = [x for x in seed_state]
        for _ in range(sentences):
            state = tuple(out[-self.order:])        
            while True:
                out.append(self.getnext(state))
                state = tuple(out[-self.order:])
                if state[-1]==break_state:
                    break
        return self.replace(join_state.join(out[self.order:]),
                            *self.replacements[::-1])
    def debug_states(self):
        for state, states in zip(self.states, self.states.values()):
            print(" ".join([x for x in state]) + "  :  " + str(states))
    def info(self):
        print("States: " + str(len(self.states)))
        print("Avg. transitions: "
              + str(sum([len(q) for q in self.states.values()])/len(self.states)))
    def __str__(self):
        return self.generate()
    def add(self, other):
        if self.order != other.order:
            print("Cannot add chain of order: " + str(self.order) + " with chain of order: " + str(other.order))
            return
        for x in other.states:
            self.states[x]+=other.states[x]
    def compare(self, other):
        common = set(self.states.keys()) & set(other.states.keys())
        print(common)
        print(len(common))
print("Loaded!")
