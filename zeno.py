#!/usr/bin/env python3

"""
Visualization tool for the 42 `Philosophers` project
"""

__author__ = "Artem (a.k.a tesla33io)"
__version__ = "1.1"
__maintainer__ = "Artem"
__email__ = "52202562+tesla33io@users.noreply.github.com"
__status__ = "Development"

import argparse
import sys
import uuid
import subprocess as sp
import io

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

BLACK = "\033[0;30m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BROWN = "\033[0;33m"
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
CYAN = "\033[0;36m"
LIGHT_GRAY = "\033[0;37m"
DARK_GRAY = "\033[1;30m"
LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
LIGHT_BLUE = "\033[1;34m"
LIGHT_PURPLE = "\033[1;35m"
LIGHT_CYAN = "\033[1;36m"
LIGHT_WHITE = "\033[1;37m"
BOLD = "\033[1m"
FAINT = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
NEGATIVE = "\033[7m"
CROSSED = "\033[9m"
RESET = "\033[0m"

ERR_NO_INPUT = f"""
{RED}{BOLD}Error: no input was recived
{LIGHT_BLUE}Maybe something went wrong during auto-simulation :(
Try saving output of your simulation and manualy run the script:
{LIGHT_GREEN}./philo ... > `file_with_sim_output`; ./zeno -P < `file_with_sim_outpu`{RESET}
"""

WARN_NOT_OPTIMIZED = f"""
{YELLOW}WARNING: visualizer is not yet optimized.
I don't recommend to run it with more than 20 philos{RESET}
"""

WARN_TIMEOUT_TOO_SMALL = f"""
{YELLOW}WARNING: timeout was too small and was therefore changed to 10 seconds{RESET}
"""


def parse_events(lines: list) -> list:
    """
    Parses a list of strings representing event logs into a list of tuples containing:
    - timestamp (int)
    - Philosopher ID (int)
    - action (str)

    Each line is expected to have a format of "timestamp ID action".
    If a line cannot be parsed, an error message is printed and the program exits.

    Args:
        lines (list): List of strings representing event logs.

    Returns:
        list: A list of tuples with parsed event data.
    """
    events = []
    for line in lines:
        line = line.strip()
        try:
            parts = line.split(
                maxsplit=2
            )  # Split into at most three parts: timestamp, ID, and action
            timestamp = int(parts[0])
            id = int(parts[1])
            action = parts[2].replace("\\n", "")
            events.append((timestamp, id, action))
        except ValueError:
            print(f"{RED}Error: `{line}' is not a part of expected input{RESET}")
            exit(1)
    return events


def sort_by_philo_id(events: list) -> dict:
    """
    Sorts a list of events by philosopher ID and groups events by each ID.

    Each philosopher's events are stored in a dictionary, where the key is the philosopher's ID
    and the value is a list of tuples containing the timestamp and action.

    Args:
        events (list): List of tuples, where each tuple contains (timestamp, ID, action).

    Returns:
        dict: A dictionary with philosopher IDs as keys and lists of (timestamp, action) tuples as values.
    """
    philosophers = {}
    for timestamp, id, action in events:
        if id not in philosophers:
            philosophers[id] = []
        philosophers[id].append((timestamp, action))
    return dict(sorted(philosophers.items()))


def get_last_timestamp(lines: list) -> int:
    """
    Retrieves the timestamp of the last event.

    Args:
        lines (list): List of strings representing event logs.

    Returns:
        int: The timestamp from the last line in the list.
    """
    return int(lines[-1].split(maxsplit=2)[0])


action_colors = {
    "has taken a fork": "gray",
    "is eating": "#e34f44",
    "is sleeping": "#4278f5",
    "is thinking": "#78b33e",
    "died": "#7d23eb",
}


def render(
    s_events: dict,
    last_timestamp: int,
    lgnd: bool = False,
    labels: bool = False,
    sim_uid: str = None,
) -> None:
    """
    Renders a timeline of philosopher actions based on sorted event data.

    Each philosopher's actions are visualized as a separate horizontal bar plot, showing
    the duration of each action over time. Annotations display the start and end times,
    action duration, and the action performed. The plot includes an optional legend.

    Args:
        s_events (dict): Dictionary where keys are philosopher IDs and values are lists
                         of tuples (timestamp, action).
        last_timestamp (int): The timestamp of the last event in the simulation.
        lgnd (bool, optional): Whether to display the legend.
        labels (bool, optional): Whether to display action labels.
        sim_uid (str, optional): Unique identifier for the simulation, used as the plot window title.

    Returns:
        None
    """
    n_philos: int = len(s_events)
    fig, axes = plt.subplots(n_philos, 1, sharex=True)
    if n_philos == 1:
        axes = [axes]  # Ensure that `axes` is always a list

    for index, pid in enumerate(s_events):
        events = s_events[pid]
        for i in range(len(events) - 1):
            if events[i][1] == "has taken a fork":  # Skip `fork` event
                continue
            start_time = events[i][0]
            end_time = events[i + 1][0]
            action = events[i][1]
            duration = end_time - start_time
            axes[index].broken_barh(
                [(start_time, duration)],
                (0, 1),
                facecolors=action_colors[action],
                mouseover=True,
            )
            if labels:
                axes[index].annotate(
                    f"{start_time} - {end_time}\n{duration} ms\n{action}",
                    (start_time + duration / 2, 0.5),
                    color="black",
                    fontsize=8,
                    ha="center",
                    va="center",
                )
        last_time = events[-1][0]
        last_action = events[-1][1]
        last_duration = 0
        if last_action != "has taken a fork" and last_action != "died":
            last_duration = last_timestamp - last_time
            axes[index].broken_barh(
                [(last_time, last_duration)],
                (0, 1),
                facecolors=action_colors[last_action],
            )
        elif last_action == "died":
            last_duration = 0
            axes[index].broken_barh(
                [(last_time, 5)],
                (0, 1),
                facecolors=action_colors[last_action],
            )
        if labels:
            axes[index].annotate(
                f"{last_time} - {last_timestamp}\n{last_duration} ms\n{last_action}",
                (last_time + last_duration / 2, 0.5),
                color="black",
                fontsize=8,
                ha="center",
                va="center",
            )
        axes[index].set_ylabel(f"{pid} -- ", rotation=0)
        axes[index].grid(True, which="both", axis="x", linestyle="--", linewidth=0.5)

    axes[-1].set_xlabel("Time (ms)")
    if lgnd:
        patches = [
            mpatches.Patch(color=color, label=action)
            for action, color in action_colors.items()
        ]
        # , bbox_to_anchor=(0.9, 0.9))
        fig.legend(handles=patches, loc="upper right")

    if sim_uid is None:
        fig.canvas.manager.set_window_title("Zeno")
    else:
        fig.canvas.manager.set_window_title(sim_uid)

    # Maximize the plot window
    manager = plt.get_current_fig_manager()
    try:
        manager.window.state("zoomed")  # For TkAgg backend
    except AttributeError:
        try:
            manager.window.showMaximized()  # For Qt5Agg or Qt4Agg backends
        except AttributeError:
            pass

    plt.tight_layout(h_pad=0.000)
    plt.show()


def analyze(s_events: dict) -> None:
    """
    Analyzes philosopher events to count occurrences of each action per philosopher.

    The function counts how many times each philosopher performed actions such as eating,
    sleeping, and thinking. It also checks if any philosopher has died. The results are
    printed out for each philosopher.

    Args:
        s_events (dict): Dictionary where keys are philosopher IDs and values are lists
                         of tuples (timestamp, action).

    Returns:
        None
    """
    stats = {}
    for pid in s_events:
        stats[pid] = {}
        for event in s_events[pid]:
            if event[1] in stats[pid]:
                stats[pid][event[1]] += 1
            else:
                stats[pid][event[1]] = 1
    for pid in stats:
        print(f"\n{LIGHT_BLUE}Philosopher {pid}{RESET}:")
        try:
            print(f"\thas eaten {stats[pid]['is eating']} times")
        except KeyError:
            print("\thas eaten 0 time")
        try:
            print(f"\thas slept {stats[pid]['is sleeping']} times")
        except KeyError:
            print("\thas slept 0 times")
        try:
            print(f"\thas thought {stats[pid]['is thinking']} times")
        except KeyError:
            print("\thas thought 0 times")
        if "died" in stats[pid]:
            print(f"\tdied 1 times {LIGHT_RED}X({RESET}")


def auto_sim(
    exec: str,
    n_philos: int,
    t_die: int,
    t_eat: int,
    t_sleep: int,
    max_meal: int,
    to: int,
) -> list:
    exec = exec if isinstance(exec, str) else exec[0]
    n_philos = str(n_philos) if isinstance(n_philos, int) else str(n_philos[0])
    t_die = str(t_die) if isinstance(t_die, int) else str(t_die[0])
    t_eat = str(t_eat) if isinstance(t_eat, int) else str(t_eat[0])
    t_sleep = str(t_sleep) if isinstance(t_sleep, int) else str(t_sleep[0])
    max_meal = str(max_meal) if isinstance(max_meal, int) else str(max_meal[0])
    if max_meal == "-1":
        max_meal = "9999999"
    timeout = str(to) if isinstance(to, int) else str(to[0])
    if int(timeout) <= 9:
        print(WARN_TIMEOUT_TOO_SMALL)
        to = "10"
    print(
        f"{GREEN}Simulation: {LIGHT_GREEN}{exec} {n_philos} {t_die} {t_eat} {t_sleep} {max_meal}{RESET}"
    )
    simproc = sp.run(
        ["timeout", timeout, exec, n_philos, t_die, t_eat, t_sleep, max_meal],
        text=True,
        capture_output=True,
    )
    return simproc.stdout.splitlines()[0:-2]


def parse_input():
    parser = argparse.ArgumentParser(
        prog=f"{YELLOW}zeno{RESET}",
        description=f"Zeno (of Citium) [v{__version__}] visualizes the progress of the philosophers' simulation.",
        epilog=f"{CYAN}“Be tolerant with others and strict with yourself.”{RESET} – Marcus Aurelius",
        add_help=False,
    )
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help=f"-- {GREEN}show this help message and exit{RESET}",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        help=f"-- {GREEN}show program's version number and exit{RESET}",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "-s",
        "--save",
        action="store_true",
        help=f"-- {GREEN}Save simulation output to a file{RESET}",
        dest="save",
    )
    parser.add_argument(
        "--legend-off",
        action="store_false",
        help=f"-- {GREEN}Disable plot legend{RESET}",
        dest="legend",
    )
    parser.add_argument(
        "--labels-off",
        action="store_false",
        help=f"-- {GREEN}Disable labels in the plot{RESET}",
        dest="labels",
    )
    parser.add_argument(
        "-P",
        action="store_true",
        help=f"-- {GREEN}Accept input from pipe. "
        + f"If -P flag is not specified, zeno would run the simulation automatically with specified settings (below){RESET}",
        dest="from_pipe",
    )
    parser.add_argument(
        "-exec",
        nargs=1,
        default="philo",
        type=str,
        help=f"-- {GREEN}Name of the executable{RESET}",
        dest="exec",
    )
    parser.add_argument(
        "-to",
        nargs=1,
        default=15,
        type=int,
        help=f"-- {GREEN}Timeout for auto-simulation{RESET}",
        dest="timeout",
    )
    parser.add_argument(
        "-np",
        nargs=1,
        default=5,
        type=int,
        help=f"-- {GREEN}Number of philosophers in the simulation{RESET}",
        dest="num",
    )
    parser.add_argument(
        "-td",
        nargs=1,
        default=800,
        type=int,
        help=f"-- {GREEN}Time to die{RESET}",
        dest="t_die",
    )
    parser.add_argument(
        "-te",
        nargs=1,
        default=200,
        type=int,
        help=f"-- {GREEN}Time to eat{RESET}",
        dest="t_eat",
    )
    parser.add_argument(
        "-ts",
        nargs=1,
        default=200,
        type=int,
        help=f"-- {GREEN}Time to sleep{RESET}",
        dest="t_sleep",
    )
    parser.add_argument(
        "-mm",
        nargs=1,
        default=-1,  # -1 means no limit
        type=int,
        help=f"-- {GREEN}Limit of meals{RESET}",
        dest="max_meal",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = vars(parse_input())
    output = None
    print(WARN_NOT_OPTIMIZED)

    if args["from_pipe"]:
        output = sys.stdin.readlines()
    else:
        output = auto_sim(
            args["exec"],
            args["num"],
            args["t_die"],
            args["t_eat"],
            args["t_sleep"],
            args["max_meal"],
            args["timeout"],
        )
    if len(output) <= 0 or output is None:
        print(ERR_NO_INPUT)
        exit(1)

    sim_uid = str(uuid.uuid4())
    if args["save"]:
        with open(f"./philo_output_{sim_uid[:8]}", "w") as pof:
            pof.writelines(output)

    events = parse_events(output)
    s_events = sort_by_philo_id(events)

    print(f"Current simulation UID: {sim_uid}")
    if args["save"]:
        print(f"Log of the simulation saved in `philo_output_{sim_uid[:8]}`")

    analyze(s_events)
    print(
        f"{BLINK}{CYAN}TIP{RESET}{CYAN}: you can maximize the window with simulation visualization for better result{RESET}"
    )
    render(
        s_events, get_last_timestamp(output), args["legend"], args["labels"], sim_uid
    )
