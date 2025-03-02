# region imports
import numpy as np
from scipy.integrate import solve_ivp   #done
import matplotlib.pyplot as plt
# endregion

# region functions
def ode_system(t, X, *params):
    '''
    The ode system is defined in terms of state variables.
    I have as unknowns:
    x: position of the piston (This is not strictly needed unless I want to know x(t))
    xdot: velocity of the piston
    p1: pressure on right of piston
    p2: pressure on left of the piston
    For initial conditions, we see: x=x0=0, xdot=0, p1=p1_0=p_a, p2=p2_0=p_a
    :param X: The list of state variables.
    :param t: The time for this instance of the function.
    :param params: the list of physical constants for the system.
    :return: The list of derivatives of the state variables.
    '''
    """
    Steps for def ode_system:
    1. Unpack the parameters (placeholder variables for inputs)
    2. Create state variables to use in equations and for plotting
    3. List of all equations needed to graph the solution
    4. Return list of derivatives of state variables
    """
    #unpack the parameters
    """Setting up the variables for values"""
    A, Cd, ps, pa, V, beta, rho, Kvalve, m, y=params

    #state variables
    #X[0] = x
    #X[1] = xdot
    #X[2] = p1
    #X[3] = p2

    #calculate derivatives
    #conveniently rename the state variables   #done
    """State Variables that will be used to solve the differential equations"""
    x = X[0]
    xdot = X[1]
    p1 = X[2]
    p2 = X[3]

    #use my equations from the assignment
    """The three equations listed in the word doc"""
    xddot = (p1 - p2) * A / m
    p1dot = (y * Kvalve * (ps - p1) - rho * A * xdot) * beta / (V * rho)
    p2dot = -(y * Kvalve * (p2 - pa) - rho * A * xdot) * beta / (V * rho)

    #return the list of derivatives of the state variables
    return [xdot, xddot, p1dot, p2dot] #done

def main():
    """
    Steps for def main:
    1. Create variable (t) and use np.linspace to make an array
    2. List values for all necessary variables and state variables
    3. Solve the initial value problem (sln) with the proper functions/variables
    4. Unpack results to specific variable names
    5. Plot result
    :return:
    """
    #After some trial and error, I found all the action seems to happen in the first 0.02 seconds
    """This creates an array"""
    t=np.linspace(0,0.02,200)

    # myargs=(A, Cd, Ps, Pa, V, beta, rho, Kvalve, m, y)
    """Values for our parameters"""
    myargs=(4.909E-4, 0.6, 1.4E7,1.0E5,1.473E-4,2.0E9,850.0,2.0E-5,30, 0.002) #values for variables

    #because the solution calls for x, xdot, p1 and p2, I make these the state variables X[0], X[1], X[2], X[3]
    #ic=[x=0, xdot=0, p1=pa, p2=pa]
    """creating variables 'pa' & 'ic' to args for state variables and initial conditions"""
    pa = myargs[3] # done
    ic = [0, 0, pa, pa] # done # initial conditions

    #call odeint with ode_system as callback
    """Solves ivp for the three ode's"""
    sln = solve_ivp(ode_system, [t[0], t[-1]], ic, t_eval=t, args=myargs)

    #unpack result into meaningful names
    """Creating new variables for the solutions of the ivp and state variables"""
    xvals = sln.y[0]
    xdot = sln.y[1]
    p1 = sln.y[2]
    p2 = sln.y[3]

    #plot the result
    """creating the first plot (plotting xdot as a function of time"""
    plt.subplot(2, 1, 1)
    plt.subplot(2, 1, 1)
    plt.plot(t, xvals, 'r-', label='$x$')
    plt.ylabel('$x$')
    plt.legend(loc='upper left')

    ax2=plt.twinx()
    ax2.plot(t, xdot, 'b-', label=r'$\dot{x}$')   # Corrected an error on this line. python interpreted '\d' as an escape character
    plt.ylabel(r'$\dot{x}$')
    plt.legend(loc='lower right')

    """Using the solution above, we are plotting p1 and p2 together as a function of time"""
    plt.subplot(2,1,2)
    plt.plot(t, p1, 'b-', label='$P_1$')
    plt.plot(t, p2, 'r-', label='$P_2$')
    plt.legend(loc='lower right')
    plt.xlabel('Time, s')
    plt.ylabel('$P_1, P_2 (Pa)$')

    plt.show()
# endregion

# region function calls
if __name__=="__main__":
    main()
# endregion