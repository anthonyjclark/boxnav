from box import Box, Pt
from boxenv import BoxEnv
from boxnavigator import PerfectNavigator, WanderingNavigator, Action

from ue5env import UE5EnvWrapper
from celluloid import Camera
import matplotlib.pyplot as plt

from argparse import ArgumentParser


# TODO: update to reflect OldenborgUE
boxes = [
    Box(Pt(420, -350), Pt(-190, -350), Pt(-190, 1070), Pt(115, 1020)),
    Box(Pt(-860, 240), Pt(-190, 240), Pt(-190, 600), Pt(-400, 440))
    # Box(Pt(1070, -190), Pt(-350, -190), Pt(-350, 420), Pt(900, 315)),
    # Box(Pt(240, -860), Pt(240, -190), Pt(610, -190), Pt(400, -440)),
    # Box(Pt(240, -450), Pt(-240, -190), Pt(1070, -190), Pt(500, 115)),
    # Box(Pt(-190, -350), Pt(-190, 1070), Pt(420, 1070), Pt(115, 1020))
    # Box(Pt(-365, 600), Pt(-450, 600), Pt(-190, 240), Pt(-700, 240)),
]


def simulate():
    """Create and update the box environment and run the navigator."""
    env = BoxEnv(boxes)
    agent_position = Pt(2, 2)
    agent_rotation = 0
    if args.ue:
        ue5 = UE5EnvWrapper(args.port)
        startX, startY, z = ue5.getCameraLocation(0)
        agent_position = Pt(startX, startY)
    else:
        ue5 = None

    if args.navigator == "wandering":
        agent = WanderingNavigator(
            agent_position, agent_rotation, env, out_of_bounds=args.ue, ue5_wrapper=ue5
        )
    elif args.navigator == "perfect":
        agent = PerfectNavigator(
            agent_position, agent_rotation, env, out_of_bounds=args.ue, ue5_wrapper=ue5
        )
    else:
        raise ValueError("Invalid argument error (check code for options).")

    fig, ax = plt.subplots()
    camera = Camera(fig)

    # TODO: turn into CLI argument
    max_actions_to_take = 20
    num_actions_taken = 0

    while not agent.at_final_target():
        action_taken, correct_action = agent.take_action()
        print(agent.position.xy)
        print(ue5.getCameraLocation(0))

        # if action_taken == Action.FORWARD:
        #     ue5.forward(agent.translation_increment)
        # elif action_taken == Action.ROTATE_LEFT:
        #     ue5.rotate_left(agent.rotation_increment)
        # elif action_taken == Action.ROTATE_RIGHT:
        #     ue5.rotate_right(agent.rotation_increment)
        # else:
        #     ue5.move_backward(agent.translation_increment)
        # agent.update_position
        # else:
        #     raise NotImplemented

        # agent.update_position()

        # TODO: use "correct_action" to label the image

        env.display(ax)
        agent.display(ax, env.scale)
        camera.snap()

        num_actions_taken += 1
        if num_actions_taken >= max_actions_to_take:
            break

    print(
        f"Simulation complete, it took {num_actions_taken} actions to reach the end. Now creating output."
    )

    anim = camera.animate()
    anim.save("output." + args.save_ext)


argparser = ArgumentParser("Navigate around a box environment.")
argparser.add_argument("save_ext", type=str, help="Extension for output format.")
argparser.add_argument(
    "port", type=int, default=8500, help="Port to connect to the unreal Environment"
)
argparser.add_argument(
    "--navigator", type=str, default="perfect", help="Navigator to use."
)
argparser.add_argument(
    "--ue", action="store_true", help="Navigate in Unreal Engine environment."
)

args = argparser.parse_args()

simulate()
