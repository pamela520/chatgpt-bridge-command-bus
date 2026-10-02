# ChatGPT Bridge Command Bus

Public transport-only repository for encrypted ChatGPT Bridge command and result envelopes.

- Public by design.
- Command and result bodies must remain encrypted.
- Do not commit credentials, bearer tokens, private keys, browser data, local secrets, or plaintext local-device commands/results.
- The canonical command slot is `queue/command.json` on branch **`commands`**.
- Results are written as `results/<requestId>.json` on branch **`results`**.
- The Agent polls only `commands`; result commits must never modify that branch.
- Do not stage Blender scripts, payloads, documentation, or unrelated files on `commands`.
- `bridge-public.pem` is the Bridge command-encryption **public** key; the matching private key never belongs in this repository.
- Repository write permission authorizes command publication; the local Bridge agent independently rechecks expiry, device targeting, permission class, destructive confirmation, lockdown state, method existence, and replay state.

Source, bootstrap contract, and security model are maintained in the private `pamela520/work` Bridge project.


Large one-off scripts should travel inside the encrypted Bridge command path rather than being committed as repository payloads. The `main` branch is non-operational/historical; normal command traffic belongs on `commands`, and encrypted replies belong on `results`.
