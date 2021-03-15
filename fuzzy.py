import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# create fuzzy variables
service = ctrl.Antecedent(np.arange(0, 11, 1), "service")
food = ctrl.Antecedent(np.arange(0, 11, 1), "food")

tip = ctrl.Consequent(np.arange(0, 26, 1), "tip")

service.automf(number=3, names=["poor", "acceptable", "outstanding"])
food.automf(number=3, names=["bad", "decent", "great"])

tip["low"] = fuzz.trimf(tip.universe, [0, 0, 12.5])
tip["medium"] = fuzz.trimf(tip.universe, [0, 12.5, 25])
tip["high"] = fuzz.trimf(tip.universe, [12.5, 25, 25])

# rules

rule_1 = ctrl.Rule(service["outstanding"] | food["great"], tip["high"])
rule_2 = ctrl.Rule(service["acceptable"], tip["medium"])
rule_3 = ctrl.Rule(service["poor"] & food["bad"], tip["low"])

control_system = ctrl.ControlSystem([rule_1, rule_2, rule_3])

# Simulator
simulator = ctrl.ControlSystemSimulation(control_system)
simulator.input["service"] = 6
simulator.input["food"] = 4
simulator.compute()

tip_result = simulator.output["tip"]
print(tip_result)

tip.view(sim=simulator)
plt.show()

