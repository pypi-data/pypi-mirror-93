from Core import Core, clear

__core = Core()

intro = \
"""
CUBITUS Robotic Arm ~user interface~ v1.0
Enter \'help\' to show all comands
"""

helpstr = \
"""
>> about       Show application info.
>> clear       Clear terminal.
>> exit        Exit interface.
>> help        Show all commands.
>> perform     Perform a specific movement based on input.
>> equation    Perform a custom curve based on input.
>> reset       Reset application.
"""

about = \
"""
C.U.B.I.T.U.S. Robotic Arm
Developed by Oliver Kudzia 2020/2021
"""

def set_end_effector(unit, rho=0.0, omega=0.0, tau=0.0):
    """
    Sets end effector to specific angles (degrees or radians).

    If only 'unit' parameter is given, sets the default angle [0°, 0°, 0°]

    Parameters
    ----------
    unit : str
        'degrees' or 'radians'
    rho, omega, tau : float
        angle values (one for each axis)
    """
    if not isinstance(unit, str): raise TypeError("Parameter 'unit' must be string!")
    __core.SetEndEffector(unit, rho, omega, tau)

def set_gripper(is_grabbed):
    __core.SetGripper(is_grabbed)

def load_xml(name):
    """
    Loads XML file depending on where the file is located.

    ->Note that XML file must be in correct format and in the same directory as python script.
    ->Otherwise fails to proceed.

    Parameters
    ----------
    name : str
        full name of the file (e.g. 'cubitus.xml')
    """
    if not isinstance(name, str): raise TypeError("Parameter 'unit' must be string!")
    __core.LoadXML(__file__, name)

def move_to_point(x, y, z):
    """
    Moves the robotic arm to designated position.

    Depending on OS (Windows / Linux):
    ->Windows:\tplots the result using matplotlib
    ->Linux:\tphysically moves with the arm itself

    Parameters
    ----------
    x, y, z : float or int
        Carthesian coordinates for each axis (X, Y, Z)
    """
    __core.PerformPoint([x, y, z])

def perform_line(pointA, pointB, sampling=50, repeat=1):
    """
    Performs a line and move robotic arm towards computed positions.

    Depending on OS (Windows / Linux):
    ->Windows:\tplots the result using matplotlib
    ->Linux:\tphysically moves with the arm itself

    Parameters
    ----------
    pointA, pointB : list
        Points between which a line will be performed.
    """
    __core.PerformLine(pointA, pointB, sampling, repeat)

def perform_circle(pointA, pointB, pointC, sampling=50, repeat=1):
    """
    Performs a circle which is formed by 3 carthesian points and move robotic arm towards computed positions.

    Depending on OS (Windows / Linux):
    ->Windows:\tplots the result using matplotlib
    ->Linux:\tphysically moves with the arm itself

    Parameters
    ----------
    pointA, pointB, pointC : list
        Points between which a circle will be performed.
    """
    __core.PerformCircle(pointA, pointB, pointC, sampling, repeat)

def perform_parabola(quadratic, height, vertex, sampling=50, repeat=1):
    """
    Performs a parabola which is formed by 3 parameters and move robotic arm towards computed positions.

    Depending on OS (Windows / Linux):
    ->Windows:\tplots the result using matplotlib
    ->Linux:\tphysically moves with the arm itself

    Parameters
    ----------
    quadratic, vertex : float
    height : int
        Parameters defining parabola which will be performed.
    """
    __core.PerformParabola(quadratic, height, vertex, sampling, repeat)

def perform_bezier(pointA, pointB, pointC, sampling=50, repeat=1):
    """
    Performs a beziér curve which is formed by 3 carthesian points and move robotic arm towards computed positions.

    Depending on OS (Windows / Linux):
    ->Windows:\tplots the result using matplotlib
    ->Linux:\tphysically moves with the arm itself

    Parameters
    ----------
    pointA, pointB, pointC : list
        Points between which a beziér curve will be performed.
    """
    __core.PerformBezier(pointA, pointB, pointC, sampling, repeat)

def perform_custom_curve(Xequation: str, Yequation: str, Zequation: str, sampling=50, repeat=1):
    """
    Performs specific curve with respect to given equations.

    Parameters
    ----------
    sampling : int
        precision of a movement, determines on how many
        pieces is movement broken into
    repeat : int
        how many times should be specific shape performed
    """
    if not isinstance(Xequation, str) or not isinstance(Yequation, str) or not isinstance(Zequation, str): raise TypeError("All equations must be strings!")
    __core.PerformCustomCurve(Xequation, Yequation, Zequation, sampling, repeat)

def run_ui():
    """
    Opens user interface which acts like a simple command terminal.
    """

    def Perform():
        print("What type of shape do you want to perform?\nPossible options:\n\t• point\n\t• line\n\t• circle\n\t• parabola\n\t• bezier")
        shapeType = input(">>  ")
        clear()
        print("What sampling do you want (it means how many IK positions of selected shape will be computed)?\nPossible options:\n\t• a whole number from interval <10; 100>")
        sampling = int(input(">>  "))
        clear()
        print("How many times do you want to perform this movement?\nPossible options:\n\t• a whole number from interval <1; inf>")
        count = int(input(">>  "))
        __core.PerformUIGeometricShape(shape=shapeType, sampling=sampling, repeat=count)

    def PerformEquation():
        print("What sampling do you want (it means how many IK positions of selected shape will be computed)?\nPossible options:\n\t• a whole number from interval <10; 100>")
        sampling = int(input(">>  "))
        clear()
        print("How many times do you want to perform this movement?\nPossible options:\n\t• a whole number from interval <1; inf>")
        count = int(input(">>  "))
        __core.PerformUICustomCurve(sampling=sampling, repeat=count)

    print(intro)
    try:
        while True:
            userInput = input('>>  ').lower()
            if userInput == '': pass
            elif userInput == 'about':      print(about)
            elif userInput == 'clear':      clear()
            elif userInput == 'exit':       break
            elif userInput == 'help':       print(helpstr)
            elif userInput == 'perform':    Perform()
            elif userInput == 'equation':   PerformEquation()
            elif userInput == 'reset':      clear(); print(intro)
            else: print('Unknown command.')
    except KeyboardInterrupt: clear(); exit()
