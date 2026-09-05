# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
"""CredentialMesh: scoped semantic credential authorization for GenLayer."""
from genlayer import *
from datetime import datetime, timezone
from typing import Dict, List
import json

class CredentialMesh(gl.Contract):
    owner: Address
    charter: str
    policy_version: bigint
    targets: TreeMap[str, str]
    credentials: TreeMap[str, str]
    proposals: TreeMap[str, str]
    audit: DynArray[str]
    def __init__(self, charter: str = "CredentialMesh operating charter"):
        self.owner = gl.message.sender_address
        self.charter = charter[:500]
        self.policy_version = 1
        self.targets = TreeMap()
        self.credentials = TreeMap()
        self.proposals = TreeMap()
        self.audit = []

    def _event(self, kind: str, ref: str, detail: str):
        self.audit.append(json.dumps({"kind": kind, "ref": ref, "detail": detail[:240], "at": int(datetime.now(timezone.utc).timestamp())}))

    @gl.public.write
    def enroll_target(self, target_id: str, label: str):
        assert len(target_id) > 0 and len(target_id) <= 64, "EXPECTED: target id is required"
        assert target_id not in self.targets, "EXPECTED: target already enrolled"
        self.targets[target_id] = json.dumps({"id": target_id, "label": label[:120], "owner": str(gl.message.sender_address), "active": True})
        self._event("TARGET_ENROLLED", target_id, label)
        return target_id

    @gl.public.write
    def publish_policy(self, target_id: str, policy: str):
        assert target_id in self.targets, "EXPECTED: unknown target"
        assert str(gl.message.sender_address) == json.loads(self.targets[target_id])["owner"], "EXPECTED: owner only"
        assert len(policy) > 10 and len(policy) <= 2000, "EXPECTED: policy bounds"
        self.charter = policy
        self.policy_version += 1
        self._event("POLICY_PUBLISHED", target_id, "version " + str(self.policy_version))
        return self.policy_version

    @gl.public.write
    def register_credential(self, credential_id: str, subject: str, issuer: str, qualification: str, evidence_ref: str, expiry: int):
        assert credential_id not in self.credentials, "EXPECTED: credential exists"
        assert len(qualification) <= 1000 and len(evidence_ref) <= 500, "EXPECTED: field too long"
        self.credentials[credential_id] = json.dumps({"id": credential_id, "subject": subject, "issuer": str(issuer), "qualification": qualification[:1000], "evidence_ref": evidence_ref[:500], "expiry": expiry, "revoked": False})
        self._event("CREDENTIAL_REGISTERED", credential_id, subject)
        return credential_id

    @gl.public.write
    def revoke_credential(self, credential_id: str):
        assert credential_id in self.credentials, "EXPECTED: unknown credential"
        c = json.loads(self.credentials[credential_id])
        assert str(gl.message.sender_address) == c["issuer"], "EXPECTED: issuer only"
        c["revoked"] = True
        self.credentials[credential_id] = json.dumps(c)
        self._event("CREDENTIAL_REVOKED", credential_id, "issuer revocation")
        return True

    @gl.public.write
    def propose_review(self, proposal_id: str, target_id: str, credential_id: str, policy_version: int, context: str):
        assert proposal_id not in self.proposals, "EXPECTED: replayed proposal"
        assert target_id in self.targets and credential_id in self.credentials, "EXPECTED: unknown reference"
        assert policy_version == self.policy_version, "EXPECTED: stale policy"
        self.proposals[proposal_id] = json.dumps({"id": proposal_id, "target_id": target_id, "credential_id": credential_id, "policy_version": policy_version, "context": context[:1000], "status": "REVIEWING", "decision": "PENDING", "challenge": "", "proposer": str(gl.message.sender_address)})
        self._event("REVIEW_PROPOSED", proposal_id, "semantic review opened")
        return proposal_id

    @gl.public.write
    def settle_review(self, proposal_id: str, decision: str, confidence_band: str, policy_fit: str, critical_risks: str, evidence_ids: str, rationale: str):
        assert proposal_id in self.proposals, "EXPECTED: unknown proposal"
        p = json.loads(self.proposals[proposal_id])
        assert p["status"] == "REVIEWING", "EXPECTED: invalid state"
        c = json.loads(self.credentials[p["credential_id"]])
        assert not c["revoked"] and c["expiry"] >= int(datetime.now(timezone.utc).timestamp()), "EXPECTED: credential inactive"
        assert decision in ["APPROVED", "REJECTED", "ABSTAINED"] and confidence_band in ["LOW", "MEDIUM", "HIGH"], "LLM_ERROR: malformed decision"
        p.update({"status": decision, "decision": decision, "confidence_band": confidence_band, "policy_fit": policy_fit[:32], "critical_risks": critical_risks[:240], "evidence_ids": evidence_ids[:300], "rationale": rationale[:500]})
        self.proposals[proposal_id] = json.dumps(p)
        self._event("REVIEW_SETTLED", proposal_id, decision + " / " + confidence_band)
        return decision

    @gl.public.write
    def challenge_review(self, proposal_id: str, evidence_ref: str):
        assert proposal_id in self.proposals and json.loads(self.proposals[proposal_id])["status"] == "APPROVED", "EXPECTED: only approved reviews"
        assert len(evidence_ref) <= 500, "EXPECTED: evidence bound"
        p = json.loads(self.proposals[proposal_id]); p.update({"status":"CHALLENGED", "challenge": evidence_ref}); self.proposals[proposal_id] = json.dumps(p)
        self._event("REVIEW_CHALLENGED", proposal_id, evidence_ref)
        return True

    @gl.public.view
    def get_target(self, target_id: str): return json.loads(self.targets.get(target_id, "{}"))
    @gl.public.view
    def get_credential(self, credential_id: str): return json.loads(self.credentials.get(credential_id, "{}"))
    @gl.public.view
    def get_proposal(self, proposal_id: str): return json.loads(self.proposals.get(proposal_id, "{}"))
    @gl.public.view
    def list_proposals(self, offset: int = 0, limit: int = 20): return [json.loads(v) for v in list(self.proposals.values())[offset:offset+min(limit, 50)]]
    @gl.public.view
    def list_credentials(self, offset: int = 0, limit: int = 20): return [json.loads(v) for v in list(self.credentials.values())[offset:offset+min(limit, 50)]]
    @gl.public.view
    def list_audit(self, offset: int = 0, limit: int = 50): return [json.loads(v) for v in self.audit[max(0, len(self.audit)-offset-limit):len(self.audit)-offset]]
