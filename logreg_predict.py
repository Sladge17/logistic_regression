import sys
import os

def check_argv(argv):
	length = len(argv)
	if not length or length > 2:
		print("\033[31mNeed min one, max two params\033[37m")
		exit()
	return length

def fill_dump(dump='dump', custom=0):
	x_minmax = []
	weight = []
	while True:
		try:
			with open(dump) as file:
				for string in file:
					if string == '\n':
						break
					x_minmax.append(list(map(float, string.split())))
				for string in file:
					weight.append(float(string))
			break
		except:
			if custom:
				print("\033[31mDumpfile not exist\033[37m")
				exit()
			try:
				try:
					os.system("python3 logreg_train.py datasets/dataset_train.csv")
				except:
					os.system("python logreg_train.py datasets/dataset_train.csv")
			except:
				print("\033[31mNot exist file logreg_train.py\033[37m")
				exit()
	return x_minmax, weight

def get_reader(path):
	try:
		reader = open(path)
	except FileNotFoundError:
		print("\033[31mDataset not exist\033[37m")
		exit()
	return reader

def get_indexcolumn(reader):
	target = ['Ravenclaw', 'Slytherin', 'Gryffindor',
			'Ravenclaw', 'Slytherin', 'Gryffindor']
	index = [0] * (len(target) * 2)
	title = reader.readline()[:-1].split(',')
	for i in range(len(title)):
		if title[i] == 'Muggle Studies':
			index[0] = i
		if title[i] == 'Charms':
			index[1] = i
		if title[i] == 'Divination':
			index[2] = i
		if title[i] == 'Flying':
			index[3] = i
		if title[i] == 'History of Magic':
			index[4] = i
		if title[i] == 'Transfiguration':
			index[5] = i
		if title[i] == 'Charms':
			index[6] = i
		if title[i] == 'Care of Magical Creatures':
			index[7] = i
		if title[i] == 'Divination':
			index[8] = i
		if title[i] == 'Care of Magical Creatures':
			index[9] = i
		if title[i] == 'Herbology':
			index[10] = i
		if title[i] == 'Flying':
			index[11] = i
	return target, index

def clear_string(string, index):
	string = string[:-1].split(',')
	string = list(map(lambda x: string[x], index))
	return string

def norm_string(string, x_minmax):
	for j in range(len(string)):
		if string[j] == '':
			continue
		string[j] = normalization(float(string[j]), *x_minmax[j])
	return string

def normalization(target, val_min, val_max):
	return (target - val_min) / (val_max - val_min)

def fill_probability(probability, string, weight):
	for i in range(len(probability)):
		try:
			probability[i] = sigmoid(string[i * 2] * weight[i * 3] +\
									string[i * 2 + 1] * weight[i * 3 + 1] +\
									1 * weight[i * 3 + 2])
		except TypeError:
			probability[i] = 0

def sigmoid(predict):
	sigmoid = 1 / (1 + 2.718 ** -predict)
	return sigmoid

def get_house(probability, target):
	if max(probability) > 0.5:
		for i in range(len(probability)):
			if probability[i] == max(probability):
				house = target[i]
				break
	else:
		house = 'Hufflepuff'
	return house

def main(argv):
	if check_argv(argv) == 1:
		x_minmax, weight = fill_dump()
	else:
		x_minmax, weight = fill_dump(argv[1], 1)
	reader = get_reader(argv[0])
	target, index = get_indexcolumn(reader)
	writer = open("houses.csv", 'w')
	writer.write("Index,Hogwarts House\n")
	probability = [0] * len(target)
	for i, string in enumerate(reader):
		string = norm_string(clear_string(string, index), x_minmax)
		fill_probability(probability, string, weight)
		house = get_house(probability, target)
		writer.write(f"{i},{house}\n")
	reader.close()
	writer.close()
	print('\033[32mCreated file "houses.csv"\033[37m')

if __name__ == "__main__":
	main(sys.argv[1:])