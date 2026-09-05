import { createClient, createAccount } from 'genlayer-js';
import { studionet } from 'genlayer-js/chains';
const address = process.env.NEXT_PUBLIC_CREDENTIALMESH_ADDRESS;
if (!address) { console.error('Set NEXT_PUBLIC_CREDENTIALMESH_ADDRESS before schema verification.'); process.exit(1); }
const client = createClient({ chain: studionet, account: createAccount() });
const schema = await client.getContractSchema(address);
const names = (schema?.functions ?? schema ?? []).map((x) => typeof x === 'string' ? x : x.name);
const required = ['enroll_target','publish_policy','register_credential','revoke_credential','propose_review','settle_review','challenge_review','get_target','get_credential','get_proposal','list_proposals','list_credentials','list_audit'];
const missing = required.filter((name) => !names.includes(name));
if (missing.length) { console.error('Schema mismatch. Missing:', missing.join(', ')); process.exit(1); }
console.log('CredentialMesh schema verified:', required.length, 'methods');
