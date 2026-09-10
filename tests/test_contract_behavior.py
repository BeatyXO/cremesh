import pytest


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
