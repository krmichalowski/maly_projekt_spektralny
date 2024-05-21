from cffi import FFI
import numpy as np



ffi=FFI()
lib=ffi.dlopen('build/libFFTW_python.so')


ffi.cdef('''
         double** init_double_pointer_pointer();
         ''')
ffi.cdef('''
         void init_data(int n,double**wartosc,double**wspolczynniki);
         ''')
ffi.cdef('''
         void fftw_init(int n,double**wartosc,double**wspolczynniki,double** fftw_plan_pointer,double** fftw_invers_plan_pointer);
         ''')
ffi.cdef('''
         void py_fftw_execute(double** fftw_plan_pointer);
         ''')
ffi.cdef('''
         void py_fftw_invers_execute(double** fftw_invers_plan_pointer);
         ''')


class Solution:
    def __init__(self,n_reals):
        self.wartosci=ffi.new('double**')
        self.wspolczynniki=ffi.new('double**')
        self.n_reals=n_reals
        self.n_complex=int(n_reals/2+1)

        self.wartosci=lib.init_double_pointer_pointer()
        self.wspolczynniki=lib.init_double_pointer_pointer()

        lib.init_data(n_reals,self.wartosci,self.wspolczynniki)

    def pass_real_data(self):
        return self.wartosci

    def pass_complex_data(self):
        return self.wspolczynniki
    
    def init_fftw_plans(self):
        self.fftw_plan_pointer=ffi.new('double**')
        self.fftw_plan_pointer=lib.init_double_pointer_pointer()
        self.fftw_invers_plan_pointer=ffi.new('double**')
        self.fftw_invers_plan_pointer=lib.init_double_pointer_pointer()

        lib.fftw_init(self.n_reals,self.wartosci,self.wspolczynniki,self.fftw_plan_pointer,self.fftw_invers_plan_pointer)
    
    def makeSpectral(self):
        lib.py_fftw_execute(self.fftw_plan_pointer)
        
        for i in range(0,self.n_complex*2):  #razy dwa bo dostaje sie do complex jak do doubli ktore sa obok siebie, tu jest normalizacja wspolczynnikow
            self.wspolczynniki[0][i]=self.wspolczynniki[0][i]/self.n_reals
    
    def makePhysical(self):
        lib.py_fftw_invers_execute(self.fftw_invers_plan_pointer)
    
    def print_wartosci(self):
        for i in range(0,self.n_reals):
            print(self.wartosci[0][i])
    
    def print_wspolczynniki(self):
        i=0
        while i<(self.n_complex*2):
            txt="({:},{:})".format(self.wspolczynniki[0][i],self.wspolczynniki[0][i+1])
            print(txt)
            i=i+2
    
    def set_real_data(self,real,indeks):
        self.wartosci[0][indeks]=real
    
    def set_complex_data(self,real,imag,indeks):
        i=2*indeks
        self.wartosci[0][i]=real
        self.wartosci[0][i+1]=imag

