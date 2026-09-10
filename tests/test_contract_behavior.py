import pytest
import hashlib
import json


def test_real_contract_requires_attestation_and_binds_credential(direct_vm, direct_deploy):
    mesh = direct_deploy("contracts/credential_mesh.py")
    from genlayer.py.types import Address
    owner = Address(direct_vm.sender)
    mesh.enroll_target("target", "Target")
    mesh.register_issuer("issuer", owner)
    mesh.register_source_authority("source", owner)
    with pytest.raises(AssertionError, match="source attestation required"):
        mesh.register_credential("credential", "issuer", "Subject", "Qualification", "https://example.org", "digest1234", "source", 9999999999)
    mesh.attest_source("source", "https://example.org", "digest1234")
    mesh.register_credential("credential", "issuer", "Subject", "Qualification", "https://example.org", "digest1234", "source", 9999999999)
    assert mesh.get_credential("credential")["source_digest"] == "digest1234"


def test_real_contract_authorization_requires_finalized_matching_proposal(direct_vm, direct_deploy):
    mesh = direct_deploy("contracts/credential_mesh.py")
    from genlayer.py.types import Address
    owner = Address(direct_vm.sender)
    mesh.enroll_target("target", "Target")
    mesh.register_issuer("issuer", owner)
    mesh.register_source_authority("source", owner)
    mesh.attest_source("source", "https://example.org", "digest1234")
    mesh.register_credential("credential", "issuer", "Subject", "Qualification", "https://example.org", "digest1234", "source", 9999999999)
    mesh.publish_policy("target", "Qualification must match the requested role.")
    mesh.propose_review("proposal", "target", "credential", 2, "role=engineer")
    assert mesh.is_credential_authorized("proposal") is False
    assert mesh.get_authorization("proposal")["authorized"] is False
    proposal = mesh.get_proposal("proposal")
    assert proposal["status"] == "REVIEWING"
    assert proposal["policy_hash"] == mesh.get_policy("target", 2)["hash"]


def test_real_contract_full_settlement_challenge_finalization_authorization_and_revocation(
    direct_vm, direct_deploy, direct_bob
):
    """Exercise the real contract lifecycle, including nondeterministic paths."""
    mesh = direct_deploy("contracts/credential_mesh.py")
    from genlayer.py.types import Address

    owner = Address(direct_vm.sender)
    challenger = Address(direct_bob)
    evidence = "Ada Lovelace completed the accredited computer science qualification."
    evidence_digest = hashlib.sha256(evidence.encode()).hexdigest()

    direct_vm.mock_web(
        r"^https://evidence\.test$",
        {"method": "GET", "status": 200, "body": evidence},
    )
    direct_vm.mock_llm(
        r"Return strict JSON with decision",
        json.dumps(json.dumps({"decision": "APPROVED", "confidence_band": "HIGH", "policy_fit": "match",
                               "critical_risks": [], "evidence_ids": ["evidence-1"],
                               "rationale": "The source supports the qualification."})),
    )
    direct_vm.mock_llm(r"Independently verify this proposed", json.dumps("true"))
    direct_vm.mock_llm(
        r"Return strict JSON only",
        json.dumps(json.dumps({"uphold": False, "reason": "challenge evidence is insufficient"})),
    )
    direct_vm.mock_llm(
        r"Return JSON object only",
        json.dumps(json.dumps({"uphold": False})),
    )

    mesh.enroll_target("target", "Target")
    mesh.register_issuer("issuer", owner)
    mesh.register_source_authority("source", owner)
    mesh.attest_source("source", "https://evidence.test", evidence_digest)
    mesh.register_credential(
        "credential", "issuer", "Subject", "Qualification",
        "https://evidence.test", evidence_digest, "source", 4102444800,
    )
    mesh.publish_policy("target", "Qualification must match the requested role.")
    mesh.propose_review("proposal", "target", "credential", 2, "role=engineer")

    assert mesh.settle_review("proposal") == "APPROVED"
    settled = mesh.get_proposal("proposal")
    assert settled["status"] == "APPROVED"
    assert settled["challenge_deadline"] == settled["settled_at"] + 86400
    assert mesh.is_credential_authorized("proposal") is False

    with direct_vm.prank(challenger):
        assert mesh.challenge_review("proposal", "https://evidence.test", evidence_digest) is True
    assert mesh.get_proposal("proposal")["status"] == "CHALLENGED"
    assert mesh.resolve_challenge("proposal") == "APPROVED"

    with pytest.raises(AssertionError, match="challenge window open"):
        mesh.finalize_review("proposal")
    direct_vm.warp("2026-09-12T00:00:00Z")
    assert mesh.finalize_review("proposal") is True
    assert mesh.get_proposal("proposal")["status"] == "FINALIZED"
    assert mesh.is_credential_authorized("proposal") is True

    mesh.revoke_credential("credential")
    assert mesh.get_credential("credential")["revoked"] is True
    assert mesh.is_credential_authorized("proposal") is False
