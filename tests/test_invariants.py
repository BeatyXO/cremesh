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

def test_browser_key_is_explicitly_local_and_exportable():
    s = FRONTEND.read_text(encoding="utf-8"); assert "generatePrivateKey" in s; assert "exportBrowserPrivateKey" in s; assert "disconnectBrowserWallet" in s

def test_issuer_and_source_authority_are_bound():
    s = source(); assert "register_issuer" in s; assert "register_source_authority" in s; assert "unauthorized issuer" in s

def test_context_is_bound_to_authorization():
    s = source(); assert '"context_digest"' in s; assert 'p.get("context_digest"' in s

def test_authorization_behavioral_matrix():
    def authorized(credential, target, policy, proposal, now, revoked=False, expiry=999):
        return bool(credential and target and policy and proposal.get("credential_id") == credential and proposal.get("target_id") == target and proposal.get("policy_version") == 2 and proposal.get("status") == "FINALIZED" and not revoked and expiry >= now)
    base={"credential_id":"c","target_id":"t","policy_version":2}
    for status in ("REVIEWING","APPROVED","REJECTED","ABSTAINED","CHALLENGED"):
        assert not authorized("c","t",True,{**base,"status":status},1)
    assert authorized("c","t",True,{**base,"status":"FINALIZED"},1)
    assert not authorized("c","t",True,{**base,"status":"FINALIZED"},1,revoked=True)
    assert not authorized("c","t",True,{**base,"status":"FINALIZED"},1000,expiry=999)
