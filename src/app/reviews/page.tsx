import ProtocolPage from '@/components/ProtocolPage';
import LivePanel from '@/components/LivePanel';
export default function Reviews(){return <ProtocolPage eyebrow="REVIEWS / CONSENSUS" title="Semantic authorization"><LivePanel readMethod="list_proposals" readArgs={[0,20]} writeMethod="propose_review" labels={['proposal_id','target_id','credential_id','policy_version','context']} /></ProtocolPage>}
