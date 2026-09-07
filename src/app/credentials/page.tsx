import ProtocolPage from '@/components/ProtocolPage';
import LivePanel from '@/components/LivePanel';
export default function Credentials(){return <ProtocolPage eyebrow="CREDENTIALS / LIVE" title="Credential registry"><LivePanel readMethod="list_credentials" writeMethod="register_credential" labels={['credential_id','subject','qualification','evidence_ref','source_digest','expiry']} /></ProtocolPage>}
