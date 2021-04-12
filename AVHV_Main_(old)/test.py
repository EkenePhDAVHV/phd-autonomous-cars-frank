from AVHV_Main.Car import Car
from AVHV_Main.Environment import Environment
from AVHV_Main.test.LayoutList import cross_roads

my_car = Car(route=[1, 2, 4, 5])
print(my_car)
print(my_car.position)
print(my_car.acceleration.get_value())
print(my_car.velocity.get_value())
print(my_car.speed)
print(my_car.route)

my_car.set_environment(Environment('my_environment', cross_roads()))

print(my_car.environment.road_system)

print(my_car.environment.road_system.node(1))

print(my_car.environment.road_system.node(1).position)

