/* Exhaustive search over F_P: is target T in the span of <= n of the given N vectors?
   Input (stdin): P dim N n, then N vectors (dim ints each), then target (dim ints).
   DFS over increasing index subsets, pruning linearly dependent extensions (valid: if T is in the span of
   an n-subset, it is in the span of an independent sub-subset, all of whose prefixes are independent).
   Output: number of independent subsets (of size <= n) whose span contains T and which are minimal along
   the DFS path (i.e. residual first becomes 0 at the last added vector), plus node counts. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXD 40
#define MAXN 200
static int P, dim, N, n;
static int V[MAXN][MAXD], T[MAXD];
static int rows[MAXD][MAXD], piv[MAXD];
static int res[MAXD+1][MAXD];
static int inv[64];
static long long nodes = 0, found = 0, foundsize[MAXD+1];
static int chosen[MAXD];
static int maxprint = 5;
static void dfs(int depth, int start) {
  for (int j = start; j < N; j++) {
    int w[MAXD];
    memcpy(w, V[j], sizeof(int)*dim);
    for (int b = 0; b < depth; b++) {
      int c = w[piv[b]];
      if (c) { int *r = rows[b]; for (int t = 0; t < dim; t++) w[t] = (w[t] + (P - c) * r[t]) % P; }
    }
    int pc = -1;
    for (int t = 0; t < dim; t++) if (w[t]) { pc = t; break; }
    if (pc < 0) continue; /* dependent */
    nodes++;
    int iv = inv[w[pc]];
    for (int t = 0; t < dim; t++) w[t] = (w[t] * iv) % P;
    int *rs = res[depth], *rn = res[depth+1];
    int c = rs[pc];
    int zero = 1;
    for (int t = 0; t < dim; t++) { rn[t] = (rs[t] + (P - c) * w[t]) % P; if (rn[t]) zero = 0; }
    chosen[depth] = j;
    if (zero) {
      found++; foundsize[depth+1]++;
      if (maxprint > 0) { maxprint--; printf("FOUND size %d:", depth+1); for (int b = 0; b <= depth; b++) printf(" %d", chosen[b]); printf("\n"); }
      continue;
    }
    if (depth + 1 < n) {
      memcpy(rows[depth], w, sizeof(int)*dim); piv[depth] = pc;
      dfs(depth + 1, j + 1);
    }
  }
}
int main(void) {
  if (scanf("%d %d %d %d", &P, &dim, &N, &n) != 4) return 1;
  for (int i = 0; i < N; i++) for (int t = 0; t < dim; t++) { scanf("%d", &V[i][t]); V[i][t] = ((V[i][t] % P) + P) % P; }
  for (int t = 0; t < dim; t++) { scanf("%d", &T[t]); T[t] = ((T[t] % P) + P) % P; }
  for (int a = 1; a < P; a++) for (int b = 1; b < P; b++) if (a * b % P == 1) inv[a] = b;
  memcpy(res[0], T, sizeof(int)*dim);
  int allz = 1; for (int t = 0; t < dim; t++) if (T[t]) allz = 0;
  if (allz) { printf("target is zero\n"); return 0; }
  dfs(0, 0);
  printf("P=%d dim=%d N=%d n=%d nodes=%lld found=%lld", P, dim, N, n, nodes, found);
  for (int s = 1; s <= n; s++) if (foundsize[s]) printf(" [size %d: %lld]", s, foundsize[s]);
  printf("\n");
  return 0;
}
