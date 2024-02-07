# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 18:56:05 2023

@author: Meenakshi Pillai
"""
#Import the library needed for taking command line arguments
import sys

###Define three functions: 1. Read fasta file 2. Align sequences to show the dash and space 3. Main fnctn
#1. Define the read fasts fnctn to take the file path from the command line
def read_fasta(file_path):
    sequences = {}
    current_sequence = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('>'):
                current_sequence = line[1:]
                sequences[current_sequence] = ''
            else:
                sequences[current_sequence] += line

    return sequences


#2. Define two functions for processing the dash and space output and to print the sequences and output together
def align_sequences(sequences):
    aligned_sequences = list(sequences.values())
    length = len(aligned_sequences[0])

    for i in range(1, len(aligned_sequences)):
        for j in range(length):
            if aligned_sequences[0][j] == aligned_sequences[i][j]:
                aligned_sequences[0] = aligned_sequences[0][:j] + '|' + aligned_sequences[0][j + 1:]
            else:
                aligned_sequences[0] = aligned_sequences[0][:j] + ' ' + aligned_sequences[0][j + 1:]

    return aligned_sequences[0]
def print_aligned_sequences(sequences, aligned_result):
        seq1, seq2 = list(sequences.values())
        print(f'{seq1}')
        print(f'{aligned_result}')
        print(f'{seq2}')
        
#3. Define the main function
def main():
    if len(sys.argv) != 2:
        print("Usage: python fasta_aligner.py <path_to_aligned_fna>")
        sys.exit(1)

    file_path = sys.argv[1] #use the argv command to take input from the command line

    try:
        sequences = read_fasta(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        sys.exit(1)

    aligned_result = align_sequences(sequences)
    print_aligned_sequences(sequences,aligned_result)

if __name__ == "__main__":
    main()
