# Provenance and review limits

The architecture note was prepared from existing project material and code, with ChatGPT, Claude and Gemini assisting the writing. The author participated in the AI-assisted project; this is not a claim of unaided authorship of all implementation code.

Newly authored public material: explanatory prose and two fictional records in an illustrative JSON structure. No original private code, original database schema, real equipment data, client identity, deployment configuration or private file paths are included. The repository license covers these published materials, not the omitted project.

Existing-code observations used for the note:

- Separate per-module backend organization in the earlier version.
- Shared reading persistence and module mapping in the refactored version.
- Required source file and line at the canonical entry; explicit compatibility markers at the legacy entry.
- Separate sustained and burst limits in an in-process upload limiter.

These are source-level observations, not new hardware tests. Legacy adapters existing in code does not prove a successful production migration. The illustrative JSON is not executable evidence of the private implementation. No code-level, end-to-end, safety or final-site acceptance certificate is implied.

Excluded model suggestions: unverified hours spent, maintenance-effort multipliers, guaranteed reader response, and the incorrect claim that hashing a file path keeps its identity stable across renames. A path hash is not a content checksum.

Publication of this existing-work note does not initiate later project work or represent client approval of any future implementation schedule.
