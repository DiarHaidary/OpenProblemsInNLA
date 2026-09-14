# Certificate format and interpretation

The `certificates/rankM.npz` files are ordinary NumPy archives, readable without pickle. The array named `roots` contains **centers**, not exact algebraic root coordinates. It has shape `(q,(2*M)^2)` and dtype `complex128`, with matrix entries flattened in row-major order. `U` stores the data in the original, ordinary-Frobenius coordinates. Every binary64 real or imaginary component of a center or data entry is interpreted as the exact dyadic rational represented by those bits.

`certificates/data_matrices.json` also lists every data entry as an exact dyadic numerator and denominator exponent, independently of NumPy file loading.

The optional integer array `radius_exponents` records radii from certificate generation. A radius exponent `k` denotes the exact complex maximum-norm ball of radius `2^k` about the center. The final verification command does **not** trust this field: it recomputes an inverse proposal, independently reconstructs the exact polynomial system and Jacobian, obtains fresh bounds, checks contraction, and checks separation for its freshly obtained balls. No numerical residual is used as a substitute for an exact inequality.

A passed contraction test proves a unique simple zero in its ball. The exact disjointness check proves that all those zeros are distinct. The implicit-function theorem transfers their number as a lower bound to the generic degree. None of these assertions proves that the supplied balls cover the entire complex critical fiber.

`final_rankM_verification.json` records the C++ multiprecision-integer rerun. `independent_rankM_all.json` records the separate Python integer/fraction contraction rerun on **all** final centers. The latter does not import or call the C++ checker; it does share the numerical inverse-proposal routine and the exact separation helper. The shared inverse proposal is not trusted by either contraction checker. The source and results are not represented as an independent external referee review.

Each final result records the SHA-256 hash of the exact input archive it verified. The `SHA256SUMS` manifest supplies an additional file-integrity check. Hashes do not prove mathematical correctness.

Any displayed decimal bounds are informational approximations. Exact acceptance uses integers and fractions. Aggregate maxima of different quantities may occur at different roots and must not be multiplied together to reconstruct a single-root test.
