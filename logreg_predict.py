import sys
import os

# def read_weights():
# 	x_minmax = [0] * 2
# 	weight = [0] * 2
# 	while True:
# 		try:
# 			with open("weights") as file:
# 				for i, string in enumerate(file):
# 					if i < 2:
# 						x_minmax[i] = int(string)
# 						continue
# 					weight[i - 2] = float(string)
# 			return (x_minmax, weight)
# 		except:
# 			try:
# 				os.system("python teacher.py")
# 			except:
# 				print("\033[31mNot exist file teacher.py\033[37m")
# 				exit()

# def normalization(target, val_min, val_max):
# 	return (target - val_min) / (val_max - val_min)

# def prediction(target, x_minmax, weight):
# 	target = normalization(target, *x_minmax)
# 	prediction = int(round(target * weight[0] + weight[1], 0))
# 	return prediction

# def check_argv(argv):
# 	if not len(argv):
# 		return 0
# 	for i in range(len(argv)):
# 		try:
# 			argv[i] = int(argv[i])
# 		except:
# 			print("\033[31mIncorrect input\033[37m")
# 			exit()
# 		if argv[i] < 0:
# 			print("\033[31mIncorrect input\033[37m")
# 			exit()
# 	return 1

# def run_multiprediction():
# 	x_minmax, weight = read_weights()
# 	while True:
# 		argv = input("Target mileage (km)(q -> quit): ")
# 		if argv == 'q':
# 			exit()
# 		try:
# 			argv = int(argv)
# 		except:
# 			print("\033[31mIncorrect input, try again\033[37m")
# 			continue
# 		if argv < 0:
# 			print("\033[31mIncorrect input, try again\033[37m")
# 			continue
# 		predict = max(prediction(int(argv), x_minmax, weight), 0)
# 		print(f"\033[32mMileage {argv}km, cost {predict}\033[37m")

# def run_singleprediction(argv):
# 	x_minmax, weight = read_weights()
# 	for i in argv:
# 		predict = max(prediction(i, x_minmax, weight), 0)
# 		print(f"\033[32mMileage {i}km, cost {predict}\033[37m")

def fill_dump(dump):
	x_minmax = []
	weight = []
	with open(dump) as file:
		for string in file:
			if string == '\n':
				break
			x_minmax.append(list(map(float, string.split())))
		for string in file:
			weight.append(float(string))
	return x_minmax, weight

def normalization(target, val_min, val_max):
	return (target - val_min) / (val_max - val_min)

def sigmoid(predict):
	# sigmoid = 1 / (1 + np.exp(-predict))
	sigmoid = 1 / (1 + 2.718 ** -predict)
	return sigmoid


def main(argv):
	x_minmax, weight = fill_dump(argv[1])
	
	writer = open("houses.csv", 'w')
	writer.write("Index,Hogwarts House\n")
	count = 0
	
	target = ['Ravenclaw', 'Slytherin', 'Gryffindor',
			'Ravenclaw', 'Slytherin', 'Gryffindor']
	probability = [0] * len(target)
	
	index = [0] * (len(target) * 2)
	with open(argv[0]) as reader:
		title = 0
		for string in reader:
			if not title:
				title = string[:-1].split(',')
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
				continue
			string = string[:-1].split(',')
			string = list(map(lambda x: string[x], index))

			for j in range(len(string)):
				if string[j] == '':
					continue
				string[j] = normalization(float(string[j]), *x_minmax[j])

			for i in range(len(probability)):
				try:
					probability[i] = sigmoid(string[i * 2] * weight[i * 3] +\
											string[i * 2 + 1] * weight[i * 3 + 1] +\
											1 * weight[i * 3 + 2])
				except TypeError:
					# probability[i] = None
					probability[i] = 0


			# prob_max = max(probability)
			
			if max(probability) > 0.5:
				for i in range(len(probability)):
					if probability[i] == max(probability):
						house = target[i]
						break
			else:
				house = 'Hufflepuff'


    # if np.max(probability) > 0.5:
    #     # print(probability)
    #     house = target[np.where(probability == np.max(probability))[0][0]]
    # else:
    #     if np.all([i < 0.5 for i in probability]):
    #         house = 'Hufflepuff'
    #         # print(probability)
    #     else:
    #         # print(probability)
    #         house = 'nan'
			
			# writer.write(f"{count},{string}\n")
			writer.write(f"{count},{house}\n")
			count += 1

	writer.close()


			# exit()





if __name__ == "__main__":
	main(sys.argv[1:])