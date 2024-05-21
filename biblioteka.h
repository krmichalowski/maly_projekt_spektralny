
double** init_double_pointer_pointer();

void fftw_init(int n,double** wartosc,double** wspolczynniki,double** fftw_plan_pointer,double** fftw_invers_plan_pointer);

void py_fftw_execute(double** fftw_plan_pointer);

void py_fftw_invers_execute(double** fftw_invers_plan_pointer);