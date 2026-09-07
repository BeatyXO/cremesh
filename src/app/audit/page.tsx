import ProtocolPage from '@/components/ProtocolPage';
export default function Audit(){return <ProtocolPage eyebrow="AUDIT / PUBLIC READS" title="Audit trail"><div className="empty"><h3>Public contract audit</h3><p>Audit records are read-only and sourced from list_audit() on the deployed StudioNet contract.</p></div></ProtocolPage>}
