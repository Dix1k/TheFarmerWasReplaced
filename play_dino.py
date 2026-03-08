from core import move_to, reset_farm_state


def snake_coords(size):
	# Формирует маршрут обхода поля NxN в виде "змейки"
	path = []

	# Сначала проходим по первой строке сверху вниз (левый столбец)
	for col in range(size):
		path.append((0, col))

	# Если поле 1x1 — маршрут готов
	if size == 1:
		return path

	current_row = 1          # Текущая строка
	direction = -1           # Направление движения по строке
	extend_row = size - 2    # Специальная строка для корректного обхода

	# Для чётного размера поля корректируем последнюю строку
	if size % 2 == 0:
		extend_row = size - 1

	# Основной цикл обхода строк
	while current_row < size:
		if direction == 1:
			# Движение слева направо
			start_col = 1
			# Последняя строка при нечётном размере — начинаем с 0
			if current_row == size - 1 and size % 2 == 1:
				start_col = 0
			columns = range(start_col, size)
		else:
			# Движение справа налево
			if current_row == extend_row:
				columns = range(size - 1, -1, -1)
			else:
				columns = range(size - 1, 0, -1)

		# Добавляем все клетки строки в маршрут
		for col in columns:
			path.append((current_row, col))

		# Специальная логика для чётного поля:
		# возвращаемся вверх по левому столбцу
		if current_row == size - 1 and size % 2 == 0:
			for row in range(size - 2, 0, -1):
				path.append((row, 0))
			break

		# Переходим к следующей строке и меняем направление
		current_row += 1
		direction = -direction

	return path


def play_dino():
	# Патрулирование фермы по змейке в шляпе динозавра
	size = get_world_size()          # Размер фермы
	coords = snake_coords(size)      # Получаем маршрут обхода
	quick_print("coords = ", coords)

	idx = 1                          # Индекс текущей цели
	change_hat(Hats.Dinosaur_Hat)    # Надеваем шляпу динозавра

	while True:
		# Берём следующую клетку маршрута
		target_x, target_y = coords[idx]
		idx += 1

		# Пытаемся перейти в клетку (без автопути)
		moveable = move_to(target_x, target_y, False)

		# Если движение не удалось — перезагружаем шляпу
		# (используется как способ "починить" застревание)
		if not moveable:
			change_hat(Hats.Purple_Hat)
			change_hat(Hats.Dinosaur_Hat)

		# Если дошли до конца маршрута — начинаем сначала
		if idx >= len(coords):
			idx = 0


def run():
	# Сброс состояния фермы
	reset_farm_state()

	# Запуск динозаврьего патруля
	play_dino()


# Точка входа в программу
run()
