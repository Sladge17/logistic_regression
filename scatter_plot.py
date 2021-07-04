import sys
import matplotlib.pyplot as plt

def check_argv(argv):
	if len(argv) != 2:
		print("\033[31mNeed only one dataset\033[37m")
		exit()
	return argv[1]

def fill_data(path):
	title = 0
	feature = {'Index':[], 'Astronomy':[], 'Muggle Studies':[]}
	with open(path) as file:
		for line in file:
			if not title:
				title = line[:-1].split(',')
				for i, data in enumerate(title):
					if data == 'Index':
						index = i
					if data == 'Astronomy':
						astronomy = i
					if data == 'Muggle Studies':
						muggle_studies = i
				continue
			data = line[:-1].split(',')
			if data[index] == '':
				feature['Index'].append('NaN')
			else:
				feature['Index'].append(float(data[index]))
			if data[astronomy] == '':
				feature['Astronomy'].append('NaN')
			else:
				feature['Astronomy'].append(float(data[astronomy]))
			if data[muggle_studies] == '':
				feature['Muggle Studies'].append('NaN')
			else:
				feature['Muggle Studies'].append(float(data[muggle_studies]))
	return feature

def draw_graph(feature):
	plt.figure(figsize=(18, 10))
	plt.scatter(feature['Index'], feature['Astronomy'],
				label='Astronomy', s=10)
	plt.scatter(feature['Index'], feature['Muggle Studies'],
				label='Muggle Studies', s=10)
	plt.title('Similar features')
	plt.xlabel('index')
	plt.ylabel('feature')
	plt.legend(loc='upper right')
	plt.show()

def main(argv):
	path = 'datasets/dataset_train.csv'
	feature = fill_data(path)
	draw_graph(feature)

if __name__ == "__main__":
	main(sys.argv)