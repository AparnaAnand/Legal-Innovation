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

#COULDNT_FIND = {}

def create_matrix(date,period,word_list):
	# 1. Load word2vec model based on date and period inputs
	# 2. For each word in word_list, query into model to obtain vector (if word not in model's vocab format the vocab's word as done in calculate_tf and then check if it tallies. If it doesn't tally take 0*100 vector)
	# 3. Append all vectors to form the word embedding matrix
	# 4. Return matrix
	#global COULDNT_FIND
	model = w2v.load_word2vec(date,period)
	#list_of_vocab = []
	#f = open(os.path.join(cs.path_tf_five,date+"allvocab.csv"), "wb")
	#writer = csv.writer(f)
	#for word in model.vocab:
		#list_of_vocab.append(word)
		#writer.writerow([word])
	#print "Done"
	#raw_input()
	#notfind = []
	mat = []
	for (word,c) in word_list:
		corr_word = word
		if corr_word in model.vocab: # CHECK CASE DOESN'T EXIST!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			mat.append(model[corr_word])
		else:
			for voc_word in model.vocab:
				old_voc = voc_word
				voc_word = voc_word.lower()
				voc_word = re.sub('\W', '', voc_word)
				voc_word = re.sub('[0-9]', '', voc_word)
				if voc_word == '':
					continue
			'''
				if word=="pinpoints":
					print old_voc,voc_word
					raw_input()
			'''
				if word == voc_word:
					#print "Here", word,voc_word,old_voc
					corr_word = old_voc
					#print corr_word
					break
			if corr_word not in model.vocab:
				#print "Not found!",corr_word
				#raw_input()
				#notfind.append(corr_word)
				mat.append([0]*100)
				#continue
			else:
				mat.append(model[corr_word])
	numpy_mat = np.array(mat)
	#COULDNT_FIND[date] = notfind
	#print COULDNT_FIND
	#raw_input()
	#print numpy_mat.shape
	return numpy_mat

def realign_models_all(period):
	# 1. Find the years for which the models are present, create the year_list and sort it
	# 2. Read the intersection file and newly added file and store all words in files in a word_list; also store year new words first occur in, in word_year
	# 3. For each time period, call create_matrix to create the word embedding
	# 4. Further call reorient() to realign the embedding of each year period (except first) wrt the previous year period's embedding
	# 5. Store all realigned embeddings in order in aligned_matrices list
	# 6. For each word in word_list, calculate the two scores (pairwise and last-first) from the aligned_matrices list
	# 7. Store scores in i_score_diff_all and i_score_diff_first_last, for intersection words, and i_score_diff_all and i_score_diff_first_last for newly added words
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
	final_set_words = set()
	year_list = []
	for file in glob.glob("*"+postfix):
		year = file.split("_")[0]
		year_list.append(year)
	year_list = sorted(year_list)
	print "YEARS: ",year_list
	os.chdir(os.path.join("..",".."))
	
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
		diff_by_year[year] = sorted(diff_by_year[year], key = lambda x : x[1], reverse = True)[:20]
	#word_list = []
	for year_str in diff_by_year:
		for (word,score) in diff_by_year[year_str]:
			m = re.search('(.*)_TF_five.csv',year_str)
			year = m.group(1)
			word_year[word] = year
			word_list.append((word,"n"))
	print "LEN WORDLIST: ",len(word_list)

	aligned_matrices = []
	first = create_matrix(year_list[0],period,word_list)
	aligned_matrices.append(first)
	for sec in range(1,len(year_list)):
		second = create_matrix(year_list[sec],period,word_list)
		first, r = emb.reorient(first,second)
		aligned_matrices.append(first)
	print "ALIGNED LEN: ",len(aligned_matrices)
	print "EACH MATRIX IN ALIGNED SHAPE: ",aligned_matrices[0].shape

	i_score_diff_all = []
	i_score_diff_first_last = []
	n_score_diff_all = []
	n_score_diff_first_last = []
	for word_index in range(len(word_list)):
		score = 0
		i = 0
		for j in range(1,len(aligned_matrices)):
			pair_diff = np.linalg.norm(aligned_matrices[j][word_index]-aligned_matrices[i][word_index])
			score+= pair_diff
			i+=1
		if word_list[word_index][1]=="i":
			i_score_diff_all.append((word_index,score))
		else:
			word = word_list[word_index][0]
			year = word_year[word]
			n_score_diff_all.append((year,word_index,score))

		score2 = 0
		if word_list[word_index][1]=="i":
			score2 = np.linalg.norm(aligned_matrices[len(aligned_matrices)-1][word_index]-aligned_matrices[0][word_index])
			i_score_diff_first_last.append((word_index,score2))
		else:
			y_i = year_list.index(year)
			print year,y_i
			raw_input()
			score2 = np.linalg.norm(aligned_matrices[len(aligned_matrices)-1][word_index]-aligned_matrices[y_i][word_index])
			n_score_diff_first_last.append((year,word_index,score2))
		if word_index%100 == 0:
			print "At: ",word_index
	i_sorted_scores_all = sorted(i_score_diff_all, key = lambda x : x[1], reverse = True)
	i_sorted_scores_first_last = sorted(i_score_diff_first_last, key = lambda x : x[1], reverse=True)
	n_sorted_scores_all = sorted(n_score_diff_all, key = lambda x : x[2], reverse = True)
	n_sorted_scores_all = sorted(n_sorted_scores_all, key = lambda x : x[0])
	n_sorted_scores_first_last = sorted(n_score_diff_first_last, key = lambda x : x[2], reverse = True)
	n_sorted_scores_first_last = sorted(n_sorted_scores_first_last, key = lambda x : x[0])
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
	

	'''
	
	aligned_matrices = []
	first = create_matrix(year_list[0],period,word_list)
	aligned_matrices.append(first)
	for sec in range(1,len(year_list)):
		second = create_matrix(year_list[sec],period,word_list)
		first, r = emb.reorient(first,second)
		aligned_matrices.append(first)
	print "ALIGNED LEN: ",len(aligned_matrices)
	print "EACH MATRIX IN ALIGNED SHAPE: ",aligned_matrices[0].shape
	score_diff_all = []
	score_diff_first_last = []
	for word_index in range(len(word_list)):
		score = 0
		i = 0
		for j in range(1,len(aligned_matrices)):
			pair_diff = np.linalg.norm(aligned_matrices[j][word_index]-aligned_matrices[i][word_index])
			score+= pair_diff
			i+=1
		word = word_list[word_index]
		year = word_year[word]
		score_diff_all.append((year,word_index,score))
		score2 = 0
		score2 = np.linalg.norm(aligned_matrices[len(aligned_matrices)-1][word_index]-aligned_matrices[0][word_index])
		score_diff_first_last.append((year,word_index,score2))
		if word_index%100 == 0:
			print "At: ",word_index
	sorted_scores_all = sorted(score_diff_all, key = lambda x : x[2], reverse = True)
	sorted_scores_all = sorted(sorted_scores_all, key = lambda x : x[0])
	sorted_scores_first_last = sorted(score_diff_first_last, key = lambda x : x[2], reverse = True)
	sorted_scores_first_last = sorted(sorted_scores_first_last, key = lambda x : x[0])
	f = open(os.path.join(path_final_output,cs.final_all_new),"wb")
	writer = csv.writer(f)
	for (y,i,sc) in sorted_scores_all:
		writer.writerow([y,word_list[i],sc])
	f.close()
	f = open(os.path.join(path_final_output,cs.final_first_last_new),"wb")
	writer = csv.writer(f)
	for (y,i,sc) in sorted_scores_first_last:
		writer.writerow([y,word_list[i],sc])
	f.close()
    '''

if __name__ == '__main__':
	# 1. python realign_models.py five
	# 2. python realign_models.py decade
	period = sys.argv[1]
	realign_models_all(period)
