import sys
import constant_strings as cs
import os,glob
import unicodecsv as csv
import use_word2vec as w2v
import numpy as np
import embed_util as emb
import numpy
import re
from collections import defaultdict

def create_matrix(date,period,word_list):
	# 1. Load word2vec model based on date and period inputs
	# 2. For each word in word_list, query into model to obtain vector (if word not in model's vocab, take [0]*100 vector)
	# 3. Append all vectors to form the word embedding matrix
	# 4. Return matrix
	model = w2v.load_word2vec(date,period)
	mat = []
	for (word,c) in word_list:
		corr_word = word
		if corr_word in model.vocab:
			mat.append(model[corr_word])
		else:
			if c == 'i':
				print "Not found!",corr_word
				print "Shouldn't happen"
				raw_input()
			else:
				mat.append([0]*100)
	numpy_mat = np.array(mat)
	return numpy_mat

def realign_models_all(period):
	# 1. Find the years for which the models are present, create the year_list and sort it
	# 2. Read the intersection file and newly added file and store all words in files in a word_list; also store the year the new words first occur in, in word_year
	# 3. For each time period, call create_matrix to create the word embedding
	# 4. Further call reorient() to realign the embedding of each time period (except first) wrt the previous time period's embedding
	# 5. Store all realigned embeddings in order in aligned_matrices list
	# 6. For each word in word_list, calculate the two scores (pairwise and last-first) from the aligned_matrices list
	# 7. Store scores in i_score_diff_all and i_score_diff_first_last, for intersection words, and n_score_diff_all and n_score_diff_first_last for newly added words
	# 8. Sort all score lists and write into separate files to hold the most changed words in sorted order

	if period == "five":
		path = cs.path_models_five
		postfix = cs.postfix_models_five
		tf_path = cs.path_tf_five
		path_final_output = cs.path_final_five
	else:
		path = cs.path_models_decade
		postfix = cs.postfix_models_decade
		tf_path = cs.path_tf_decade
		path_final_output = cs.path_final_decade
	os.chdir(path)
	year_list = []
	print "Finding list of time periods.."
	for file in glob.glob("*"+postfix):
		year = file.split("_")[0]
		year_list.append(year)
	year_list = sorted(year_list)
	print "TIME PERIODS: ",year_list
	os.chdir(os.path.join("..",".."))
	
	print "Finding word list.."
	word_list = []
	with open(os.path.join(tf_path,cs.intersection_file),"rb") as f:
		for rec in csv.reader(f, delimiter=',', lineterminator='\n'):
			word = list(rec)[0]
			word_list.append((word,"i"))
	diff_by_year = defaultdict(list)
	word_year = {}
	with open(os.path.join(tf_path,cs.newly_added),"rb") as f:
		for rec in csv.reader(f, delimiter=',', lineterminator='\n'):
			word = rec[0]
			score = int(rec[1])
			year = rec[2]
			diff_by_year[year].append((word,score))
	for year in diff_by_year:
		diff_by_year[year] = sorted(diff_by_year[year], key = lambda x : x[1], reverse = True)[:100]
	for year_str in diff_by_year:
		for (word,score) in diff_by_year[year_str]:
			m = re.search('(.*)_TF_five.csv',year_str)
			year = m.group(1)
			word_year[word] = year
			word_list.append((word,"n"))
	print "LEN WORDLIST: ",len(word_list)

	print "Aligning matrices.."
	aligned_matrices = []
	first = create_matrix(year_list[0],period,word_list)
	aligned_matrices.append(first)
	for sec in range(1,len(year_list)):
		second = create_matrix(year_list[sec],period,word_list)
		first, r = emb.reorient(first,second)
		aligned_matrices.append(first)
	print "ALIGNED LEN: ",len(aligned_matrices)
	print "EACH MATRIX IN ALIGNED SHAPE: ",aligned_matrices[0].shape

	print "Start scoring.."
	i_score_diff_all = []
	i_score_diff_first_last = []
	n_score_diff_all = []
	n_score_diff_first_last = []
	for word_index in range(len(word_list)):
		score = 0
		i = 0
		word = word_list[word_index][0]
		category = word_list[word_index][1]
		year = '1950-01-01' if category == 'i' else word_year[word]
		y_i = year_list.index(year)
		for j in range(1,len(aligned_matrices)):
			pair_diff = np.linalg.norm(aligned_matrices[j][word_index]-aligned_matrices[i][word_index])
			if category == "i":
				score+= pair_diff
			else:
				if i >= y_i:
					score+= pair_diff
			i+=1
		if category == "i":
			i_score_diff_all.append((word_index,score))
		else:
			n_score_diff_all.append((year,word_index,score))
		score2 = 0
		if category == "i":
			score2 = np.linalg.norm(aligned_matrices[len(aligned_matrices)-1][word_index]-aligned_matrices[0][word_index])
			i_score_diff_first_last.append((word_index,score2))
		else:
			score2 = np.linalg.norm(aligned_matrices[len(aligned_matrices)-1][word_index]-aligned_matrices[y_i][word_index])
			n_score_diff_first_last.append((year,word_index,score2))
		if word_index%100 == 0:
			print "At: ",word_index
	print "Scoring done.\nStart sorting.."
	i_sorted_scores_all = sorted(i_score_diff_all, key = lambda x : x[1], reverse = True)
	i_sorted_scores_first_last = sorted(i_score_diff_first_last, key = lambda x : x[1], reverse=True)
	n_sorted_scores_all = sorted(n_score_diff_all, key = lambda x : x[2], reverse = True)
	n_sorted_scores_all = sorted(n_sorted_scores_all, key = lambda x : x[0])
	n_sorted_scores_first_last = sorted(n_score_diff_first_last, key = lambda x : x[2], reverse = True)
	n_sorted_scores_first_last = sorted(n_sorted_scores_first_last, key = lambda x : x[0])
	print "Sorting done.\nWrite into files.."
	f = open(os.path.join(path_final_output,cs.final_all_new),"wb")
	writer = csv.writer(f)
	for (y,i,sc) in n_sorted_scores_all:
		writer.writerow([y,word_list[i][0],sc])
	f.close()
	f = open(os.path.join(path_final_output,cs.final_first_last_new),"wb")
	writer = csv.writer(f)
	for (y,i,sc) in n_sorted_scores_first_last:
		writer.writerow([y,word_list[i][0],sc])
	f.close()
	f = open(os.path.join(path_final_output,cs.final_all_inter),"wb")
	writer = csv.writer(f)
	for (i,sc) in i_sorted_scores_all:
		writer.writerow([word_list[i][0],sc])
	f.close()
	f = open(os.path.join(path_final_output,cs.final_first_last_inter),"wb")
	writer = csv.writer(f)
	for (i,sc) in i_sorted_scores_first_last:
		writer.writerow([word_list[i][0],sc])
	f.close()
	print "Files written."

if __name__ == '__main__':
	# 1. python realign_models.py five
	# 2. python realign_models.py decade
	period = sys.argv[1]
	realign_models_all(period)
