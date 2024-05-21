from cffi import FFI
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import kontenery
from kontenery import lib
from kontenery import ffi


#zeby wszytsko miało sens zakładam stałą długość przedziału równą 2
L=2
n=400

def rhs(x):
    return x**4+x**3-7*x**2+4*x



def solve(sol: kontenery.Solution):
    for i in range(0,sol.n_reals):
        sol.set_real_data(rhs(i*L/n),i)
    sol.makeSpectral()
    #teraz sol ma we wspolczynnikach rozwiniecie prawej strony, to bedzie nadpisane
    
    sol.wspolczynniki[0][0]=0.0
    sol.wspolczynniki[0][1]=0.0
    k=1
    i=2
    while i<(sol.n_complex*2):
        real_save=sol.wspolczynniki[0][i]
        sol.wspolczynniki[0][i]=(sol.wspolczynniki[0][i]+np.pi*sol.wspolczynniki[0][i+1]*k)/(1+k*k*np.pi*np.pi)
        sol.wspolczynniki[0][i+1]=(sol.wspolczynniki[0][i+1]-np.pi*real_save*k)/(1+k*k*np.pi*np.pi)

        sol.wspolczynniki[0][0]=sol.wspolczynniki[0][0]-2*sol.wspolczynniki[0][i]
        i=i+2
        k=k+1
    print("")
    print("resault coefficients:")
    sol.print_wspolczynniki()
    
    sol.makePhysical()
    x=np.ndarray(shape=(sol.n_reals+1),dtype=float)
    y=np.ndarray(shape=(sol.n_reals+1),dtype=float)
    x_dense=np.ndarray(shape=(100),dtype=float)
    analityczne=np.ndarray(shape=(100),dtype=float)

    for i in range(0,sol.n_reals):
        x[i]=i*L/sol.n_reals
        y[i]=sol.wartosci[0][i]
    i=sol.n_reals
    x[i]=i*L/sol.n_reals
    y[i]=sol.wartosci[0][0]
    
    for i in range(0,100):
        x_dense[i]=i*L/99
        analityczne[i]=x_dense[i]**4-3*x_dense[i]**3+2*x_dense[i]**2

    plt.plot(x,y,label='numeryczne')
    plt.plot(x_dense,analityczne,label='analityczne')
    plt.legend()
    plt.grid()
    plt.show()




os.chdir('build')
os.system('make')
os.chdir('..')



sol=kontenery.Solution(n)
sol.init_fftw_plans()

solve(sol)