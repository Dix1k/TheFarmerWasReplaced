from core import do_harvest, do_plant, reset_farm_state, scan_farm, spawn_by_column

def plant_by_column(plant_types=None):
	# Создать callback для посадки, который чередует культуры по столбцам.
	if plant_types == None:
		# Если список культур не задан, использовать стандартный набор
		plant_types = [Entities.Carrot, Entities.Tree, Entities.Grass]

	def do_planting():
		# Если на текущей позиции можно собрать урожай — собрать его
		if can_harvest():
			do_harvest()
			# Выбрать тип растения для посадки: индекс определяется по координате X
			# (остаток от деления на длину списка культур)
			plant_type = plant_types[get_pos_x() % len(plant_types)]
			
			# Для деревьев: если координата Y нечётная, вместо дерева посадить куст
			if plant_type == Entities.Tree and get_pos_y() % 2 == 1:
				plant_type = Entities.Bush
			
			# Посадить выбранное растение
			do_plant(plant_type)
		
		# Вернуть True, если запас сена достиг или превысил 2 000 000 000,
		# что может служить сигналом для завершения работы
		return num_items(Items.Hay) >= 2000000000

	return do_planting  # Вернуть функцию-callback для использования в других методах

def run_scan_farm_default():
	# Сбросить состояние фермы и запустить обход всей фермы с посадкой растений
	reset_farm_state()
	scan_farm(plant_by_column())  # Использовать стандартную конфигурацию посадок

def run_spawn_by_column_grass():
	# Сбросить состояние фермы и запустить посадку травы по столбцам
	reset_farm_state()
	spawn_by_column(plant_by_column([Entities.Grass]))  # Только трава

def run_spawn_by_column_default():
	# Сбросить состояние фермы и запустить стандартную посадку по столбцам
	reset_farm_state()
	spawn_by_column(plant_by_column())  # Стандартная конфигурация посадок

# Режимы работы:
# run_scan_farm_default()  # Обход всей фермы с чередованием культур (1 дрон)
run_spawn_by_column_default()  # Обход всей фермы с чередованием культур (несколько дронов)
# run_spawn_by_column_grass()  # Посадка только травы по столбцам
