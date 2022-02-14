import sys
from collections import defaultdict, Counter

from local_alignment import LocalAlignment
import random
from random import randint
import numpy as np
import scipy.io as sio

class Statistics(LocalAlignment):
    def __init__(self, db, matrix, imin, imax):
        self.db = db
        self.matrix = matrix

        self.str_db = ""
        self.freq_dict = None

        self.random_seq = []
        self.imin = imin
        self.imax = imax
    
    def freq(self):
        for ele in self.db:
            self.str_db += ele
        self.freq_dict = Counter(self.str_db)
        print(self.freq_dict)

    
    def generate_random(self, num):
        sample_list = list(self.freq_dict.keys())
        i_weights = [self.freq_dict[ele] for ele in sample_list]
        with open('random.txt', 'w') as f:
            for _ in range(num):
                cur_random = random.choices(sample_list, weights=i_weights, k=randint(self.imin, self.imax))
                cur_random = "".join(i for i in cur_random)
                self.random_seq.append(cur_random)
                f.write(cur_random)
                f.write('\n')
        # print(len(self.random_seq))



    def print_output(self):
        pass


def preprocessing(argv):
    # variable
    matrix = defaultdict(dict)
    db = []

    imin = float("inf")
    imax = float("-inf")

    # get db
    with open(argv[1]) as f:
        for line in f.readlines():
            line = line.strip()
            imin = min(len(line), imin)
            imax = max(len(line), imax)
            db.append(line)

    # get matrix
    with open(argv[2]) as f:
        chars = f.readline().strip().split()[1:]
        temp = []
        for _ in range(len(chars)):
            temp.append(f.readline()[1:].strip().split())
        row = len(temp)
        col = len(temp[0])
        for i in range(row):
            for j in range(col):
                matrix[chars[i]][chars[j]] = int(temp[i][j])
        

    return db, matrix, imin, imax

def main(argv):
    num = 100
    db, matrix, imin, imax = preprocessing(argv)

    stat = Statistics(db, matrix, imin, imax)
    stat.freq()
    
    stat.generate_random(num)

    align = LocalAlignment(stat.random_seq, matrix, float("-inf"))
    assert stat.random_seq == align.seq

    for i in range(0,num,2):     
        align.local_alignment(i)
        print(i, align.imax)

    






if __name__ == "__main__":
    main(sys.argv)
