'use client';
import Link from 'next/link';
export default function Nav(){return <nav className="topbar"><Link className="brand" href="/"><span className="seal">CM</span><span>Credential<span className="gold">Mesh</span></span></Link><div className="network"><span className="dot"/> STUDIONET <small>61999</small></div><div className="navlinks"><Link href="/credentials">Credentials</Link><Link href="/targets">Targets & Policies</Link><Link href="/reviews">Reviews</Link><Link href="/audit">Audit</Link></div></nav>}
