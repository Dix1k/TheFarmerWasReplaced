def do_plant(entity_type):
	# Посадить объект, предварительно убедившись, что грунт соответствует его требованиям.
	# Список объектов, которым нужна почва (пашня)
	need_soil = [Entities.Carrot, Entities.Sunflower, Entities.Pumpkin, Entities.Cactus]
	
	if entity_type in need_soil:
		# Если текущий тип грунта не пашня, вспахать землю
		if get_ground_type() != Grounds.Soil:
			till()
	else:
		# Если объект не требует пашни, но грунт — пашня, вспахать её
		if get_ground_type() == Grounds.Soil:
			till()

	# Посадить объект
	plant(entity_type)
	
	# Если уровень воды ниже 0.5 и есть запас воды, использовать воду
	if get_water() < 0.5 and num_items(Items.Water) > 0:
		use_item(Items.Water)


def do_harvest():
	# Собрать урожай с объекта, находящегося под дроном
	harvest()


def move_dir_n(direction, steps):
	# Попытаться переместиться в заданном направлении на указанное количество шагов.
	movable = True  # Флаг возможности перемещения
	for _ in range(steps):
		if not movable:
			break  # Прекратить попытки, если перемещение стало невозможным
		movable = movable and move(direction)  # Выполнить шаг и обновить флаг
	return movable  # Вернуть статус возможности перемещения

def move_to(x, y, shortest=True):
	# Переместиться в целевую координату, опционально используя кратчайший тороидальный путь.
	size = get_world_size()  # Получить размер мира (поля)
	current_x, current_y = get_pos_x(), get_pos_y()  # Текущие координаты дрона
	
	if shortest:
		# Рассчитать кратчайший путь с учётом тороидальной геометрии
		dx = ((x - current_x + size // 2) % size) - size // 2
		dy = ((y - current_y + size // 2) % size) - size // 2
	else:
		# Рассчитать прямой путь (без учёта тороидальности)
		dx = x - current_x
		dy = y - current_y

	movable = True  # Флаг возможности перемещения
	
	# Пройти по осям X и Y, перемещаясь в нужном направлении
	for delta, positive_dir, negative_dir in [(dx, East, West), (dy, North, South)]:
		if delta > 0:
			# Если нужно двигаться в положительном направлении
			movable = movable and move_dir_n(positive_dir, delta)
		elif delta < 0:
			# Если нужно двигаться в отрицательном направлении
			movable = movable and move_dir_n(negative_dir, -delta)
	
	return movable  # Вернуть статус возможности перемещения

def fork_join(func, max_workers=max_drones()):
	# Запустить функцию на нескольких дронах и дождаться завершения всех задач.
	drone_handles = []  # Список дескрипторов запущенных дронов
	
	# Запустить дроны (кроме последнего, который будет выполнен в текущем потоке)
	for worker_id in range(max_workers - 1):
		def wrapper(idx=worker_id):
			func(idx)  # Вызвать функцию с индексом дрона
		drone_handles.append(spawn_drone(wrapper))  # Запустить дрон и сохранить дескриптор

	# Выполнить функцию для последнего дрона в текущем потоке
	func(max_workers - 1)
	
	# Дождаться завершения всех запущенных дронов
	for handle in drone_handles:
		if handle:
			wait_for(handle)

def reset_farm_state():
	# Сбросить состояние фермы: сменить шляпу и очистить поле перед запуском сценария.
	clear()  # Очистить ферму
	change_hat(Hats.Purple_Hat)  # Сменить шляпу на фиолетовую

def scan_farm(func):
	# Пройти по всей ферме, вызывая callback-функцию для каждой ячейки.
	exited = False  # Флаг завершения обхода
	while not exited:
		for _ in range(get_world_size()):  # Пройти по строкам
			for _ in range(get_world_size()):  # Пройти по столбцам
				exited = func()  # Вызвать callback-функцию, получить флаг завершения
				move(North)  # Переместиться на север
				if exited:  # Если обход завершён, прервать цикл
					break
			move(East)  # Переместиться на восток
			if exited:  # Если обход завершён, прервать цикл
				break

def spawn_by_column(callback, max_workers=max_drones()):
	# Запустить дроны для обработки фермы по столбцам.
	size = get_world_size()  # Получить размер фермы
	# Рассчитать количество столбцов на одного дрона
	per_worker = (size + max_workers - 1) // max_workers
	quick_print("perN", per_worker)  # Вывести количество столбцов на дрон

	def run_column(worker_id):
		# Проверить, есть ли столбцы для обработки у данного дрона
		if worker_id * per_worker >= size:
			return
		
		exited = False  # Флаг завершения обработки
		while not exited:
			# Пройти по назначенным дрону столбцам
			for x in range(worker_id * per_worker, min((worker_id + 1) * per_worker, size)):
				# Пройти по всем строкам в столбце
				for y in range(size):
					move_to(x, y)  # Переместиться в ячейку
					exited = callback()  # Вызвать callback-функцию, получить флаг завершения
					if exited:  # Если обработка завершена, прервать цикл
						break
				if exited:  # Если обработка завершена, прервать цикл
					break

	# Запустить обработку столбцов с использованием нескольких дронов
	fork_join(run_column, max_workers)
