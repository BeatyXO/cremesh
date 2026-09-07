import ProtocolPage from '@/components/ProtocolPage';
import LivePanel from '@/components/LivePanel';
export default function Audit(){return <ProtocolPage eyebrow="AUDIT / PUBLIC READS" title="Audit trail"><LivePanel readMethod="list_audit" readArgs={[0,50]} writeMethod="enroll_target" labels={[]} /></ProtocolPage>}
