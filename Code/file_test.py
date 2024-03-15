# This is a simple example of a Spike Custom System Programming Language program.
import force_sensor, distance_sensor, motor, motor_pair
from hub import port
import time
from app import linegraph as ln
import runloop
from math import *
import random
pair = motor_pair.PAIR_1
motor_pair.pair(pair, port.F, port.B)
motor_module = port.E
motor_module1 = port.A
force_module = port.D
calibration = 1
average = 111
times = 1
times1 = 1
average_calibration = []
average_obs = []
ai_data = []

def write_ai_data(file):
    with open("{file}", "w") as f:
        for line in ai_data:
            f.write(line)
ai = runloop.AI()
import random

class Random:
    def __init__(self, seed=None):
        # Setze den Startwert des Generators
        self.seed = seed if seed is not None else 0
        self.state = self.seed

        # LCG Parameter
        self.multiplier = 1103515245
        self.increment = 12345
        self.modulus = 2 ** 31

    def rand(self):
        # Generiere eine Zufallszahl und aktualisiere den Zustand
        self.state = (self.multiplier * self.state + self.increment) % self.modulus
        return self.state / self.modulus

    def randint(self, a, b):
        # Generiere eine Zufallszahl zwischen a und b (einschließlich beider Enden)
        return int(self.rand() * (b - a + 1)) + a

class LinearRegression:
    def __init__(self, learning_rate=0.01, epochs=1000):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        num_samples = len(X)
        num_features = len(X[0])
        self.weights = [0.0] * num_features
        self.bias = 0.0

        for _ in range(self.epochs):
            y_predicted = self.predict(X)
            dw = [0.0] * num_features
            db = 0.0

            for i in range(num_samples):
                dw = [dw[j] + (-2 / num_samples) * X[i][j] * (y[i] - y_predicted[i]) for j in range(num_features)]
                db += (-2 / num_samples) * (y[i] - y_predicted[i])

            self.weights = [self.weights[j] - self.learning_rate * dw[j] for j in range(num_features)]
            self.bias -= self.learning_rate * db

    def predict(self, X):
        y_predicted = []
        for sample in X:
            y_pred = sum(sample[i] * self.weights[i] for i in range(len(sample))) + self.bias
            y_predicted.append(y_pred)
        return y_predicted


class KMeans:
    def __init__(self, k, max_iters=100):
        self.k = k
        self.max_iters = max_iters
        self.centroids = None

    def fit(self, X):
        # Initialisiere zufällige Zentren
        self.centroids = random.sample(X, self.k)

        for _ in range(self.max_iters):
            # Zuweisung jeder Probe zu einem Cluster basierend auf der nächstgelegenen Zentroiden
            clusters = [[] for _ in range(self.k)]
            for sample in X:
                distances = [self._euclidean_distance(sample, centroid) for centroid in self.centroids]
                closest_centroid_idx = distances.index(min(distances))
                clusters[closest_centroid_idx].append(sample)

            # Aktualisiere die Zentren basierend auf den zugewiesenen Proben
            for i in range(self.k):
                if clusters[i]:
                    self.centroids[i] = [sum(dim) / len(dim) for dim in zip(*clusters[i])]

    def predict(self, X):
        predictions = []
        for sample in X:
            distances = [self._euclidean_distance(sample, centroid) for centroid in self.centroids]
            closest_centroid_idx = distances.index(min(distances))
            predictions.append(closest_centroid_idx)
        return predictions

    def _euclidean_distance(self, x1, x2):
        return sum((a - b) ** 2 for a, b in zip(x1, x2)) ** 0.5


class QLearning:
    def __init__(self, num_states, num_actions, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1, seed=None):
        self.num_states = num_states
        self.num_actions = num_actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_table = [[0] * num_actions for _ in range(num_states)]
        self.random_generator = random.Random(seed)

    def choose_action(self, state):
        if self.random_generator.random() < self.exploration_rate:
            return self.random_generator.randint(0, self.num_actions - 1)  # Wähle eine zufällige Aktion
        else:
            return self.get_best_action(state)  # Wähle die beste Aktion basierend auf Q-Werten

    def get_best_action(self, state):
        return self.q_table[state].index(max(self.q_table[state]))

    def update_q_table(self, state, action, reward, next_state):
        old_q_value = self.q_table[state][action]
        next_max_q_value = max(self.q_table[next_state])
        new_q_value = (1 - self.learning_rate) * old_q_value + self.learning_rate * (reward + self.discount_factor * next_max_q_value)
        self.q_table[state][action] = new_q_value

    def set_parameters(self, learning_rate=None, discount_factor=None, exploration_rate=None):
        if learning_rate is not None:
            self.learning_rate = learning_rate
        if discount_factor is not None:
            self.discount_factor = discount_factor
        if exploration_rate is not None:
            self.exploration_rate = exploration_rate
            


# Beispielverwendung:
# LinearRegression
X_train = [[1], [2], [3], [4], [5]]
y_train = [2, 4, 6, 8, 10]

model = LinearRegression()
model.fit(X_train, y_train)

X_test = [[6], [7], [8]]
predictions = model.predict(X_test)
print(predictions)

# KMeans
X = [[1, 2], [5, 8], [3, 6], [10, 12], [15, 18], [11, 14]]
model = KMeans(k=2)
model.fit(X)

print("Centroids:", model.centroids)

predictions = model.predict(X)
print("Predictions:", predictions)

# QLearning
num_states = 5
num_actions = 3
env = QLearning(num_states, num_actions, seed=42)

# Training
for _ in range(1000):
    state = env.random_generator.randint(0, num_states - 1)
    action = env.choose_action(state)
    reward = env.random_generator.uniform(0, 1)
    next_state = env.random_generator.randint(0, num_states - 1)
    env.update_q_table(state, action, reward, next_state)

# Testen
test_state = 4
best_action = env.get_best_action(test_state)
print("Beste Aktion für Zustand", test_state, ":", best_action)
#Module function
async def module(degrees=0, speed=1110, acceleration=10000):
    if (degrees > 0):
        await motor.run_for_degrees(motor_module, degrees, speed, acceleration=acceleration)
    elif (degrees < 0):
        await motor.run_for_degrees(motor_module, degrees, speed, acceleration=acceleration)
    elif (degrees == 0):
        print("Error")
#Drive function
async def drive(distance=0, multiplier=14, speed=1000, acceleration=1000):
    if (distance > 0):
        degrees = multiplier*(distance - calibration)
        await motor_pair.move_for_degrees(pair, degrees, 0, velocity=speed, acceleration=acceleration)
    elif (distance < 0):
        degrees = multiplier*(distance + calibration)
        await motor_pair.move_for_degrees(pair, degrees, 0, velocity=speed, acceleration=acceleration)
    elif (distance == 0):
        print("Bist du dumm?")

#Tank function
async def tank(degrees=0, left_speed=1000, right_speed=1000, acceleration=1000):
    #180 degrees = 90 Grad
    if (degrees > 0):
        await motor_pair.move_tank_for_degrees(pair, -degrees, left_speed, -right_speed, acceleration=acceleration)
    elif (degrees < 0):
        await motor_pair.move_tank_for_degrees(pair, degrees, -left_speed, right_speed, acceleration=acceleration)
    elif (degrees == 0):
        print("Bist du dumm?")

#Obstacle function
async def obstacle(distance=0, speed=1000, acceleration=1000):
    if (distance > 0):
        while distance_sensor.distance(port.C) > distance:
            await drive(2, 14, speed, acceleration)
        print("Obstacle detected!")
        #print(distance_sensor.distance(port.C))
    elif (distance <= 0):
        print("Bist du dumm?")
#Switch function
async def switch(switch=False):
    while switch == False:
        if (force_sensor.force(force_module) >= 50):
            switch = True
            return True
#Calibrate function
async def calibrate(speed=1000, acceleration=1000):
        if (distance_sensor.distance(port.C) < 110):
            print("Calibration not possible! | Distance to small!")
        elif (distance_sensor.distance(port.C) > 110):
            try:
                await drive(-1, 14, speed, acceleration)
                distance0 = distance_sensor.distance(port.C)
                await drive(10, 14, speed, acceleration)
                distance1 = distance_sensor.distance(port.C)
                calibration = distance0 - distance1
                #print("Calibration done!")
                print(calibration)
                wait(0.5)
            except:
                print("Calibration not possible! | Error!")
async def main():
  print('Running main Function')
  await drive(10)
  await tank(30)
  await drive(10)
runloop.run(main())
