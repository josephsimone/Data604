import simpy
import random

seed = 23
sticks_made = 0

print(f'Welcome to Joe\'s Hockey Stick Factory Simulator')
print(f'----------------------------------')
print(f'                             _     ')
print(f'                            -     ')
print(f'                           -      ')
print(f'                          -       ')
print(f'                         -        ')
print(f'                        -         ')
print(f'                  * -----         ')
print(f'BEGINNING SIMULATION')
print(f'----------------------------------')

# -------------------------------------------------

# Parameters


# working hours
hours = 8

# business days
days = 23

# total working time (hours)
total_time = hours * days

# containers
# graphite
graphite_capacity = 500
initial_graphite = 200

# polyurethane
poly_capacity = 100
initial_poly = 60

# paint
shaft_pre_paint_capacity = 60
blade_pre_paint_capacity = 60
shaft_post_paint_capacity = 120
blade_post_paint_capacity = 120

# dispatch
dispatch_capacity = 500

# employees per activity
# shaft
num_shaft = 2
mean_shaft = 1
std_shaft = 0.1

# blade
num_blade = 1
mean_blade = 1
std_blade = 0.2

# paint
num_paint = 3
mean_paint = 3
std_paint = 0.3

# assembly
num_assem = 2
mean_assem = 1
std_assem = 0.2

# critical levels
# critical stock should be 1 business day greater than supplier take to come
graphite_critical_stock = (((8 / mean_shaft * num_shaft +
                             (8 / mean_blade) * num_blade) * 3))  # 2 days to deliver + 1 marging

poly_critical_stock = (8 / mean_assem) * num_assem * 2  # 1 day to deliver + 1 marging


# -------------------------------------------------
# Constructor

class Hockey_Stick_Factory:
    def __init__(self, env):
        self.graphite = simpy.Container(env, capacity=graphite_capacity, init=initial_graphite)
        self.graphite_control = env.process(self.graphite_stock_control(env))
        self.poly = simpy.Container(env, capacity=poly_capacity, init=initial_poly)
        self.poly_control = env.process(self.polyurethane_stock_control(env))
        self.shaft_pre_paint = simpy.Container(env, capacity=shaft_pre_paint_capacity, init=0)
        self.blade_pre_paint = simpy.Container(env, capacity=blade_pre_paint_capacity, init=0)
        self.shaft_post_paint = simpy.Container(env, capacity=shaft_post_paint_capacity, init=0)
        self.blade_post_paint = simpy.Container(env, capacity=blade_post_paint_capacity, init=0)
        self.dispatch = simpy.Container(env, capacity=dispatch_capacity, init=0)
        self.dispatch_control = env.process(self.dispatch_sticks_control(env))

    def graphite_stock_control(self, env):
        yield env.timeout(0)
        while True:
            if self.graphite.level <= graphite_critical_stock:
                print('Graphite Stock Bellow Critical Level ({0}) at day {1}, hour {2}'.format(
                    self.graphite.level, int(env.now / 8), env.now % 8))
                print('Calling Graphite Supplier')
                print('----------------------------------')
                yield env.timeout(16)
                print('graphite Supplier Arrives at day {0}, hour {1}'.format(
                    int(env.now / 8), env.now % 8))
                yield self.graphite.put(300)
                print('New Graphite Stock is {0}'.format(
                    self.graphite.level))
                print('----------------------------------')
                yield env.timeout(8)
            else:
                yield env.timeout(1)

    def polyurethane_stock_control(self, env):
        yield env.timeout(0)
        while True:
            if self.poly.level <= poly_critical_stock:
                print('Polyurethane Stock Bellow Critical Level ({0}) at day {1}, hour {2}'.format(
                    self.poly.level, int(env.now / 8), env.now % 8))
                print('Calling Polyurethane Supplier')
                print('----------------------------------')
                yield env.timeout(9)
                print('Polyurethane Supplier Arrives at day {0}, hour {1}'.format(
                    int(env.now / 8), env.now % 8))
                yield self.poly.put(30)
                print('New Polyurethane Stock is {0}'.format(
                    self.poly.level))
                print('----------------------------------')
                yield env.timeout(8)
            else:
                yield env.timeout(1)

    def dispatch_sticks_control(self, env):
        global sticks_made
        yield env.timeout(0)
        while True:
            if self.dispatch.level >= 50:
                print('Dispatched Stock is {0}, Calling Pro Shop to pick up Hockey Sticks at day {1}, hour {2}'.format(
                    self.dispatch.level, int(env.now / 8), env.now % 8))
                print('----------------------------------')
                yield env.timeout(4)
                print('Pro Stop Picking {0} Hockey Sticks up at day {1}, hour {2}'.format(
                    self.dispatch.level, int(env.now / 8), env.now % 8))
                sticks_made += self.dispatch.level
                yield self.dispatch.get(self.dispatch.level)
                print('----------------------------------')
                yield env.timeout(8)
            else:
                yield env.timeout(1)


# Jobs

def shaft_builder(env, hockey_stick_factory):
    while True:
        yield hockey_stick_factory.graphite.get(1)
        shaft_time = random.gauss(mean_shaft, std_shaft)
        yield env.timeout(shaft_time)
        yield hockey_stick_factory.shaft_pre_paint.put(1)


def blade_builder(env, hockey_stick_factory):
    while True:
        yield hockey_stick_factory.graphite.get(1)
        blade_time = random.gauss(mean_blade, std_blade)
        yield env.timeout(blade_time)
        yield hockey_stick_factory.blade_pre_paint.put(2)


def painter(env, hockey_stick_factory):
    while True:
        yield hockey_stick_factory.shaft_pre_paint.get(5)
        yield hockey_stick_factory.blade_pre_paint.get(5)
        paint_time = random.gauss(mean_paint, std_paint)
        yield env.timeout(paint_time)
        yield hockey_stick_factory.shaft_post_paint.put(5)
        yield hockey_stick_factory.blade_post_paint.put(5)


def assembler(env, hockey_stick_factory):
    while True:
        yield hockey_stick_factory.shaft_post_paint.get(1)
        yield hockey_stick_factory.blade_post_paint.get(1)
        yield hockey_stick_factory.poly.get(1)
        assembling_time = max(random.gauss(mean_assem, std_assem), 1)
        yield env.timeout(assembling_time)
        yield hockey_stick_factory.dispatch.put(1)


# Generators


def shaft_builder_gen(env, hockey_stick_factory):
    for i in range(num_shaft):
        env.process(shaft_builder(env, hockey_stick_factory))
        yield env.timeout(0)


def blade_builder_gen(env, hockey_stick_factory):
    for i in range(num_blade):
        env.process(blade_builder(env, hockey_stick_factory))
        yield env.timeout(0)


def painter_job_gen(env, hockey_stick_factory):
    for i in range(num_paint):
        env.process(painter(env, hockey_stick_factory))
        yield env.timeout(0)


def assembler_job_gen(env, hockey_stick_factory):
    for i in range(num_assem):
        env.process(assembler(env, hockey_stick_factory))
        yield env.timeout(0)


# -------------------------------------------------

# Run Simulation
env = simpy.Environment()
hockey_stick_factory = Hockey_Stick_Factory(env)

shaft_gen = env.process(shaft_builder_gen(env, hockey_stick_factory))
blade_gen = env.process(blade_builder_gen(env, hockey_stick_factory))
painter_gen = env.process(painter_job_gen(env, hockey_stick_factory))
assembler_gen = env.process(assembler_job_gen(env, hockey_stick_factory))

env.run(until=total_time)

print('Pre paint has {0} shafts and {1} blades ready to be painted'.format(
    hockey_stick_factory.shaft_pre_paint.level, hockey_stick_factory.blade_pre_paint.level))
print('Post paint has {0} shafts and {1} blades ready to be assembled'.format(
    hockey_stick_factory.shaft_post_paint.level, hockey_stick_factory.blade_post_paint.level))
print(f'Dispatch has %d hockey sticks ready to go!' % hockey_stick_factory.dispatch.level)
print(f'----------------------------------')
print('Total Hockey Sticks Made: {0}'.format(sticks_made + hockey_stick_factory.dispatch.level))
print(f'----------------------------------')
print(f'SIMULATION STOPPED')
