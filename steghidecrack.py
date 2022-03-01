#!/usr/bin/python3
import os
import argparse
from multiprocessing.pool import ThreadPool as Pool


# define worker function before a Pool is instantiated
def worker(line, filename, remaining):
    try:
        output = os.system("steghide extract -sf " + filename.strip() + " -p '" + line.strip() + "'")
        print('output ', output, ' line ', line)
        if "could not extract" not in output:
            print("FOUND!!!!!!=> " + line)
            print(output)
    except:
        pass
    print("Remainning : ", str(remaining))


def get_wordlist(wordlistname):
    with open(wordlistname, "r", encoding='UTF-8', errors='ignore') as myfile:
        return myfile.readlines()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", help="File name of image")
    parser.add_argument("--wordlist", help="dictionary path")
    parser.add_argument("--threads", help="Number of threads ", type=int)

    args = parser.parse_args()

    wordlist = get_wordlist(args.wordlist)
    length = len(wordlist)
    i = 1;
    pool_size = args.threads
    pool = Pool(pool_size)
    for line in wordlist:
        remaining = length - i
        pool.apply_async(worker, (line, args.filename, remaining))
        i = i + 1
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
