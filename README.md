# CredentialMesh

## Product

Issuers publish credentials with natural-language qualifications and evidence references. Verifiers ask whether a credential satisfies a specific role or access policy; the contract records a scoped, expiring decision and supports issuer revocation.

This is a GenLayer-native protocol, not a backend workflow. Off-chain preparation may collect and display evidence, but the contract owns the lifecycle and only deterministic settlement becomes canonical.

## Why GenLayer is essential

Semantic matching between credential evidence and a policy is nondeterministic; issuer authority, credential IDs, expiry, revocation, policy version, and attestation scope are deterministic. The implementation must make this boundary visible in code, tests, and UI. A normal EVM contract can bind bytes and enforce roles; it cannot independently interpret the meaning of arbitrary source, policy, evidence, or behavior.

## Existing-work exclusion

Not an identity registry or generic credential wallet: the hard primitive is context-bound semantic authorization.|three credential types, one access policy, valid/expired/revoked/misleading evidence paths| It must not become a betting app, grant reviewer, quote verifier, appeal court, creative lineage app, or generic AI dashboard.

## Stack lock

Next.js App Router + TypeScript; genlayer-js@1.1.8; injected EIP-1193 wallet only; Studionet chain ID 61999; RPC https://studio.genlayer.com/api; Python Intelligent Contract; no server signer and no canonical backend database.

## Lifecycle

Issuer registers; credential is committed; verifier supplies policy and context; validators assess fit; bounded attestation is issued; issuer can revoke; expiry is enforced.

## Security invariants

No credential becomes globally valid; attestations are scoped to policy/context; revoked or expired credentials cannot pass; validator prose never becomes authorization.

## Vector Store

Use GenLayer's typed Vector Store for scoped retrieval of policies, source excerpts, manifests, prior decisions, and evidence. Store record ID, kind, source reference, digest, embedding model/version, and bounded excerpt. Retrieval informs the evaluator; similarity alone never authorizes an action.

## MVP proof

## Current implementation note

The deployed contract and frontend use deterministic credential, policy, proposal, challenge, and revocation flows. `settle_review` now uses `gl.nondet.web.get` to fetch declared public evidence and `gl.vm.run_nondet_unsafe` to have validators independently assess the proposed structured decision. Deterministic code still owns credential validity, policy version, authorization, and lifecycle state. The current StudioNet deployment is recorded in `handoff.md`.


