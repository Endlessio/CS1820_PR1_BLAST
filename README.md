## Program File Tree Structure and Auxiliary Files Introduction
```bash
├── databases
│   ├── P4db.txt
│   ├── db1.txt
│   └── db2.txt
├── matrices
│   ├── pam250.m
│   └── unitary.m
├── src
│   ├── extension.py
│   ├── local_alignment.py
│   ├── random.txt # generated random sequences
│   ├── statistics.txt # required statistics.txt
│   ├── seeding.py
│   ├── seeds1.txt # output seeds from seeding.sh, same as the test exm in instruction
│   ├── seeds2.txt # output seeds from seeding.sh, same as the test exm in instruction
│   └── statistics.py
├── test_cases
│   ├── extension
│   │   ├── seeds1.txt
│   │   └── seeds2.txt
│   ├── local
│   │   ├── localDNA1.txt
│   │   ├── localDNA2.txt
│   │   └── localProt1.txt
│   └── seeding
│       ├── query1.txt
│       └── query2.txt
├── extension.sh
├── local.sh
├── seeding.sh
└── structure.tree # use to generate and keep track file tree structure
```







## Shell Command

When run any command, make sure you are under the corresponding directory. 

Specifically, here, you need to under the root dir.



### Local Alignment

```bash
sh local.sh <seq.txt> <matrix.m> <gap_penalty>
-------------------------------------------------------------
exm: sh local.sh ./test_cases/local/localProt1.txt ./matrices/pam250.m -1
```



### Seeding

```bash
sh seeding.sh <db.txt> <query.txt> <matrix.m> <k> <T>
-------------------------------------------------------------
exm: sh seeding.sh ./databases/db2.txt ./test_cases/seeding/query2.txt ./matrices/pam250.m 3 3
```



### Extension

```bash
sh extension.sh <db.txt> <matrix.m> <seeds.txt> <X> <S>
-------------------------------------------------------------
sh extension.sh ./databases/db1.txt ./matrices/pam250.m ./src/seeds1.txt 2 7
```



### Statistics

```bash
sh statistics.sh <db.txt> <matrix.m>
-------------------------------------------------------------
sh statistics.sh ./databases/P4db.txt ./matrices/pam250.m
```





## Implementation

### Local Alignment

Implemented the Smith-Waterman Local Alignment Algorithm with dynamic programming.

- Time Complexity: $O(n^2)$
- Space Complexity: $O(n^2)$

In core algorithm, two 2d-array are constructed to simulate the matrices, one matrix records the score to track max score, the other matrix records the direction to track the alignment sequence for output.

Notice, though the default input seq.txt assumes only containing two sequences for alignments, this prorgam generalizes to support multiple sequences file with fomat with $seq\_i\_j$, where i is the alignment pair number, j is the sequence number in one alignment pair. This kind of generalization makes the alignments of random sequences in part 4 be easier:

```
seq1-1
seq1-2
seq2-1
seq2-2
...
seqn-1
seqn-2
```

To apply alignments for different pairs, just change the idx number (default is 0) in the main function when call the local_alignment method. 

For example, set it to 4 means apply alignment for the fifth pair:

![截屏2022-02-15 下午6.20.31](/Users/endlessio/Library/Application Support/typora-user-images/截屏2022-02-15 下午6.20.31.png)



### Seeding

The seeding phase of the BLAST algorithm.

With n be query length, m be database size, k be k-mer size, T be threshold:

- Time Complexity: $O((n-k)20^kk)$
- Space Complexity: $min(O(20^k),\ O(m-k))$

The algorithm can be divided into the following steps:

![截屏2022-02-15 下午6.30.29](/Users/endlessio/Library/Application Support/typora-user-images/截屏2022-02-15 下午6.30.29.png)

1. find_alpha_kmer: form a list structure contains all the possible alpha k-mer
2. find _query_kmer: form a python dict structure (hashmap) with key be distinct possible k-mer string from query and value be the start index list of the specific k-mer string.
3. find_db_kmer: form a python dict structure (hashmap) with key be db sequence index, value be a python dict structure (hashmap) with key be distinct possible k-mer string from specific db sequence, value be the start index list of the specific k-mer string.
4. score_cal: calculate the score for all possible seeds by comparing k-mer from query and alphabet
5. find_seed_pos: check for whether the seeds from step 4 appears in db sequences, if yes, store the start index
6. print_output: print output with required format



### Extension

The extension phase of the BLAST algorithm.

With seeds number be $e$, 

- Time Complexity: $O(e*n)$
- Space Complexity: $O(e*n)$

The algorithm can be divided into the following steps:

Iterating each seed:

1. calculate the current score
2. do right extension, return max score and corresponding index
3. do left extension, return max score and corresponding index
4. calculate final score, if it has not been seen and exceed the threshold, append to result.

![截屏2022-02-15 下午6.39.52](/Users/endlessio/Library/Application Support/typora-user-images/截屏2022-02-15 下午6.39.52.png)

Notice, the following data structure can be highlighted:

1. self.seen: python set strucure to check whether the current result (in the structure of tuple (db_seq_num, start_index_query, start_index_db, alignments)) be seen.
2. self.res: store the final res with heap struture with element as tuple: (final_score, len(seq1), -seq_num, -db_start_index, -query_start_index, seq1, seq2, cur_seed), so that the res can be popped in certain order by final score, then length, then smaller db_seq_num first, then smaller query_seq_num first. Since python heapq structure is a min heap, remember to add negative sign on the certain index.



### Statistics

1. calculate the amino acid frequency with python build-in Counter library.
2. generate weighted random sequence with random.choices library
3. inherit the LocalAlignment class from local_alignment.py, and apply local alignment on the genereated random sequence.





## Bug Reporting

Currently no identifying bugs

