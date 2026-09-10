# CredentialMesh â€” Handoff Log

Append-only execution log. Record facts, not guesses: files changed, commands, test results, deployment addresses, transaction hashes, and blockers.

## 2026-09-01 â€” Strong replacement pack created

- Replaced the prior concept handoff with a protocol-level design.
- No implementation or deployment has been performed in this folder.
- Next action: inspect current repository contract patterns, implement deterministic storage/state machine, then add direct tests before frontend work.

## 2026-09-05 — Initial end-to-end implementation

- Added Next.js App Router frontend with Embassy archive visual system, palette from supplied reference, responsive operations view, empty/loading/error messaging, proposal dossier drawer, and public read mode.
- Added centralized `src/lib/genlayer.ts` for StudioNet chain configuration and wallet identity plumbing; injected wallet is explicit, browser-wallet mode is surfaced honestly when no imported browser key exists.
- Added `contracts/credential_mesh.py` with target enrollment, policy versioning, credential registration/revocation, proposal/review settlement, challenge, pagination-shaped reads, and append-only audit events.
- Added package/tooling files and `.env.example`.
- Verification pending: install dependencies, run typecheck/build, then deploy and exercise on StudioNet when a CLI account/address is available.

- Verification note: npm registry access was available but the generated node_modules tree remained incomplete/locked; typecheck/build could not run because local tsc/next binaries were absent. No deployment was attempted because the pack has no configured deployer or contract address.

## 2026-09-05 — Deployment-readiness audit

- Corrected the contract to the GenLayer Intelligent Contract shape: pinned `py-genlayer` runtime, `gl.Contract`, public read/write decorators, `gl.message.sender_address`, and deterministic transaction time.
- Added `gltest.config.yaml` with StudioNet as the default network and `scripts/verify-schema.mjs` for deployed call-surface verification.
- `python -m py_compile contracts/credential_mesh.py` passed.
- `genvm-lint check contracts/credential_mesh.py --json` passed AST lint (`ok: true`) with return-annotation warnings; SDK validation was blocked by local cache permission error `WinError 5` while reading the extracted GenVM runtime.
- Deployment is not yet performed; next action is repair the GenVM cache permissions, run SDK validation, then deploy with the GenLayer CLI and set `NEXT_PUBLIC_CREDENTIALMESH_ADDRESS`.

## 2026-09-05 — StudioNet deployment

- Repaired permissions on `C:\Users\DELL\.cache\genvm-linter` and `C:\Users\DELL\.genlayer`.
- Active deployer: `aase-deployer` (`0x3926627Eb9D353e29C7D6f8f914bE96F38631bAB`).
- Deployment transaction: `0x36fdbba8f230fbe54f76e43a01e69f0aef6625fe9817962ea05d5e18751937dd`.
- Contract address: `0x436acD8A031a1Eb916C166cD25B2800C646B9ab0`.
- Receipt status: `ACCEPTED`; result `MAJORITY_AGREE`; 5 validators agreed; GenVM execution result `SUCCESS`.
- Added deployed address to `.env.example` and local `.env.local`.
- Next action: run schema verification and exercise the deployed write surface.

## 2026-09-05 — Corrected StudioNet deployment

- Fixed runtime storage initialization (`audit = []`) and persistent integer typing (`bigint`).
- Corrected deployment transaction: `0x704729d8b5c7e566e07e0f7554de8cc789c03261c4bd87c18d464752f38640b0`.
- Corrected contract address: `0x30A598abE7c7d767F4442550D25c82c4d0bBa3DF`.
- Receipt: `ACCEPTED`, `MAJORITY_AGREE`, 5 validators agreed, leader GenVM execution `SUCCESS`.
- Updated `.env.example` and `.env.local` to the corrected address.

## 2026-09-05 — Full StudioNet lifecycle test

- Final deployed contract: `0xb26303B9f3833618AFaeb9fc4132662382E40Bb7`.
- Verified reads: `get_target`, `get_credential`, `get_proposal`, `list_proposals`, and `list_audit`.
- Verified writes: `enroll_target`, `publish_policy`, `register_credential`, `propose_review`, `settle_review`, `challenge_review`, and `revoke_credential`.
- Real lifecycle state reached: `REVIEWING` → `APPROVED / HIGH` → `CHALLENGED`; credential read back with `revoked: true`.
- Settlement required non-empty CLI arguments; empty-string CLI args caused rollback, documented as a CLI gotcha.
- Final live reads passed and environment files now point to the final address.

## 2026-09-05 — Web Access and equivalence deployment

- Added source-grounded evaluator to `settle_review`: bounded public evidence fetch via `gl.nondet.web.get`, leader extraction via `gl.nondet.exec_prompt`, and independent validator acceptance via `gl.vm.run_nondet_unsafe`.
- Deployed contract: `0x9438e8B9266145c9c3f915152aA94F84f8Da11A6`.
- Deployment transaction: `0x11cda6b2ebdd75e088030aa4ad79537bfd377ba6e25a2ac2d2f75ffbc91abbae`.
- Deployment receipt: `ACCEPTED`, `MAJORITY_AGREE`, 5 validators; leader GenVM execution `SUCCESS`.
- Updated environment files and README to the new contract address and consensus behavior.

## 2026-09-05 — Web Access full-cycle verification

- Fresh deterministic setup passed on `0x9438e8B9266145c9c3f915152aA94F84f8Da11A6`: target enrollment, policy publication, credential registration, and proposal creation all returned `ACCEPTED` and were visible in subsequent reads.
- Fresh non-deterministic settlement passed: `settle_review` fetched `https://example.org` with `gl.nondet.web.get`, ran the bounded prompt/equivalence validator path, and committed `ABSTAINED / LOW` with `policy_fit: insufficient_evidence`.
- Stored rationale correctly identified the placeholder source as insufficient and did not approve based only on the credential qualification string.
- Final live `get_proposal` and `list_audit` reads passed; this verifies the Web Access path is fail-closed and consensus-backed.

## 2026-09-07 — Final submission-readiness verification

- Final deployed contract: `0x287f8A91E9AA4ef39cdBc65B130E88921A54771d`.
- Deployment transaction: `0xdcadbae294b782ebd1fb43fc7135613696a2353b6ac76d98b78a8487b298cd76`; receipt `FINALIZED`, `MAJORITY_AGREE`, leader GenVM execution `SUCCESS`.
- GitHub baseline: `176d5fa` before this wallet-only pass; subsequent wallet provider changes are uncommitted pending production-browser verification.
- Pending settlement `0xe47a6b8bcf608f2059b64e569df3271a422089167c394b3032316ac47259ed92` finalized with `MAJORITY_AGREE`; leader GenVM execution `SUCCESS`; persisted proposal `fresh-review-20260907` is `REJECTED / HIGH`.
- Settlement readback: source digest `ff67a9d764d6a2367a187734e697f6a53217db9a21c101d410a113ca871a299d`, evidence `evidence_1`, rationale states Example Domain does not evidence a qualification. Challenge deadline remained `0` because approval was not reached.
- `is_credential_authorized(fresh-credential-20260907, fresh-target-20260907, 2)` read back `false`.
- Fresh lifecycle writes accepted on the exact contract: target enrollment tx `0x7643c74b316f1add780ab80acdfdc5df1d1d1ff12500b1f1e6cba5920f234868`; policy/credential/proposal writes were read back successfully. The earlier mixed-address attempt was rejected with `EXPECTED: unknown target` and is not treated as evidence.
- Schema verifier: all 17 methods passed. GenVM lint passed with return-annotation warnings. TypeScript typecheck passed before the final provider refactor; production build was started but did not emit a completion result in the local process.
- Browser wallet provider refactor is present locally: injected writes pass `window.ethereum` to `createClient`; local browser wallet export/disconnect helpers are present. A real write from the Vercel production UI and a Vercel deployment receipt were not verified in this environment.

## 2026-09-10 — Clean final contract and MIN follow-up

- Final clean contract: `0x6CB6024731Fe65C84A8DF300cCD43d4decd9A3f2`.
- Deployment transaction: `0xef04ee3366a05442d18bab8b750d2fa03cb0bd4e773c1135e9c48980e115060f`; receipt `ACCEPTED`, consensus `MAJORITY_AGREE`, deployment GenVM execution `SUCCESS`.
- Clean lifecycle setup used correctly separated arguments. Enrollment readback succeeded; issuer registration, source-authority registration, policy publication, attestation, credential registration, and proposal creation were then verified on the same contract.
- Settlement transaction: `0x8f877077c821f9c49a50c507812d26ccc65d3dd441d99a2b1e5777b25105d4bc`; receipt `ACCEPTED`, consensus `MAJORITY_AGREE`, leader GenVM execution `SUCCESS`.
- Settlement readback: proposal `clean-review` persisted as `ABSTAINED / HIGH`; source digest matched `ff67a9d764d6a2367a187734e697f6a53217db9a21c101d410a113ca871a299d`; authorization read returned `false`.
- Revocation readback: credential `clean-credential` persisted with `revoked: true`; authorization remained `false`.
- Schema verifier: 21 methods verified. Python compilation, behavioral tests, TypeScript typecheck, and production Next.js build passed locally.
- Follow-up fixes: source attestation is mandatory before credential registration; challenge validators require independent `uphold` equality with the leader conclusion; policy and proposal-bound authorization reads are exposed in the UI.

## 2026-09-10 — Canonical deployment

- Canonical contract: `0xF7d4B16634915E474e3c522DdB069a7275600964` on StudioNet chain `61999`.
- Deployment transaction: `0x23055be3703a5c8a80dc39021a64ae92f3fd0bb7a388bb7592bded6db0eeec27`; receipt `ACCEPTED`, consensus `MAJORITY_AGREE`, GenVM execution `SUCCESS`.
- `.env.example`, README, schema verifier input, and Explorer evidence now point to this deployment. Schema count: 21 methods.
- Verification: GenVM lint passed (`ok: true`, return-annotation warnings only); Python compilation passed; behavioral contract-state tests passed; TypeScript typecheck passed; production build passed.
- This address supersedes all earlier deployments in this append-only log; earlier entries remain historical evidence only.

## 2026-09-10 — Real contract behavior tests

- Removed the `MeshModel` imitation tests.
- Exact command: `gltest -q tests/test_contract_behavior.py`.
- Result: `2 passed in 0.24s`.
- These tests deploy and execute `contracts/credential_mesh.py` through the direct GenLayer VM, covering mandatory source attestation/digest binding and proposal-bound authorization before finalization. They fail on broken real contract methods.
