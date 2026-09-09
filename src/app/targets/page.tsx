import ProtocolPage from '@/components/ProtocolPage';
import LivePanel from '@/components/LivePanel';
import ActionPanel from '@/components/ActionPanel';
import ReadPanel from '@/components/ReadPanel';
export default function Targets(){return <ProtocolPage eyebrow="TARGETS & POLICIES / LIVE" title="Scoped policy records"><LivePanel readMethod="get_target" readArgs={['']} writeMethod="enroll_target" labels={['target_id','label']} /><ActionPanel method="publish_policy" labels={['target_id','policy']} /><ReadPanel method="get_policy" labels={['target_id','version']} /></ProtocolPage>}
