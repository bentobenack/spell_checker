# Spell Checker

# How to execute: python spellchecker.py words_en.txt dictionary_en.txt

# Imports
import csv
import sys
import time
import random
import numpy as np

# Global Constants
deletion_cost = 1
insertion_cost = 1
substitution_cost = 1

# Find the nearest word
# s = word
# dictionary = dictionary of words
def find_closest_word(s, dictionary):
  distances = []
  for i in range(0, len(dictionary)):
    # Calculate the levenshtein distance between s and dictionary[i]
    distance = levenshtein_distance(s, dictionary[i], deletion_cost, insertion_cost, substitution_cost)

    if distance == 0:
      return dictionary[i]
    distances.append(distance)
  return dictionary[distances.index(min(distances))]


# Levenshtein Distance
# s = word 1; 
# t = word 2
# m = length of s; 
# n = length of t
# The values of deletion_cost, insertion_cost, substitution_cost are fixed

# Function for calculating the Levenshtein distance
def levenshtein_distance(s, t, deletion_cost, insertion_cost, substitution_cost):
  first_len, second_len = len(s), len(t)
  if s == t:
    return 0

  if first_len > second_len:
    s, t = t, s
    first_len, second_len = second_len, first_len

  if second_len == 0:
    return first_len

  # Initializing the matrix with zeros
  d = [[0] * second_len for x in range(first_len)]

  # Setting values ​​for the first row and first column
  for i in range(0, first_len):
    d[i][0] = i * deletion_cost
  for j in range(0, second_len):
    d[0][j] = j * insertion_cost

  for j in range(1, second_len):
    for i in range(1, first_len):
      if s[i] == t[j]:
        d[i][j] = d[i - 1][j - 1]
      else:
        d[i][j] = min(d[i - 1][j] + deletion_cost, d[i][j - 1] + insertion_cost, d[i - 1][j - 1] + substitution_cost) + 1

  return d[first_len - 1][second_len - 1]

# Error Average
# Comparison between the typo and the real word
def measure_error(typos, true_words, dictionary):
  error_count = 0
  start = time.time()
  for i in range(0, len(typos)):
    closest_word = find_closest_word(typos[i], dictionary)
    true_word = true_words[i]
    if ',' in true_word:
      true_word_arr = true_word.split(',')
      has_match = False
      for x in range(0, len(true_word_arr)):
        word = true_word_arr[x].strip()
        if closest_word == word:
          has_match = True 
          break
      if has_match:
        print ('Word without typo: ' + closest_word)
      else:
        print ('Typing error detected: ' + typos[i] + '. Correct word: ' + true_word)
        error_count = error_count + 1
    elif ' ' in true_word:
      true_word_arr = true_word.split(' ')
      has_match = False
      for x in range(0, len(true_word_arr)):
        word = true_word_arr[x].strip()
        if closest_word == word:
          has_match = True 
          break
      if has_match:
        print ('Word without typo: ' + closest_word)
      else:
        print ('Typing error detected: ' + typos[i] + '. Correct word: ' + true_word)
        error_count = error_count + 1

    else:
      if closest_word == true_word:
        print ('Word without typo: ' + closest_word)
      else:
        print ('Typing error detected: ' + typos[i] + '. Correct word: ' + true_word)
        error_count = error_count + 1
  print ('Error rate of ' + str(float( ) / len(typos)))
  print ('Calculation time was ' + str(time.time() - start) + ' seconds')


def main():
  args = sys.argv[1:]

  if len(args) != 2:
    print ('Please type: python spellcheck.py <file to be corrected> <word dictionary>')
    sys.exit(1)

  filename = args[0]
  dict_word_list = args[1]

  words = [] 
  typos = []
  true_words = []
  
  with open(dict_word_list, 'r') as word_dict_file:
    words = [line.strip() for line in word_dict_file]

  with open(filename, 'r') as target_file:
    for line in target_file:
      typos.append(line.split('\t')[0].strip())
      true_words.append(line.split('\t')[1].strip())

  random_indices = random.sample(range(1, len(typos)), 100)
  random_typos = [ typos[i] for i in random_indices ]
  random_true_words = [ true_words[i] for i in random_indices ]

  # By default, the error rate is calculated on a sample of 100 words.
  # If you want to calculate the error rate in the entire dataset, comment this line below and uncomment the next one
  measure_error(random_typos, random_true_words, words)
  #measure_error(typos, true_words, words)


if __name__ == '__main__':
  main()
