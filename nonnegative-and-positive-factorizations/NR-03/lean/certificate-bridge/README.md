# NR-03 certificate bridge provenance

This directory records the reviewed seven-path bridge overlay applied to the
canonical source package. `INTEGRATION-PATHS.json` names the exact
three changed and four added development paths; the three accompanying
interface/provenance files are copied from that review input.

The package has 58 active Lean modules: the original 57-module complete-row
graph, with `NLA/NR03/Certificate.lean` replaced by the reviewed wrapper and
`NLA/NR03/CertificateBridge.lean` added. The development-only driver and
`SOURCE_INPUTS.json` are not copied into the canonical package. Their exact
source hashes remain in `ACTIVE-MODULE-MANIFEST.json` and the integration-path
receipt.

This is source provenance plus a conditional bridge-only diagnostic receipt.
The diagnostic compiled only the six lightweight modules and all four bridge
helper declarations; it did not compile the complete graph or run Comparator,
the default-kernel replay, or sandbox controls. See
`../reviews/bridge-diagnostic/RECEIPT.json`. No solved-status claim is made.
