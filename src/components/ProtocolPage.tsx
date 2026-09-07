import {ReactNode} from 'react';
import Nav from './Nav';
export default function ProtocolPage({title,eyebrow,children}:{title:string;eyebrow:string;children:ReactNode}){return <main><Nav/><section className="briefing compact"><div><p className="eyebrow">{eyebrow}</p><h1>{title}</h1></div></section><section className="workspace">{children}</section></main>}
