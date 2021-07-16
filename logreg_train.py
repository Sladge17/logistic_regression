import sys
import numpy as np

def check_argv(argv):
	argv_len = len(argv)
	if not argv_len:
		return 'data.csv'
	if argv_len != 1:
		print("\033[31mNeed only one dataset\033[37m")
		exit()
	return argv[0]

def read_data(source):
	try:
		data = np.genfromtxt(source, dtype=np.unicode, delimiter=',')
	except:
		print("\033[31mDataset not exist\033[37m")
		exit()
	title = data[0]
	y = data[1:][:, np.where(title == 'Hogwarts House')[0][0]]
	target = np.array(['Ravenclaw', 'Slytherin', 'Gryffindor',
						'Ravenclaw', 'Slytherin', 'Gryffindor'])
	data = np.genfromtxt(source, dtype=np.float32, delimiter=',')
	x = data[1:][:, [np.where(title == 'Muggle Studies')[0][0],
					np.where(title == 'Charms')[0][0],
					np.where(title == 'Divination')[0][0],
					np.where(title == 'Flying')[0][0],
					np.where(title == 'History of Magic')[0][0],
					np.where(title == 'Transfiguration')[0][0],
					np.where(title == 'Charms')[0][0],
					np.where(title == 'Care of Magical Creatures')[0][0],
					np.where(title == 'Divination')[0][0],
					np.where(title == 'Care of Magical Creatures')[0][0],
					np.where(title == 'Herbology')[0][0],
					np.where(title == 'Flying')[0][0]]]
	rowmask = np.any(np.isnan(x), axis=1)
	x = x[~rowmask]
	y = y[~rowmask]
	return target, x, y

def prepare_features(x):
	x_minmax = get_minmax(x)
	set_xnorm(x, x_minmax)
	bias = np.ones((x.shape[0], 1))
	x = np.concatenate((x, bias), 1)
	return x_minmax, x

def get_minmax(x):
	x_minmax = np.zeros([x.shape[1], 2], np.float32)
	for i in range(x.shape[1]):
		x_minmax[i] = [x[:, i].min(), x[:, i].max()]
	return x_minmax

def set_xnorm(x, x_minmax):
	for i in range(x.shape[1]):
		x[:, i] = normalization(x[:, i], *x_minmax[i])

def normalization(target, val_min, val_max):
	return (target - val_min) / (val_max - val_min)

def learning_nn(x, y, target, epochs, alpha, batch, eborder):
	weight = np.random.random(x.shape[1] + target.size - 1)
	delta = np.zeros(weight.size, np.float32)
	error = np.zeros([epochs, target.size], np.float32)
	y_bin = get_bintarget(x, y, target)
	cursor = 0
	for epoch in range(epochs):
		set_errorepoch(error, epoch, x, weight, y_bin, target)        
		if np.all([i < eborder for i in error[epoch]]):
			return weight
		for i in range(x.shape[0]):
			fill_delta(delta, x, weight, y, i, target)
			cursor += 1
			if cursor == batch:
				cursor = update_weight(weight, delta, alpha)
		cursor = update_weight(weight, delta, alpha)
		np.random.shuffle([x, y])
	return weight

def get_bintarget(x, y, target):
	y_bin = np.zeros([target.size, y.size], np.int8)
	for i in range(y_bin.shape[0]):
		y_bin[i] = list(map(lambda x: 1 if x == target[i] else 0, y))
	return y_bin

def set_errorepoch(error, epoch, x, weight, y_bin, target):
	for i in range(target.size):
		error[epoch][i] = loss_log(get_vecpredict(x, weight, i),
									y_bin[i])

def loss_log(predict, target):
	loss_log = -np.mean(target * np.log(predict) +
						(1 - target) * np.log(1 - predict))
	return loss_log

def get_vecpredict(x, weight, i):
	predict = sigmoid(np.concatenate([x[:, (i * 2):(i * 2 + 2)],
									x[:, -1].reshape(-1, 1)],
									axis=1) @\
						weight[(i * 3):(i * 3 + 3)])
	return predict

def sigmoid(predict):
	sigmoid = 1 / (1 + np.exp(-predict))
	return sigmoid

def fill_delta(delta, x, weight, y, i, target):
	for j in range(target.size):
		predict = get_housepredict(x, weight, i, j)
		delta[(j * 3):(j * 3 + 3)] += predict_error(predict, y,
													i, target[j]) *\
									sigmoid_derivative(predict) *\
									feature_slice(x, i, j)

def get_housepredict(x, weight, i, j):
	predict = sigmoid(np.concatenate([x[i][(j * 2):(j * 2 + 2)],
								[1]]) @ weight[(j * 3):(j * 3 + 3)])
	return predict

def predict_error(predict, y, i, target):
	error = predict - int(y[i] == target)
	return error

def sigmoid_derivative(predict):
	derivative = predict * (1 - predict)
	return derivative

def feature_slice(x, i, j):
	slc = np.concatenate([x[i][(j * 2):(j * 2 + 2)],
						[x[i][-1]]])
	return slc

def update_weight(weight, delta, alpha):
	weight -= delta * alpha
	delta[:] = 0
	return 0

def create_dumpfile(x_minmax, weight):
	with open("dump", 'w') as file:
		for x in x_minmax:
			file.write(f"{x[0]} {x[1]}\n" )
		file.write('\n')
		for w in weight:
			file.write(f"{w}\n")

def main(argv):
	source = check_argv(argv)
	print('reading data...')
	target, x, y = read_data(source)
	print('learning nn...')
	x_minmax, x = prepare_features(x)
	epochs = 300
	alpha = 0.01
	batch = 500
	eborder = 0.12
	weight = learning_nn(x, y, target, epochs,
						alpha, batch, eborder)
	create_dumpfile(x_minmax, weight)
	print('created dump file')

if __name__ == "__main__":
	main(sys.argv[1:])