import sys
import matplotlib.pyplot as plt

def check_argv(argv):
	if len(argv) != 2:
		print("\033[31mNeed only one dataset\033[37m")
		exit()
	return argv[1]

def fill_data(path):
	pass

def main(argv):
	# path = check_argv(argv)
	path = 'datasets/dataset_train.csv'
	feature = fill_data(path)
	draw_graph(feature)

if __name__ == "__main__":
	main(sys.argv)
