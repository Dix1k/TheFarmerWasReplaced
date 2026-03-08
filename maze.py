from core import do_harvest, reset_farm_state

def make_maze(substance=None):
	# Создать лабиринт, используя странное вещество.
	# Если количество вещества не задано, рассчитать его по формуле:
	# размер мира × 2^(число разблокированных лабиринтов − 1)
	if substance == None:
		substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	
	# Посадить куст (основа для лабиринта)
	plant(Entities.Bush)
	# Использовать странное вещество для формирования лабиринта
	use_item(Items.Weird_Substance, substance)

def play_maze():
	# Повторяющийся процесс: создание лабиринтов, поиск сокровищ и их сбор.
	
	def dfs_find_treasure():
		# Поиск сокровища методом обхода в глубину (DFS).
		current_x, current_y = get_pos_x(), get_pos_y()  # Текущие координаты
		
		# Если на текущей позиции находится сокровище — цель достигнута
		if get_entity_type() == Entities.Treasure:
			return True
		
		# Отметить текущую позицию как пройденную
		visited[(current_x, current_y)] = True
		
		directions = []  # Список направлений для поиска
		
		# Получить координаты сокровища с помощью измерения
		tx, ty = measure()
		# Определить приоритетные направления к сокровищу
		if tx - current_x > 0:
			directions.append(East)
		else:
			directions.append(West)
		
		if ty - current_y > 0:
			directions.append(North)
		else:
			directions.append(South)
		
		# Добавить оставшиеся направления (в случайном порядке)
		for direction in [East, West, North, South]:
			if direction not in directions:
				directions.append(direction)
		
		# Попробовать переместиться в каждом направлении
		for direction in directions:
			if can_move(direction):  # Если перемещение возможно
				# Рассчитать координаты следующей позиции
				next_x, next_y = current_x, current_y
				if direction == East:
					next_x += 1
				elif direction == West:
					next_x -= 1
				elif direction == North:
					next_y += 1
				elif direction == South:
					next_y -= 1
				
				# Если следующая позиция ещё не пройдена — двигаться туда
				if (next_x, next_y) not in visited:
					move(direction)  # Переместиться
					if dfs_find_treasure():  # Продолжить поиск из новой позиции
						return True
					# Если путь не привёл к цели — вернуться назад
					if direction == East:
						move(West)
					elif direction == West:
						move(East)
					elif direction == North:
						move(South)
					elif direction == South:
						move(North)
		
		return False  # Сокровище не найдено

	# Рассчитать количество странного вещества для лабиринта
	substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	
	# Бесконечный цикл создания лабиринтов и поиска сокровищ
	while True:
		make_maze(substance)  # Создать лабиринт
		visited = {}  # Очистить список пройденных позиций
		dfs_find_treasure()  # Начать поиск сокровища
		
		# Если сокровище найдено — собрать его
		if get_entity_type() == Entities.Treasure:
			do_harvest()
		
		clear()  # Очистить ферму для следующего лабиринта

def run():
	# Основной запуск: сбросить состояние фермы и начать игру с лабиринтами
	reset_farm_state()
	play_maze()

run()  # Запустить программу
