# Reference Input Intake for Model V&V

Reference material and numerical cases supplied by the project owner are inputs
to requirements definition and conventional software verification and
validation. They do not authorize an agent to invent, calculate, or approve a
Risk of Ruin value.

## What to provide

For each source or dataset, include when available:

- title, author, edition/version, publication date, and stable citation;
- original source URL, DOI, ISBN, accession number, or dataset identifier;
- license and whether redistribution in a public repository is allowed;
- the passages, tables, fields, or cases relevant to the intended requirement;
- units, currencies, timestamps, frequency, and adjustment conventions;
- expected result and acceptable numerical tolerance for validation cases;
- known limitations, corrections, revisions, or disputed interpretations.

## Repository handling

- Redistributable sources and fixtures may be added under `tests/reference/`
  with source metadata and a SHA-256 checksum.
- Copyrighted or licensed material that cannot be publicly redistributed must
  not be committed. Store only its citation, access instructions, checksum where
  lawful, and minimal derived fixtures permitted by its license.
- Credentials, brokerage exports, personal account data, material non-public
  information, and unlicensed market data must not be committed or pasted into
  public GitHub issues.
- Sensitive local material must be redacted or replaced with synthetic cases
  before it enters the development workflow.

## V&V route

Each accepted reference case is mapped to:

1. a uniquely identified requirement;
2. an exact primary source and documented interpretation;
3. deterministic input data and expected output;
4. an automated verification test with an explicit tolerance;
5. independent validation evidence and reviewer identity;
6. the model, policy, code, data, and test versions used;
7. approval status for use in a risk gate.

An agent can help catalog sources, build fixtures, implement tests, and summarize
results. It cannot certify its own risk model or create the authoritative RoR
result.
