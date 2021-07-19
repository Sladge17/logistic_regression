import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def check_argv(argv):
	if len(argv) != 2:
		print("\033[31mNeed only one dataset\033[37m")
		exit()
	return argv[1]

def fill_data(path):
	try:
		feature = pd.read_csv(path)
		feature = feature.drop(['Index', 'First Name', 'Last Name',
								'Birthday', 'Best Hand'], axis=1)
	except FileNotFoundError:
		print("\033[31mDataset not exist\033[37m")
		exit()
	return feature

def draw_graph(feature):
	sns.pairplot(feature, hue='Hogwarts House', diag_kind='hist')
	plt.show()

def main(argv):
	path = check_argv(argv)
	feature = fill_data(path)
	draw_graph(feature)

if __name__ == "__main__":
	main(sys.argv)
