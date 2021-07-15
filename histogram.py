import sys
import matplotlib.pyplot as plt

def check_argv(argv):
	if len(argv) != 2:
		print("\033[31mNeed only one dataset\033[37m")
		exit()
	return argv[1]

def fill_data(path):
	title = 0
	score = {}
	with open(path) as file:
		for line in file:
			if not title:
				title = line[:-1].split(',')
				target = {}
				for i, data in enumerate(title):
					if data == 'Hogwarts House':
						house = i
					if data == 'Arithmancy' or\
						data == 'Potions' or\
						data == 'Care of Magical Creatures':
						target[data] = i
				continue
			data = line[:-1].split(',')
			for j in target:
				if data[target[j]] == '':
					continue
				try:
					score[j][data[house]].append(float(data[target[j]]))
				except:
					try:
						score[j][data[house]] = [float(data[target[j]])]
					except:
						score[j] = {data[house]:[float(data[target[j]])]}
	return score

def draw_graph(score):
	bins = 20
	fig, axis = plt.subplots(len(score) // 2 + int(bool(len(score) % 2)), 2,
								figsize=(18, 10))
	ind = 0
	for j in score:
		for i in score[j]:
			axis[ind // 2, ind % 2].\
				hist(score[j][i], alpha=0.5, label=i, bins=bins)
		axis[ind // 2, ind % 2].set(title=j, xlabel='score', ylabel='amount')
		axis[ind // 2, ind % 2].legend(loc="upper right")
		ind += 1
	plt.show()

def main(argv):
	path = check_argv(argv)
	score = fill_data(path)
	draw_graph(score)

if __name__ == "__main__":
	main(sys.argv)