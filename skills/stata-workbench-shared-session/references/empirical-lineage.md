# Empirical evidence and refinement

For native export failures and chapter folders containing actual data, also read
[native export failures and real-file delivery](native-export-and-real-file-delivery.md).

Trace the original manuscript's claims, tables and figures through hashed data,
cleaning/variable code, sample keys, model specifications and actual outputs.
Refinement does not mean deleting text first or automatically rerunning every
model. Inspect every chain; execute only necessary stages within the approved scope.

The installed receipt tool supports:

```bash
python3 scripts/completion_check.py /absolute/stage-receipt --empirical-contract /absolute/trace.json
python3 scripts/empirical_trace.py --input /absolute/trace.json --output /absolute/trace-result.json
```

The empirical contract version 1 is shared with `thesis-refiner`. The bundled
checker performs no study coding and never repairs tolerances. It validates
script/input/output hashes, source/installed/loaded runtime layers, original
session/job, sample membership, table denominators/labels/missingness and declared
numeric comparisons. Unknown loaded state stays unknown. Existing execution,
visibility and replay requirements remain independent.

Equal N is insufficient: compare IDs, couple roles, waves and exclusion rules.
Do not apply questionnaire missing-value recodes to technical IDs. Preserve raw
and historical decoded keys when their provenance differs. Mirror/actor-partner
outputs are not independent evidence, and separate endpoint significance does
not test their difference.

Record Stata storage precision separately from printed decimals and the approved
numeric tolerance. Use `recast double` before introducing centered decimal values
into integer columns. A binary32 label never grants permission to relax a failed
comparison. CI algorithms and requested/saved/valid draws require separate fields.
Normal termination, usable standard errors and convergence are separate checks;
carry any accepted scientific partial into all dependent manuscript claims.

When NLM flags a mismatch, inspect the original stage receipt and local output.
Classify a real error before making a new .do version; confirm partial effects and
rerun only the affected stage. A transport uncertainty must be resolved without
resubmission. Preserve existing frames, user memory, unique logs and old outputs.
Document delivery, evidence closure and complete scientific reproduction are
different results; none can be inferred solely from another agent's callback.
