from core import do_harvest, do_plant, move_to, reset_farm_state


def play_companion():
	# Основной цикл companion-посадки (компаньонное земледелие)
	# Игра автоматически подсказывает, что сажать дальше
	random_plant = [
		Entities.Carrot,
		Entities.Sunflower,
		Entities.Grass,
		Entities.Bush,
		Entities.Tree
	]

	while True:
		# Если можно что-то собрать — собираем урожай
		if can_harvest():
			do_harvest()

		# Выбираем случайное растение из списка
		random_type = random_plant[random() * len(random_plant) // 1]
		quick_print("random_ty = ", random_type)

		# Сажаем выбранное растение
		do_plant(random_type)

		# Пока игра предлагает компаньонное растение
		while get_companion() != None:
			# Получаем тип растения и координаты для посадки
			next_type, (nx, ny) = get_companion()

			quick_print("next_ty = ", next_type)
			quick_print("nx = ", nx)
			quick_print("ny = ", ny)

			# Перемещаемся к нужной клетке
			move_to(nx, ny)

			# Если на клетке есть урожай — собираем
			if can_harvest():
				do_harvest()

			# Сажаем компаньонное растение
			do_plant(next_type)


def run():
	# Полный сброс состояния фермы
	reset_farm_state()

	# Запуск основного цикла посадки
	play_companion()


# Точка входа в программу
run()
