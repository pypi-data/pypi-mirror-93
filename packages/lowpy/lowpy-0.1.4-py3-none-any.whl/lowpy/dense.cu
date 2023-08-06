#include <stdio.h>

__global__ void propagate(
    const   int                     I,
    const   int                     iteration,
    const   double  * __restrict__  x,
    const   double  * __restrict__  w,
    const   double  * __restrict__  b,
            double  * __restrict__  y,
            double  * __restrict__  z
){
    int v = blockIdx.x;
    int j = blockIdx.y;
    int J = gridDim.y;
    double sum = 0;
    int inputIdx = 0;
    if (iteration > -1){
        inputIdx = iteration * I;
    }
    for (int i = 0; i < I; i++) sum += x[inputIdx+i]*w[v*J*I+j*I+i];
    y[v*J+j] = sum + b[v*J+j];
    z[v*J+j] = 1/(1 + exp(-y[v*J+j]));
}
__global__ void backpropagate(
    const   int                     iteration,
    const   int                     label,
            double * __restrict__   dedz,
    const   double * __restrict__   z,
    const   int                     J_n,
            double * __restrict__   w_n,
    const   double * __restrict__   dedz_n,
    const   double * __restrict__   dzdy_n,
            double * __restrict__   dzdy,
    const   double * __restrict__   alpha,
    const   int                     I,
            double * __restrict__   b,
            double * __restrict__   w,
    const   double * __restrict__   x,
    const   double * __restrict__   beta,
            double * __restrict__   mb,
            double * __restrict__   mw
){
    int v   = blockIdx.x;
    int j   = blockIdx.y;
    int J   = gridDim.y;
    int I_n = gridDim.y;
    int inputIdx = 0;
    if (iteration > -1){
        inputIdx = iteration * I;
    }
    if (label > -1){
        if (j == label){
            dedz[v*J+j] = z[v*J+j] - 1;
        }else{
            dedz[v*J+j] = z[v*J+j] - 0;
        }
    }else{
        double sum = 0;
        for (int j_n = 0; j_n < J_n; j_n++) sum += w_n[v*J_n*I_n+j+j_n*I_n] * dedz_n[v*J_n+j_n] * dzdy_n[v*J_n+j_n];
        dedz[v*J+j] = sum;
    }
    dzdy[v*J+j] = z[v*J+j] * (1 - z[v*J+j]);
    // b[l*J+j]   -= (beta[l] * mb[l*J+j] + alpha[l] * dedz[l*J+j] * dzdy[l*J+j]);
    // mb[l*J+j]  = (beta[l] * mb[l*J+j] + alpha[l] * dedz[l*J+j] * dzdy[l*J+j]);
    mb[v*J+j]  = beta[v] * mb[v*J+j] + alpha[v] * dedz[v*J+j] * dzdy[v*J+j];
    b[v*J+j]   -= mb[v*J+j];
    

    for (int i = 0; i < I; i++){
        //w[l*J*I+j*I+i]     -= (beta[l] * mw[l*J*I+j*I+i] + alpha[l] * dedz[l*J+j] * dzdy[l*J+j] * x[inputIdx+i]);
        //mw[l*J*I+j*I+i]     = (beta[l] * mw[l*J*I+j*I+i] + alpha[l] * dedz[l*J+j] * dzdy[l*J+j] * x[inputIdx+i]);
        mw[v*J*I+j*I+i]   = beta[v] * mw[v*J*I+j*I+i] + alpha[v] * dedz[v*J+j] * dzdy[v*J+j] * x[inputIdx+i];
        w[v*J*I+j*I+i]    -= mw[v*J*I+j*I+i];
        
    }
}
__global__ void argmax(
        const   int                     label,
        const   double  * __restrict__  z,
                int     * __restrict__  hits
){
    int v = blockIdx.x;
    int j = blockIdx.y;
    int J = gridDim.y;
    if (j == 0){
        double maxVal = 0;
        int maxIdx = 0;
        for (int i = 0; i < J; i++){
            if (z[v*J+i] > maxVal){
                maxIdx = i;
                maxVal = z[v*J+i];
            }
        }
        if (maxIdx == label){
            hits[v] += 1;
        }
    }
}