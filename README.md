# [Zeno](https://en.wikipedia.org/wiki/Zeno_of_Citium)

A Python script for parsing, visualizing, and analyzing event logs related to philosophers' actions in a simulation.

> [!NOTE]
> _Zeno cannot interrupt your simulation, so you should specify a maximum number of meals for your program to terminate properly and redirect the output to the script._
>
> See [**Usage**](https://github.com/tesla33io/42_philosophers_visualizer?tab=readme-ov-file#usage) for more info.

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

> If you get `error: externally-managed-environment` see [this](https://peps.python.org/pep-0668/)

As the final step, make the script executable by running:

```sh
chmod +x zeno.py
```

## Usage

Currently, Zeno supports only 'pipe' mode. To use the script, execute your philosophers program and pipe the output into the script as follows:

> [!NOTE]
> The `-P` flag is mandatory in current version.

If your simulation has an end condition (e.g. limit of meals or death of a philo), you can use `zeno` like so:
```sh
./philo 5 800 200 200 3 | ./zeno.py -P
```

If your simulation does not have an end condition, you can write the output to the file first:
```sh
./philo 5 800 200 200 > out
```

and then redirect this output to `zeno`:
```sh
./zeno -P < out
```

## Example

`./philo 5 800 200 200 3`

![./philo 5 800 200 200 3](https://raw.githubusercontent.com/tesla33io/42_philosophers_visualizer/main/example.png)

