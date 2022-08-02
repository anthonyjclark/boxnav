from box import Box, Pt
from boxenv import BoxEnv
from boxnavigator import BoxBoyScout

from celluloid import Camera

import matplotlib.pyplot as plt

from math import radians

# TODO: update to reflect OldenborgUE
boxes = [
    Box(Pt(0, 0), Pt(0, 20), Pt(10, 20), Pt(5, 18)),
    Box(Pt(0, 10), Pt(0, 20), Pt(30, 20), Pt(28, 15)),
    Box(Pt(20, 10), Pt(20, 40), Pt(30, 40), Pt(25, 38)),
]

env = BoxEnv(boxes)
agent = BoxBoyScout(Pt(2, 2), radians(0), env)

# Initiate camera
fig, ax = plt.subplots()
camera = Camera(fig)

while not agent.at_final_target():
    agent.take_action()

    env.display(ax)
    agent.display(ax, env.scale)
    camera.snap()

plt.show()
anim = camera.animate()
anim.save("test.gif")
