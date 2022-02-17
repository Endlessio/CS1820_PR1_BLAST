import sys
from collections import defaultdict
from itertools import product
import heapq

class Extension:
    def __init__(self, db, matrix, seed, X, S):
        self.db = db
        self.matrix = matrix
        self.seed_num = int(seed[3])
        self.seed_header = seed[:3]
        if self.seed_num > 0:
            self.seed_ele = seed[4:]
        else:
            raise Exception("seeds number equals 0")
        self.X = X
        self.S = S

        self.k = int(self.seed_header[1])

        self.res = []
        self.seen = set()
    

    def control(self, idx):
        cur_seed = self.seed_ele[idx]
        cur_seed_list = cur_seed.split()
        seq_num = int(cur_seed_list[1])

        cur_score = self.calculate(cur_seed_list)

        right_score, right_idx = self.extend(cur_seed_list, 1, cur_score)
        left_score, left_idx = self.extend(cur_seed_list, -1, cur_score)

        final_score = right_score + left_score - cur_score

        if final_score > self.S:
            seq2 = self.db[seq_num][left_idx[0]: right_idx[0]+1]
            seq1 = self.seed_header[0][left_idx[1]: right_idx[1]+1]

            check = (seq_num, left_idx[0], left_idx[1], seq1, seq2)
            if check not in self.seen:
                heapq.heappush(self.res, (final_score, len(seq1), -seq_num, -left_idx[0], -left_idx[1], seq1, seq2, cur_seed))
                self.seen.add(check)


    def calculate(self, cur_seed_list):
        db_idx = int(cur_seed_list[1])
        db_start_idx = int(cur_seed_list[3])
        q_start_idx = int(cur_seed_list[5])

        query = self.seed_header[0]
        db_seq = self.db[db_idx]
        score = 0

        for i in range(self.k):
            score += self.matrix[query[i+q_start_idx]][db_seq[i+db_start_idx]]

        return score

    def extend(self, cur_seed_list, dir, cur_score):
        db_idx = int(cur_seed_list[1])
        db_start_idx = int(cur_seed_list[3])
        q_start_idx = int(cur_seed_list[5])
        max_idx = None
        max_score = cur_score
        score = cur_score
        

        if dir == 1:
            db_start_idx += self.k
            q_start_idx += self.k
        else:
            db_start_idx -= 1
            q_start_idx -= 1

        query = self.seed_header[0]
        q_len = len(query)
        db_seq = self.db[db_idx]
        db_len = len(db_seq)


        while (0<=db_start_idx<db_len) and (0<=q_start_idx<q_len) and (max_score-score<=self.X):
            score += self.matrix[db_seq[db_start_idx]][query[q_start_idx]]
            if score > max_score:
                max_score = score
                max_idx = (db_start_idx, q_start_idx)

            db_start_idx += dir
            q_start_idx += dir

        if not max_idx:

            if dir == -1:
                max_idx = (int(cur_seed_list[3]), int(cur_seed_list[5]))
            else:
                max_idx = (int(cur_seed_list[3])+self.k-1, int(cur_seed_list[5])+self.k-1)

        return max_score, max_idx
    
    def print_output(self):
        for ele in self.seed_header:
            print(ele)
        print(len(self.res))

        print("-"*35)


        for ele in heapq.nlargest(len(self.res),self.res):
            print("Sequence %d Position %d Q-index %d" % (-ele[2], -ele[3], -ele[4]))
            print(ele[5])
            print(ele[6])
            print(ele[0])
            print("-"*35)
            



def preprocessing(argv):
    # variable
    db = []
    matrix = defaultdict(dict)
    seed = []
    X = None
    S = None

    # get db
    with open(argv[1]) as f:
        for line in f.readlines():
            db.append(line.strip())

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

    # get k
    with open(argv[3]) as f:
        for line in f.readlines():
            seed.append(line.strip())

    # get X
    X = int(argv[4])

    # get S
    S = int(argv[5])

    return db, matrix, seed, X, S

def main(argv):
    db, matrix, seed, X, S = preprocessing(argv)

    extension = Extension(db, matrix, seed, X, S)
    for idx in range(extension.seed_num):
        extension.control(idx)
    extension.print_output()


if __name__ == "__main__":
    main(sys.argv)
