import sys
import matplotlib.pyplot as plt

def check_argv(argv):
	if len(argv) != 2:
		print("\033[31mNeed only one dataset\033[37m")
		exit()
	return argv[1]

def fill_data(path):
	title = 0
	feature = {}
	with open(path) as file:
		for line in file:
			if not title:
				title = line[:-1].split(',')
				for i, data in enumerate(title):
					if data == 'Hogwarts House':
						house = i
					if data == 'Astronomy':
						astronomy = i
					if data == 'Defense Against the Dark Arts':
						darkart = i
				continue
			data = line[:-1].split(',')
			try:
				for f in feature[data[house]]:
					if data[astronomy] == '':
						feature[data[house]]['Astronomy'].\
							append('NaN')
					else:
						feature[data[house]]['Astronomy'].\
							append(float(data[astronomy]))
					if data[darkart] == '':
						feature[data[house]]['DefDarkArt'].\
							append('NaN')
					else:
						feature[data[house]]['DefDarkArt'].\
							append(float(data[darkart]))
			except KeyError:
				feature[data[house]] = {}
				if data[astronomy] == '':
					feature[data[house]]['Astronomy'] =\
						['NaN']
				else:
					feature[data[house]]['Astronomy'] =\
						[float(data[astronomy])]
				if data[darkart] == '':
					feature[data[house]]['DefDarkArt'] =\
						['NaN']
				else:
					feature[data[house]]['DefDarkArt'] =\
						[float(data[darkart])]
	return feature

def draw_graph(feature):
	plt.figure(figsize=(18, 10))
	for house in feature:
		plt.scatter(feature[house]['Astronomy'],
					feature[house]['DefDarkArt'],
					label=house, alpha=0.5, s=10)
	plt.title('Similar features')
	plt.xlabel('Astronomy')
	plt.ylabel('Defense Against the Dark Arts')
	plt.legend(loc='upper right')
	plt.show()

def main(argv):
	path = check_argv(argv)
	feature = fill_data(path)
	draw_graph(feature)

if __name__ == "__main__":
	main(sys.argv)