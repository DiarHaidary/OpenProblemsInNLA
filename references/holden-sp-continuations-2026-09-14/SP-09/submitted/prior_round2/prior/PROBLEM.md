# The target and the unresolved step

For normal n-by-n complex matrices A,B, write

    delta_n(A,B) = min_{U unitary} ||A - U B U*||_op.

SP-09 asks whether, for every n >= 3 and integer k >= 2,

    delta_nk(I_k tensor A, I_k tensor B) = delta_n(A,B).

Using U* B U instead of U B U* gives the same minimum. Likewise, I_k tensor A and A tensor I_k are unitarily equivalent by a fixed permutation. The manuscript uses A tensor I_k to make the spectral blocks explicit.

Repeating a base minimizing unitary proves the less-than-or-equal direction for all matrices. The unresolved direction requires ruling out an improvement by arbitrary unitaries that mix the repeated copies. Equality of bottleneck spectral matching under repetition does not supply this direction, because normal-matrix orbit distance can be strictly smaller than matching distance.

This package proves that reverse inequality for the explicit Krause three-point pair, with equality rigidity, and for further stated subclasses. It does not provide the reverse inequality for every normal pair or a certified counterexample to it.
