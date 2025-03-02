# region imports
import hw5a as pta
import random as rnd
import numpy as np
from matplotlib import pyplot as plt
# endregion

# region functions
def ffPoint(Re, rr):
    """
    This function takes Re and rr as parameters and outputs a friction factor according to the following:
    1.  if Re>4000 use Colebrook Equation
    2.  if Re<2000 use f=64/Re
    3.  else calculate a probabilistic friction factor where the distribution has a mean midway between the prediction
        of the f=64/Re and Colebrook Equations and a standard deviation of 20% of this mean
    :param Re:  the Reynolds number
    :param rr:  the relative roughness
    :return:  the friction factor
    """

    """
    These two if functions determines if the Colebrook or Laminar 
    equation should be used based on the value of the Reynolds number.
    """
    if Re>=4000:
        return pta.ff(Re, rr,CBEQN=True)
    if Re<=2000:
        return pta.ff(Re, rr)

    CBff = pta.ff(Re, rr, CBEQN=True)  #prediction of Colebrook Equation in Transition region  # done
    Lamff = pta.ff(Re, rr, CBEQN=False)   #prediction of Laminar Equation in Transition region  # done
    mean=(CBff+Lamff)/2
    sig=0.2*mean
    return rnd.normalvariate(mean, sig)  #use normalvariate to select a number randomly from a normal distribution  # done

def PlotPoint(Re,f):
    """
    This def plots the moody diagram
    Note: I was getting a wierd output where I was getting a moody chart (taken from hw5a)
          and then a second graph with the circle or triangle and a blank white screen as the background.
          That is why I omitted the initial plotting code directly below. Not sure if that was the reason
          why but, it works now,
    :param Re: (Reynolds number):
    :param f: (Friction factor):
    :return:
    """
    #pta.plotMoody(plotPoint=True, pt=(Re,f))
    plt.plot(Re, f, markersize=12, markeredgecolor='red', markerfacecolor='none')
    plt.draw()

def main():
    """
    The moody plot code directly below was added when I was having issues to have it show correctly.
    """
    pta.plotMoody(plotPoint=False, showPlot=False)

    while True:
        try:
            """Asking the user the pipe diameter, roughness, and flow rate"""
            d_in = float(input("Enter pipe diameter (inches): "))
            eps_mic = float(input("Enter pipe roughness (micro inches): "))
            Q_gpm = float(input("Enter flow rate (gallons per minute): "))
        except ValueError:
            print("Invalid input. Try again.")
            continue

        """Below are variables that compute conversion factors or list values of the variable"""
        d_ft = d_in / 12 # ft #diameter conversion to feet
        rr = (eps_mic * 1e-6) / d_in # in/in #relative roughness
        Q_cfs = (Q_gpm * 0.133681) / 60.0 #flow rate conversion to ft^3/s
        A = np.pi * (d_ft / 2) **2 # in^2 #cross sectional area of pipe
        V = Q_cfs / A # ft/s #average velocity
        nu = 1.0e-5 #ft^2/s #kenimatic viscosity
        Re = V * d_ft / nu #Reynolds number
        f = ffPoint(Re, rr) #friction factor
        g = 32.2 # ft*s^-2 #gravity
        hf_per_foot = f * (V**2 / (2 * g)) * (1 / d_ft) #head loss

        """Computes the Reynolds number, Friction factor, and Head loss and shows the values to the user"""
        print("\nCompute Values:")
        print("Reynolds number (Re): {:.2f}".format(Re))
        print("Friction factor (f): {:.5f}".format(f))
        print("Head loss per foot (hf/L): {:.5f} ft/ft".format(hf_per_foot))

        """
        'marker' determines if the indicator on the graph is to be a 
        triangle or circle based on the Reynold's number value.
        Then, it is placed on the moody chart and shown to the user.
        """
        marker = '^' if 2000 < Re < 4000 else 'o'

        plt.plot(Re, f, marker=marker, markersize=12, markeredgecolor='red', markerfacecolor='none')
        plt.draw()

        cont = input("Enter another set of parameters? (y/n): ")
        if cont.lower() != 'y':
            break

    plt.show()

    """
    These were given in the initial code. (Re, rr, f, PlotPoint)
    The way I wrote the code didn't have them in that specific order so I just put '#' 
    to omit and type them back out when they were needed.
    """
    #Re=float(input("Enter the Reynolds number:  "))
    #rr=float(input("Enter the relative roughness:  "))
    #f=ffPoint(Re, rr)
    #PlotPoint(Re, f)
# endregion

# region function calls
if __name__=="__main__":
    main()
# endregion