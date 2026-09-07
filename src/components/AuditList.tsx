'use client';
import {useEffect,useState} from 'react';
import {CONTRACT_ADDRESS,getReadClient} from '@/lib/genlayer';
export default function AuditList(){const[rows,setRows]=useState<any[]>([]);const[error,setError]=useState('');useEffect(()=>{getReadClient().readContract({address:CONTRACT_ADDRESS as `0x${string}`,functionName:'list_audit',args:[0,50]}).then(v=>setRows(Array.isArray(v)?v:[])).catch(e=>setError(String(e)))},[]);return <div className="queue">{error&&<p>{error}</p>}{rows.map((r,i)=><article className="proposal" key={i}><span className="index">{r.kind}</span><span className="proposal-main"><strong>{r.ref}</strong><small>{r.detail}</small></span><span>{new Date(Number(r.at)*1000).toLocaleString()}</span></article>)}</div>}
