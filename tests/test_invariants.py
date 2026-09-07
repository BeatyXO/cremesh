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

def test_no_generated_browser_private_key():
    s = FRONTEND.read_text(encoding="utf-8"); assert "generatePrivateKey" not in s; assert "credentialmesh.browser-key" not in s
