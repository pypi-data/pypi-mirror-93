# Cubitus Kinematics Package

This is the custom made package for Cubitus Robotic Arm. This package includes matplotlib plotting as well as realtime sending the data to the robotic manipulator itself.

## Installation

Run the following to install the package :

```console
$ pip install cubituskinematics
```

## Usage

First of all, you need to import cubituskinematics package/library into your project's python file.

```python
import cubituskinematics as ck
# or you could also use (but not recommended):
from cubituskinematics import *
```

Next you can test it using simple commands as shown below :

```python
# declare two points (as a list)
A = [200, 0, 120]
B = [200, 0, 230]
# performs a line movement
ck.perform_line(A, B, sampling=50, repeat=1)
# use 'sampling' and 'repeat' arguments to determine sampling and number of repetitions
```

```python
# moves to one certain point in 3D space
ck.move_to_point(210, 0, 170)
```

> NOTE: if you want to know more about a function, hover on its name to reveal more information

### User Interface Terminal

If you want to use user interface use one simple command as shown below :
```python
# opens user interface which acts like a simple command line terminal
ck.run_ui()
```

Here is a list of all possible commands which can be called via command line :

```console
>> about       Show application info.
>> clear       Clear terminal.
>> exit        Exit interface.
>> help        Show all commands.
>> perform     Perform a specific movement based on input.
>> equation    Perform a custom curve based on input.
>> reset       Reset application.
```
