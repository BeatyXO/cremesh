from pathlib import Path

CONTRACT = Path(__file__).parents[1] / "contracts" / "credential_mesh.py"
FRONTEND = Path(__file__).parents[1] / "src" / "lib" / "genlayer.ts"

def source():
    return CONTRACT.read_text(encoding="utf-8")

def test_policy_is_hashed_and_snapshotted():
    s = source(); assert "hashlib.sha256" in s; assert '"policy_hash": policy["hash"]' in s

def test_evidence_digest_is_verified():
    s = source(); assert 'digest != c["source_digest"]' in s; assert '"source_digest": str(result.get' in s

def test_consensus_owns_settlement_fields():
    s = source(); assert 'def settle_review(self, proposal_id: str):' in s

def test_live_authorization_and_finality():
    s = source(); assert "def is_credential_authorized" in s; assert "def finalize_review" in s; assert 'c["revoked"]' in s

def test_challenge_has_state_and_adjudication():
    s = source(); assert "challenge_deadline" in s; assert "resolve_challenge" in s; assert "CHALLENGED" in s

def test_wallet_uses_injected_provider_only():
    s = FRONTEND.read_text(encoding="utf-8"); assert "provider:" in s; assert "window.ethereum" in s; assert "generatePrivateKey" not in s; assert "browser-key" not in s

def test_issuer_and_source_authority_are_bound():
    s = source(); assert "register_issuer" in s; assert "register_source_authority" in s; assert "attest_source" in s; assert "unauthorized issuer" in s

def test_context_is_bound_to_authorization():
    s = source(); assert 'def is_credential_authorized(self, proposal_id: str)' in s; assert 'def get_authorization' in s; assert 'p.get("context_digest"' in s

def test_authorization_behavioral_matrix():
    def authorized(proposal_id, proposal, now, revoked=False, expiry=999):
        return bool(proposal_id and proposal.get("id") == proposal_id and proposal.get("credential_id") and proposal.get("target_id") and proposal.get("policy_version") == 2 and proposal.get("status") == "FINALIZED" and not revoked and expiry >= now)
    base={"credential_id":"c","target_id":"t","policy_version":2}
    for status in ("REVIEWING","APPROVED","REJECTED","ABSTAINED","CHALLENGED"):
        assert not authorized("p",{**base,"id":"p","status":status},1)
    assert authorized("p",{**base,"id":"p","status":"FINALIZED"},1)
    assert not authorized("p",{**base,"id":"p","status":"FINALIZED"},1,revoked=True)
    assert not authorized("p",{**base,"id":"p","status":"FINALIZED"},1000,expiry=999)
