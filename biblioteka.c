#include<stdio.h>
#include<fftw3.h>
#include<stdlib.h>
#include"biblioteka.h"

double** init_double_pointer_pointer()
{
    return (double**)malloc(sizeof(double*));
}

void init_data(int n,double**wartosc,double**wspolczynniki)
{
    double* tmp_wartosci=(double*)fftw_malloc(n*sizeof(double));
    fftw_complex* tmp_wspolczynniki=(fftw_complex*)fftw_malloc(((n/2)+1)*sizeof(fftw_complex));
    wartosc[0]=tmp_wartosci;
    wspolczynniki[0]=(double*)tmp_wspolczynniki;
}

void fftw_init(int n,double**wartosc,double**wspolczynniki,double** fftw_plan_pointer,double** fftw_invers_plan_pointer)
{
    //n to bedize rozmiar tego wiekszego czyli tablicy real, complex bedzie n/2+1
    fftw_complex* wspolczynniki_casted=(fftw_complex*)(wspolczynniki[0]);
    fftw_plan* tmp_fftw_plan=(fftw_plan*)malloc(sizeof(fftw_plan));
    tmp_fftw_plan[0]=fftw_plan_dft_r2c_1d(n,wartosc[0],wspolczynniki_casted,FFTW_ESTIMATE);
    fftw_plan_pointer[0]=(double*)tmp_fftw_plan;

    fftw_plan* tmp_fftw_invers_plan=(fftw_plan*)malloc(sizeof(fftw_plan));
    tmp_fftw_invers_plan[0]=fftw_plan_dft_c2r_1d(n,wspolczynniki_casted,wartosc[0],FFTW_ESTIMATE);
    fftw_invers_plan_pointer[0]=(double*)tmp_fftw_invers_plan;
}

void py_fftw_execute(double** fftw_plan_pointer)
{
    fftw_execute(((fftw_plan*)(fftw_plan_pointer[0]))[0]);
    printf("done fftw\n");
}

void py_fftw_invers_execute(double** fftw_invers_plan_pointer)
{
    fftw_execute(((fftw_plan*)(fftw_invers_plan_pointer[0]))[0]);
    printf("done invers fftw\n");
}