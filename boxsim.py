from box import Box, Pt
from boxenv import BoxEnv
from boxboyscout import BoxBoyScout

from celluloid import Camera

import matplotlib.pyplot as plt

from math import radians

boxes = [
    Box(Pt(0, 0), Pt(0, 20), Pt(10, 20), Pt(5, 18)),
    Box(Pt(0, 10), Pt(0, 20), Pt(30, 20), Pt(28, 15)),
]

env = BoxEnv(boxes)
agent = BoxBoyScout(env, Pt(7, 12), radians(150))

# while not env.at_final_target(agent.position):
#     agent.take_action()

# Initiate camera
fig, ax = plt.subplots()
camera = Camera(fig)

for _ in range(30):
    agent.take_action()
    env.display(ax)
    agent.display(ax, env.scale)
    camera.snap()

plt.show()
anim = camera.animate(interval=1, repeat=True, repeat_delay=100)
anim.save("test.mov")
