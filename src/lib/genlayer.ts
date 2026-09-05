import { createClient, createAccount, generatePrivateKey } from 'genlayer-js';
import { studionet } from 'genlayer-js/chains';
export const CONTRACT_ADDRESS = process.env.NEXT_PUBLIC_CREDENTIALMESH_ADDRESS || '';
export const chain = studionet;
export function getReadClient(){return createClient({chain, account:createAccount()});}
export function getWriteClient(address:string){return createClient({chain, account:address as `0x${string}`});}
export async function connectWallet(kind:'injected'|'browser'){if(kind==='injected'){if(typeof window==='undefined'||!window.ethereum) throw new Error('No injected EIP-1193 wallet detected. Use a browser wallet instead.');const accounts=await window.ethereum.request({method:'eth_requestAccounts'}) as string[];return accounts[0];} let key=localStorage.getItem('credentialmesh.browser-key'); if(key===null){key=generatePrivateKey();localStorage.setItem('credentialmesh.browser-key',key);localStorage.setItem('credentialmesh.browser-wallet-warning','acknowledged');} return createAccount(key as `0x${string}`).address;}
export function isStudioNet(chainId:string){return chainId==='0xf22f'||chainId==='61999';}
declare global { interface Window { ethereum?: {request:(args:{method:string;params?:unknown[]})=>Promise<unknown>; on?:(event:string,cb:(value:any)=>void)=>void} } }
