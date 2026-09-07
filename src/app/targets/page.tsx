import ProtocolPage from '@/components/ProtocolPage';
import LivePanel from '@/components/LivePanel';
export default function Targets(){return <ProtocolPage eyebrow="TARGETS & POLICIES / LIVE" title="Scoped policy records"><LivePanel readMethod="get_target" readArgs={['']} writeMethod="enroll_target" labels={['target_id','label']} /></ProtocolPage>}
