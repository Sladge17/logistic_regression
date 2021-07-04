import sys
import matplotlib.pyplot as plt

def check_argv(argv):
	if len(argv) != 2:
		print("\033[31mNeed only one dataset\033[37m")
		exit()
	return argv[1]

def fill_data(path):
	title = 0
	score ={}
	with open(path) as file:
		for line in file:
			if not title:
				title = line[:-1].split(',')
				for i, data in enumerate(title):
					if data == 'Hogwarts House':
						house = i
					if data == 'Care of Magical Creatures':
						target = i
				continue
			data = line[:-1].split(',')
			if data[target] == '':
				continue
			try:
				score[data[house]].append(float(data[target]))
			except KeyError:
				score[data[house]] = [float(data[target])]
	return score

def draw_graph(score):
	plt.figure(figsize=(18, 10))
	bins = 20
	for i in score:
		plt.hist(score[i], alpha=0.5, label=i, bins=bins)
	plt.title('Care of Magical Creatures')
	plt.xlabel('score')
	plt.ylabel('amount')
	plt.legend(loc='upper right')
	plt.show()

def main(argv):
	path = check_argv(argv)
	score = fill_data(path)
	draw_graph(score)

if __name__ == "__main__":
	main(sys.argv)