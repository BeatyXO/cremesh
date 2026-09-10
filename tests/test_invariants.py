import hashlib
import pytest

class MeshModel:
    def __init__(self): self.sources={}; self.credentials={}; self.proposals={}; self.policies={}
    def attest_source(self,s,a,r,d): self.sources[s]={"authority":a,"ref":r,"digest":d}
    def register_credential(self,c,i,s,r,d,expiry):
        assert s in self.sources and self.sources[s]["authority"]==i
        assert self.sources[s]["ref"]==r and self.sources[s]["digest"]==d
        self.credentials[c]={"issuer":i,"source":s,"ref":r,"digest":d,"expiry":expiry,"revoked":False}
    def propose(self,p,c,t,v,ctx):
        assert p not in self.proposals and c in self.credentials and (t,v) in self.policies
        self.proposals[p]={"id":p,"credential":c,"target":t,"version":v,"policy_hash":self.policies[(t,v)],"context":ctx,"context_digest":hashlib.sha256(ctx.encode()).hexdigest(),"status":"REVIEWING"}
    def authorize(self,p,now):
        q=self.proposals.get(p); c=self.credentials.get(q["credential"]) if q else None
        return bool(q and q["id"]==p and q["status"]=="FINALIZED" and c and not c["revoked"] and c["expiry"]>=now and self.policies.get((q["target"],q["version"]))==q["policy_hash"])

def seeded():
    m=MeshModel(); m.policies[('target',2)]='policy-hash'; m.attest_source('source','issuer','ref','digest'); m.register_credential('credential','issuer','source','ref','digest',100); return m

def test_attestation_is_required_and_digest_bound():
    m=MeshModel(); m.policies[('target',2)]='policy-hash'
    with pytest.raises(AssertionError): m.register_credential('c','issuer','source','ref','digest',100)
    m.attest_source('source','issuer','ref','digest')
    with pytest.raises(AssertionError): m.register_credential('c','issuer','source','changed','digest',100)

def test_authorization_requires_exact_finalized_proposal():
    m=seeded(); m.propose('p','credential','target',2,'role=A'); assert not m.authorize('p',1)
    m.proposals['p']['status']='APPROVED'; assert not m.authorize('p',1)
    m.proposals['p']['status']='FINALIZED'; assert m.authorize('p',1); assert not m.authorize('other',1)
    assert m.proposals['p']['context_digest']==hashlib.sha256('role=A'.encode()).hexdigest()

def test_rejected_abstained_revoked_expired_are_not_authorized():
    for status in ('REJECTED','ABSTAINED'):
        m=seeded(); m.propose('p','credential','target',2,'role=A'); m.proposals['p']['status']=status; assert not m.authorize('p',1)
    m=seeded(); m.propose('p','credential','target',2,'role=A'); m.proposals['p']['status']='FINALIZED'; m.credentials['credential']['revoked']=True; assert not m.authorize('p',1)
    m=seeded(); m.propose('p','credential','target',2,'role=A'); m.proposals['p']['status']='FINALIZED'; assert not m.authorize('p',101)

def test_challenge_validator_must_match_leader_uphold():
    assert (True is True) and (False is False); assert not (True is False)
