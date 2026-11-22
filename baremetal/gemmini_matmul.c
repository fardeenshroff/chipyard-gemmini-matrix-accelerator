/* Integration target for an upstream Gemmini software tree (not host-buildable).
 * Compile with the upstream pinned RISC-V toolchain and Gemmini generated header.
 * API may vary by commit; do not describe as executed until the target build runs.
 */
#include <stdio.h>
#include <stdbool.h>
#include <stdint.h>
#include "gemmini.h"
#define N 16
static elem_t A[N][N] row_align(1);
static elem_t B[N][N] row_align(1);
static elem_t C[N][N] row_align(1);
static int32_t reference[N][N];
int main(void) {
    for (int i=0;i<N;i++)for (int j=0;j<N;j++) {
        A[i][j]=(elem_t)((i+j)%3-1);
        B[i][j]=(elem_t)((i*2+j)%3-1);
        C[i][j]=0;
        reference[i][j]=0;
    }
    for (int i=0;i<N;i++)for (int j=0;j<N;j++)for (int k=0;k<N;k++)
        reference[i][j]+=A[i][k]*B[k][j];
    gemmini_flush(0);
    tiled_matmul_auto(N,N,N,
        (elem_t*)A,(elem_t*)B,NULL,(elem_t*)C,
        N,N,0,N,
        MVIN_SCALE_IDENTITY,MVIN_SCALE_IDENTITY,MVIN_SCALE_IDENTITY,
        NO_ACTIVATION,ACC_SCALE_IDENTITY,0,
        false,false,false,false,false,0,WS);
    gemmini_fence();
    int errors=0;
    for (int i=0;i<N;i++)for (int j=0;j<N;j++) {
        if ((int32_t)C[i][j]!=reference[i][j]) errors++;
    }
    if (errors) {
        printf("GEMMINI_RESULT n=16 status=FAIL errors=%d\n",errors);
        return 1;
    }
    printf("GEMMINI_RESULT n=16 status=PASS errors=0\n");
    return 0;
}
