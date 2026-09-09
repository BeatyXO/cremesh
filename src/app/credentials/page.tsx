import ProtocolPage from '@/components/ProtocolPage';
import LivePanel from '@/components/LivePanel';
import ActionPanel from '@/components/ActionPanel';
export default function Credentials(){return <ProtocolPage eyebrow="CREDENTIALS / LIVE" title="Credential registry"><ActionPanel method="register_issuer" labels={['issuer_id','issuer_address']} /><ActionPanel method="register_source_authority" labels={['source_id','authority']} /><ActionPanel method="attest_source" labels={['source_id','evidence_ref','source_digest']} /><LivePanel readMethod="list_credentials" writeMethod="register_credential" labels={['credential_id','issuer_id','subject','qualification','evidence_ref','source_digest','source_id','expiry']} /></ProtocolPage>}
