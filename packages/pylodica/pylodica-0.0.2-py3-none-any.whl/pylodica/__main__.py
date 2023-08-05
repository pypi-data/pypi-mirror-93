#!/usr/bin/env python 

import sys
import subprocess
import argparse
import time

def main(filepath):
    child = subprocess.run([sys.executable, filepath])
    return child

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='Python file to watch for changes.' )

    args = parser.parse_args()

    while True:
        try:
            child = main(args.file)
        except (Exception, KeyboardInterrupt):
            child.terminate()
            print('Execution halted')
            quit()