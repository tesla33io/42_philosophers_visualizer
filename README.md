# [Zeno](https://en.wikipedia.org/wiki/Zeno_of_Citium)

A Python script for parsing, visualizing, and analyzing event logs related to philosophers' actions in a simulation.

## Installation

To install the script, simply run:

```sh
wget "https://raw.githubusercontent.com/tesla33io/42_philosophers_visualizer/main/zeno.py"
```

This will download the script into your current directory.

### Dependencies

Zeno uses `matplotlib` to generate a plot representing the simulation. To ensure the script works correctly, install this library:

```sh
pip install matplotlib
```

As the final step, make the script executable by running:

```sh
chmod +x zeno.py
```

## Usage

Currently, Zeno supports only 'pipe' mode. To use the script, execute your philosophers program and pipe the output into the script as follows:

```sh
./philo 5 800 200 200 3 | ./zeno.py -P
```

The `-P` flag is mandatory in this case.

Note that Zeno cannot interrupt your simulation, so you should specify a maximum number of meals for your program to terminate properly and redirect the output to the script.