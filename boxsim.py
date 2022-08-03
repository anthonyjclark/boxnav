from box import Box, Pt
from boxenv import BoxEnv
from boxnavigator import PerfectNavigator

from celluloid import Camera
import matplotlib.pyplot as plt

from argparse import ArgumentParser
from math import radians

# TODO: update to reflect OldenborgUE
boxes = [
    Box(Pt(0, 0), Pt(0, 20), Pt(10, 20), Pt(5, 18)),
    Box(Pt(0, 10), Pt(0, 20), Pt(30, 20), Pt(28, 15)),
    Box(Pt(20, 10), Pt(20, 40), Pt(30, 40), Pt(25, 38)),
    # Box(Pt(420, -350), Pt(-190, -350), Pt(420, 1070), Pt(200, 600)),
    # Box(Pt(-365, 600), Pt(-450, 600), Pt(-190, 240), Pt(-700, 240)),
]


def simulate():
    """Create and update the box environment and run the navigator."""
    env = BoxEnv(boxes)
    agent = PerfectNavigator(Pt(2, 2), radians(0), env)

    fig, ax = plt.subplots()
    camera = Camera(fig)

    while not agent.at_final_target():
        agent.take_action()

        env.display(ax)
        agent.display(ax, env.scale)
        camera.snap()

    print("Simulation complete. Now creating output.")

    anim = camera.animate()
    anim.save("output." + args.save_ext)


argparser = ArgumentParser("Navigate around a box environment.")
argparser.add_argument("save_ext", type=str, help="Extension for output format.")
args = argparser.parse_args()

simulate()
