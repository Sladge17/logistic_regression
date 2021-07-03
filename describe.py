import sys

def check_argv(argv):
	if len(argv) != 2:
		print("\033[31mNeed only one dataset\033[37m")
		exit()
	return argv[1]

def fill_data(path):
	title = 0
	with open(path) as file:
		for string in file:
			if not title:
				title = string[:-1].split(',')
				feature = [[] for i in range(len(title))]
				continue
			string = string[:-1].split(',')
			for i in range(len(string)):
				feature[i].append(string[i])
	return title, feature

def clear_data(title, feature):
	i = 0
	while i < len(feature):
		for j in range(len(feature[i])):
			try:
				feature[i][j] = int(feature[i][j])
			except ValueError:
				try:
					feature[i][j] = float(feature[i][j])
				except ValueError:
					if feature[i][j] == '':
						feature[i][j] = 'NaN'
						continue
					feature.pop(i)
					title.pop(i)
					i -= 1
					break
			except IndexError:
				return
		i += 1

def pre_analyze(feature):
	for i in range(len(feature)):
		feature[i] = list(filter(lambda x: x != 'NaN', feature[i]))

def print_title(title, column_w):
	print_title = [i.split() for i in title]
	height = max(map(len, print_title))
	for i in range(height):
		print('     ', end='\t')
		for j in range(len(print_title)):
			try:
				print(' ' * (column_w - len(print_title[j][i])), end='')
				print(print_title[j][i], end='\t')
			except:
				print(' ' * column_w, end='\t')
		print()

def get_count(feature):
	count = len(feature)
	return count

def get_mean(feature):
	try:
		mean = sum(feature) / get_count(feature)
	except ZeroDivisionError:
		mean = 'NaN'
	return mean

def get_std(feature):
	mean = get_mean(feature)
	if mean != 'NaN':
		div = [(i - mean) ** 2 for i in feature]
		std = (sum(div) / (len(div) - 1)) ** 0.5
	else:
		std = 'NaN'
	return std

def get_min(feature):
	if len(feature) == 0:
		return 'NaN'
	min_value = feature[0]
	for i in feature[1:]:
		if i < min_value:
			min_value = i
	return min_value

def get_max(feature):
	if len(feature) == 0:
		return 'NaN'
	max_value = feature[0]
	for i in feature[1:]:
		if i > max_value:
			max_value = i
	return max_value

def get_fraction25(feature):
	if len(feature) == 0:
		return 'NaN'
	feature = sorted(feature)
	fract = len(feature) / 4
	if fract % 1:
		fract += 1
	fract_value = feature[int(fract) - 1]	
	return fract_value

def get_fraction50(feature):
	if len(feature) == 0:
		return 'NaN'
	feature = sorted(feature)
	fract = len(feature) / 2
	if fract % 1:
		fract += 1
	fract_value = feature[int(fract) - 1]	
	return fract_value

def get_fraction75(feature):
	if len(feature) == 0:
		return 'NaN'
	feature = sorted(feature)
	fract = 3 * len(feature) / 4
	if fract % 1:
		fract += 1
	fract_value = feature[int(fract) - 1]	
	return fract_value

def print_datastring(title, func, feature, column_w):
	print(title, end='\t')
	if len(title) < 4:
		print(end='\t')
	for i in range(len(feature)):
		param = func(feature[i])
		if param != 'NaN':
			param = float(param)
			sign = 1 if param < 0 else 0
			print(' ' * (column_w - (len(str(abs(int(param)))) + 7 + sign)), end='')
			print(round(param, 6), end='')
			print('0' * (6 - len(str(round(abs(param - int(param)), 6))[2:])), end='\t')
		else:
			print(' ' * (column_w - 3), end='')
			print(param, end='\t')
	print()

def main(argv):
	path = check_argv(argv)
	title, feature = fill_data(path)
	clear_data(title, feature)
	pre_analyze(feature)
	column_w = 16
	print_title(title, column_w)
	print()
	print_datastring('Count', get_count, feature, column_w)
	print_datastring('Mean', get_mean, feature, column_w)
	print_datastring('Std', get_std, feature, column_w)
	print_datastring('Min', get_min, feature, column_w)
	print_datastring('25%', get_fraction25, feature, column_w)
	print_datastring('50%', get_fraction50, feature, column_w)
	print_datastring('75%', get_fraction75, feature, column_w)
	print_datastring('Max', get_max, feature, column_w)

if __name__ == "__main__":
	main(sys.argv)