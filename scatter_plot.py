import sys
import matplotlib.pyplot as plt

def check_argv(argv):
	if len(argv) != 2:
		print("\033[31mNeed only one dataset\033[37m")
		exit()
	return argv[1]

def fill_data(path):
	title = 0
	feature = {'Astronomy':[], 'Defense Against the Dark Arts':[]}
	with open(path) as file:
		for line in file:
			if not title:
				title = line[:-1].split(',')
				for i, data in enumerate(title):
					if data == 'Astronomy':
						astronomy = i
					if data == 'Defense Against the Dark Arts':
						darkart = i
				continue
			data = line[:-1].split(',')
			if data[astronomy] == '':
				feature['Astronomy'].append('NaN')
			else:
				feature['Astronomy'].append(float(data[astronomy]))
			if data[darkart] == '':
				feature['Defense Against the Dark Arts'].append('NaN')
			else:
				feature['Defense Against the Dark Arts'].append(float(data[darkart]))
	return feature

def draw_graph(feature):
	plt.figure(figsize=(18, 10))
	plt.scatter(feature['Astronomy'], feature['Defense Against the Dark Arts'], s=10)
	plt.title('Similar features')
	plt.xlabel('Astronomy')
	plt.ylabel('Defense Against the Dark Arts')
	plt.show()

def main(argv):
	path = check_argv(argv)
	feature = fill_data(path)
	draw_graph(feature)

if __name__ == "__main__":
	main(sys.argv)