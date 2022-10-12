from box import Box, Pt
from boxenv import BoxEnv
from boxnavigator import PerfectNavigator, WanderingNavigator, Action

# from ue5env import UE5Wrapper

from celluloid import Camera
import matplotlib.pyplot as plt

from argparse import ArgumentParser


# TODO: update to reflect OldenborgUE
boxes = [
    Box(Pt(-190, -350), Pt(-190, 1070), Pt(420, 1070), Pt(115, 1020)),
    # Box(Pt(-365, 600), Pt(-450, 600), Pt(-190, 240), Pt(-700, 240)),
]


def simulate():
    """Create and update the box environment and run the navigator."""
    env = BoxEnv(boxes)

    agent_position = Pt(2, 2)
    agent_rotation = 0

    if args.navigator == "wandering":
        agent = WanderingNavigator(
            agent_position, agent_rotation, env, out_of_bounds=args.ue
        )
    elif args.navigator == "perfect":
        agent = PerfectNavigator(
            agent_position, agent_rotation, env, out_of_bounds=args.ue
        )
    else:
        raise ValueError("Invalid argument error (check code for options).")

    fig, ax = plt.subplots()
    camera = Camera(fig)

    # ue5 = UE5Wrapper()

    # TODO: turn into CLI argument
    max_actions_to_take = 200
    num_actions_taken = 0

    while not agent.at_final_target():
        action_taken, correct_action = agent.take_action()

        # if action_taken == Action.FORWARD:
        #     ue5.forward(agent.translation_increment)
        # else:
        #     raise NotImplemented

        # agent.update_position()

        # TODO: use "correct_action" to label the image

        env.display(ax)
        agent.display(ax, env.scale)
        ax.invert_xaxis()
        camera.snap()

        num_actions_taken += 1
        if num_actions_taken >= max_actions_to_take:
            break

    print(
        f"Simulation complete, it took {num_actions_taken} actions to reach the end. Now creating output."
    )

    anim = camera.animate()
    anim.save("output." + args.save_ext)  # type: ignore


argparser = ArgumentParser("Navigate around a box environment.")
argparser.add_argument("save_ext", type=str, help="Extension for output format.")
argparser.add_argument(
    "--navigator", type=str, default="perfect", help="Navigator to use."
)
argparser.add_argument(
    "--ue", action="store_true", help="Navigate in Unreal Engine environment."
)
args = argparser.parse_args()

simulate()
