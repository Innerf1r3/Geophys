from graphs import GravityGraphs

# Задайте значения R0, M0, и RAD_VEL
R0 = 49244
M0 = 1.02e26
RAD_VEL = 9648

# Создайте экземпляр класса GravityGraphs
gravity_graphs = GravityGraphs(R0, M0, RAD_VEL)

# Вызовите метод для построения графиков
gravity_graphs.plot_gravity_graphs()
