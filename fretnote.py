#!/usr/bin/python3

# copyright (c) 2019 andreas loeffler <al@exitzero.de>

import random
import signal

initial_timeout = 4

class TimeoutExpired(Exception):
    pass


class String:
    """A guitar string class"""

    def __init__(self, name, frets, notes):
        self.name = name
        self.frets = frets
        self.notes = notes
        self.fretnote = dict(zip(frets, notes))


    def randFret(self):
        return random.choice(self.frets)

    def fret2note(self, fret):
        return self.fretnote[fret]



def time_out(signum, frame):
    raise TimeoutExpired


def timed_input(t):
    signal.signal(signal.SIGALRM, time_out)
    signal.alarm(t) # t is seconds

    try:
        return input()
    finally:
        signal.alarm(0)



def learnNote(string, timeout):
    fret = string.randFret()
    note = string.fret2note(fret)
    answ = ""

    print("Enter note for %s-String on fret %2d: " % (string.name, fret), end="")

    try:
        answ = timed_input(timeout)
    except TimeoutExpired:
        print(' ... too late')
    else:
        print(' your answer %r' % answ)

    if (note.upper() == answ.upper()):
        print(" CORRECT!")
        return 1
    else:
        print(" WRONG! It's %r" % note)
        return 0


estring = String("E", (1,3,5,7,8,10,12), ('F','G','A','B','C','D','E'))
astring = String("A", (2,3,5,7,8,10,12), ('B','C','D','E','F','G','A'))
# ...
# todo: other strings, decrement timeout, run as long as answer is correct

points = 0
rounds = 20
for n in range(1, rounds):
    points += learnNote(random.choice((estring, astring)), initial_timeout)


print("points: %d out of %d" % (points, rounds))

