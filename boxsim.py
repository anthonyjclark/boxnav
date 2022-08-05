from box import Box, Pt
from boxenv import BoxEnv
from boxnavigator import PerfectNavigator, WanderingNavigator

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

    agent_position = Pt(2, 2)
    agent_rotation = 0

    if args.navigator == "wandering":
        agent = WanderingNavigator(agent_position, agent_rotation, env)
    elif args.navigator == "perfect":
        agent = PerfectNavigator(agent_position, agent_rotation, env)
    else:
        raise ValueError("Invalid argument error (check code for options).")

    fig, ax = plt.subplots()
    camera = Camera(fig)

    num_actions_taken = 0
    while not agent.at_final_target():
        action_taken, correct_action = agent.take_action()
        # TODO: use "correct_action" to label the image

        env.display(ax)
        agent.display(ax, env.scale)
        camera.snap()

        num_actions_taken += 1

    print(
        f"Simulation complete, it took {num_actions_taken} actions to reach the end. Now creating output."
    )

    anim = camera.animate()
    anim.save("output." + args.save_ext)


argparser = ArgumentParser("Navigate around a box environment.")
argparser.add_argument("save_ext", type=str, help="Extension for output format.")
argparser.add_argument(
    "--navigator", type=str, default="perfect", help="Navigator to use."
)
args = argparser.parse_args()

simulate()
