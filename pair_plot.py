import sys
import pandas as pd
import seaborn as sns

def check_argv(argv):
	if len(argv) != 2:
		print("\033[31mNeed only one dataset\033[37m")
		exit()
	return argv[1]

def fill_data(path):
	feature = pd.read_csv(path)
	feature = feature.drop(['Index', 'First Name', 'Last Name',
							'Birthday', 'Best Hand'], axis=1)
	return feature

def draw_graph(feature):
	sns.pairplot(feature['Arithmancy', 'Astronomy', 'Herbology', 'Hogwarts House'], hue='Hogwarts House', diag_kind='hist')

def main(argv):
	# path = check_argv(argv)
	path = 'datasets/dataset_train.csv'
	feature = fill_data(path)
	draw_graph(feature)

if __name__ == "__main__":
	main(sys.argv)
