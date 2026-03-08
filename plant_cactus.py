from core import do_harvest, do_plant, fork_join, move_to, reset_farm_state


def plant_cactus():
	# Непрерывно выращивает, сортирует и собирает кактусы по всей ферме
	size = get_world_size()  # Размер мира (NxN)

	# Сколько строк/столбцов обрабатывает один дрон
	per_worker = (size + max_drones() - 1) // max_drones()

	# Основной цикл — работаем, пока не наберём нужное количество кактусов
	# while True:
	while num_items(Items.Cactus) < 33554432:

		def sort_by_row(worker_id):
			# Каждый дрон обрабатывает свой диапазон строк
			for x in range(
				worker_id * per_worker,
				min((worker_id + 1) * per_worker, size)
			):
				# Засаживаем всю строку кактусами
				for y in range(size):
					move_to(y, x)
					do_plant(Entities.Cactus)

				# Сортировка строки пузырьком по оси X (слева направо)
				for i in range(size - 1):
					swapped = False
					for j in range(size - 1 - i):
						move_to(j, x)
						# Сравниваем текущую клетку с соседней справа
						if measure() > measure(East):
							swap(East)
							swapped = True
					# Если обменов не было — строка уже отсортирована
					if not swapped:
						break

		# Запускаем сортировку строк параллельно на дронах
		fork_join(sort_by_row)

		def sort_by_col(worker_id):
			# Каждый дрон обрабатывает свой диапазон столбцов
			for x in range(
				worker_id * per_worker,
				min((worker_id + 1) * per_worker, size)
			):
				# Сортировка столбца пузырьком по оси Y (сверху вниз)
				for i in range(size - 1):
					swapped = False
					for j in range(size - 1 - i):
						move_to(x, j)
						# Сравниваем текущую клетку с клеткой сверху
						if measure() > measure(North):
							swap(North)
							swapped = True
					# Если обменов не было — столбец уже отсортирован
					if not swapped:
						break

		# Запускаем сортировку столбцов параллельно
		fork_join(sort_by_col)

		# После полной сортировки собираем урожай
		do_harvest()


def run():
	# Полный сброс состояния фермы
	reset_farm_state()

	# Запуск фермы кактусов
	plant_cactus()


# Точка входа в программу
run()
