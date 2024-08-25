# [Zeno](https://en.wikipedia.org/wiki/Zeno_of_Citium)

A Python script for parsing, visualizing, and analyzing event logs related to philosophers' actions in a simulation.

## Installation

To install the script, simply run:

```sh
wget "https://raw.githubusercontent.com/tesla33io/42_philosophers_visualizer/main/zeno.py"
```

This will download the script into your current directory.

### Dependencies

`zeno` uses `matplotlib` to generate a plot representing the simulation. To ensure the script works correctly, install this library:

```sh
pip install matplotlib
```

> [!TIP]
> If you get `error: externally-managed-environment` see [this](https://peps.python.org/pep-0668/)

As the final step, make the script executable by running:

```sh
chmod +x zeno.py
```

## Usage

### Pipe Mode

> [!NOTE]
> When running the script in pipe mode, your program **must terminate on its own**.

To use `zeno` in pipe mode, you can directly pipe the output of your `philo` simulation to the script:

```sh
./philo 5 800 200 200 7 | ./zeno -P
```

The `-P` flag indicates that the script is in pipe mode and should read from `STDIN`.

### Auto Mode

> [!NOTE]
> The `-P` flag overrides any other simulation settings and forces `zeno` to run in pipe mode.

> [!WARNING]
> This mode is still experimental and may not work perfectly. It is recommended to use pipe mode instead.

`zeno` can attempt to run a simulation for you if you specify the necessary parameters:

```sh
zeno [-exec EXEC] [-to TIMEOUT] [-np NUM] [-td T_DIE] [-te T_EAT] [-ts T_SLEEP] [-mm MAX_MEAL]
```

- `-exec EXEC` - Name of the executable to run.
- `-to TIMEOUT` - Timeout for the auto-simulation ($`\ge 10`$).
- `-np NUM` - Number of philosophers in the simulation.
- `-td T_DIE` - Time to die.
- `-te T_EAT` - Time to eat.
- `-ts T_SLEEP` - Time to sleep.
- `-mm MAX_MEAL` - Maximum number of meals allowed.

## Example

`./philo 5 800 200 200 3`

![./philo 5 800 200 200 3](https://raw.githubusercontent.com/tesla33io/42_philosophers_visualizer/main/example.png)

