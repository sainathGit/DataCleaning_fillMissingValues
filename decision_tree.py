
import csv
import pickle as pkl
import sys
import math
from collections import Counter

D = []
major_class = "" 
index = {} #its a dictionary to store indices of attributes in dataset

#======================================================

class tree_node:
	test = ""
	children = {}
	class_name = None
	

#=======================================================

def shrink_data(Dj, attr_index, output):
	Di = [x for x in Dj if x[attr_index] == output]
	return Di 

#=======================================================

def info(Dj):
	
	info_D = 0
	class_list = [x[-1] for x in Dj]
	counter = Counter(class_list)
	for key in counter.keys():
		p_i =  counter[key]/len(class_list)
		info_D += -1*p_i*math.log2(p_i)
		
	return info_D	

#=======================================================		

def infoA(Dj,attr_index):
	outputs = set(x[attr_index] for x in Dj) 
	
	info_A = 0
	for output in outputs:
		Di = shrink_data(Dj, attr_index, output)		
		info_A = info_A + (len(Di)/len(Dj))*info(Di)		
	return info_A

#=======================================================

def max_gain(Dj, attr_list):
	
	class_entropy = info(Dj)
	
	max_gain = [-sys.maxsize,""]
	
	for attr in attr_list:
		info_A = infoA(Dj, index[attr]) 
		gain_A = class_entropy - info_A			
		if gain_A > max_gain[0]:
			max_gain[0] = gain_A
			max_gain[1] = attr		
	return max_gain[1]
				
#=======================================================

def create_tree(Dj, attr_list):	
	node =  tree_node()
	class_list = [i[-1] for i in Dj]

#base conditions

	if len(Dj) == 0:
		node.class_name = major_class
		return node

	if class_list[1:] == class_list[:-1]:
		node.class_name = class_list[0];
		print("class node created", node.class_name)
		return node
	
#finding the maximum gain attribute

	splitting_node = max_gain(Dj, attr_list)
	print("created node with test" ,splitting_node)
	node.test = splitting_node
	attr_list.remove(splitting_node)
	
#here am considering the outputs in given data only
	
	attr_index = index[splitting_node] 
	outputs = set([i[attr_index] for i in Dj])
	
#recursively creatind the nodes
	
	for output in outputs:
		print('now going to',  output)
		Di = shrink_data(Dj, attr_index, output)
		node.children[output] = create_tree(Di, attr_list)
		print("attached to:" , node.test)
	print("node with attr", node.test, "attached")	
	
	return node

#========================================================


def fill_class(node, entry, index):
	
	while(node.class_name == None):
		test = node.test
		output = entry[index[test]]
		node = node.children[output]
	entry[-1] = node.class_name
	return 


def most_common(lst):
	data = Counter(lst)
	return max(lst, key=data.get)

#=========================================================

#reading csv file
def read_csv(file_name):
	D = []
	attr_list = []
	with open(file_name, 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter = ',')
		
		for i, row in enumerate(reader):
			if i==0:
				attr_list = row[1:-1]
			else:
				D.append(row[1:])
	return [D, attr_list]



[D,attr_list] = read_csv("dataset.csv")
#filling the global variables

for i, attr in enumerate(attr_list):
	index[attr] = i
mojor_class = most_common([i[-1]  for i in D])



#recursive call of create_tree starts

decisionTree = create_tree(D, attr_list)

#========================================================

# using bove tree for prediction:

(c_D, attr_list) = read_csv("currupted_data.csv")

			
for i, entry in enumerate(c_D):
	
	if(entry[-1] == '#'):
		print("found currupted entry in" , i)
		print("fixing data.....")
	fill_class(decisionTree,entry,index)
	print("ok completed!filled with class", entry[-1])


print("completed 100%")
with open("fixed_data.csv", "w") as csvfile:
	writer = csv.writer(csvfile)
	f_D = [attr_list,]
	f_D.extend(c_D)
	writer.writerows(f_D)
