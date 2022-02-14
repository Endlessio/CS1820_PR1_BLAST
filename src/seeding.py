import sys
from collections import defaultdict
from itertools import product
import heapq

class Seeding:
    def __init__(self, db, query, matrix, k, T):
        self.db = db
        self.query = query
        self.matrix = matrix
        self.k = k
        self.T = T

        self.query_kmer = defaultdict(list)
        self.alpha_kmer = []
        self.db_kmer = defaultdict(lambda: defaultdict(list))

        self.seeds = defaultdict(set)

        self.res = []
    
    def find_db_kmer(self):
        for idx, ele in enumerate(self.db):
            if len(ele) < self.k:
                continue
            else:
                for i in range(len(ele)-self.k+1):
                    cur = ele[i:i+self.k]
                    self.db_kmer[idx][cur].append(i)

    def find_query_kmer(self):
        for q in self.query:
            length = len(q)
            assert length >= self.k

            for i in range(length-self.k+1):
                cur = q[i:i+self.k]
                self.query_kmer[cur].append(i)


    def find_alpha_kmer(self):
        chars = self.matrix.keys()
        self.alpha_kmer = list(product((chars), repeat = self.k))
        for idx in range(len(self.alpha_kmer)):
            self.alpha_kmer[idx] = "".join(list(self.alpha_kmer[idx]))


    def score_cal(self):
        def compare(q_mer, a_mer):
            assert len(q_mer) == len(a_mer), "ERROR: len(q_mer) != len(a_mer)"
            length = len(q_mer)
            score = 0
            for i in range(length):
                score += self.matrix[q_mer[i]][a_mer[i]]
            return score > self.T

        for q_mer in self.query_kmer.keys():
            for a_idx, a_mer in enumerate(self.alpha_kmer):
                if compare(q_mer, a_mer):
                    self.seeds[q_mer].add(a_idx)


    def find_seed_pos(self):
        def compare(a_mer, db_seq_dict):
            if a_mer in db_seq_dict:
                return db_seq_dict[a_mer]
            return False

        for q_mer, a_mer_set in self.seeds.items():
            for a_mer_idx in a_mer_set:
                for db_seq_idx in range(len(self.db)):
                    res = compare(self.alpha_kmer[a_mer_idx], self.db_kmer[db_seq_idx])
                    if res:
                        for db_idx in res:
                            for q_idx in self.query_kmer[q_mer]:
                                heapq.heappush(self.res, (db_seq_idx, db_idx, q_idx))

    def print_output(self):
        for query in self.query:
            print(query)
        print(self.k)
        print(self.T)
        print(len(self.res))
        while self.res:
            idx1, idx2, idx3 = heapq.heappop(self.res)
            print("Sequence %d Position %d Q-index %d" % (idx1, idx2, idx3))

def preprocessing(argv):
    # variable
    db = []
    query = []
    matrix = defaultdict(dict)
    k = None
    T = None

    # get db
    with open(argv[1]) as f:
        for line in f.readlines():
            db.append(line.strip())

    # get query
    with open(argv[2]) as f:
        query.append(f.readline().strip())

    # get matrix
    with open(argv[3]) as f:
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
    k = int(argv[4])
    assert k>0, "ERROR: k smaller than 0"

    # get T
    T = int(argv[5])

    return db, query, matrix, k, T

def main(argv):
    db, query, matrix, k, T = preprocessing(argv)

    seed = Seeding(db, query, matrix, k, T)
    seed.find_alpha_kmer()
    seed.find_query_kmer()
    seed.find_db_kmer()
    seed.score_cal()
    seed.find_seed_pos()
    seed.print_output()


if __name__ == "__main__":
    main(sys.argv)
