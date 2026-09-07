import { createClient, createAccount } from 'genlayer-js';
import { studionet } from 'genlayer-js/chains';
export const CONTRACT_ADDRESS = process.env.NEXT_PUBLIC_CREDENTIALMESH_ADDRESS || '';
export const chain = studionet;
export function getReadClient(){return createClient({chain, account:createAccount()});}
export function getWriteClient(address:string){return createClient({chain, account:address as `0x${string}`});}
export async function connectWallet(kind:'injected'|'browser'){if(kind==='browser') throw new Error('Browser-generated wallets are disabled. Use an injected wallet.');if(typeof window==='undefined'||!window.ethereum) throw new Error('No injected EIP-1193 wallet detected. Install MetaMask, Rabby, or another browser wallet.');const current=String(await window.ethereum.request({method:'eth_chainId'}));if(current!=='0xf22f'&&current!=='61999'){try{await window.ethereum.request({method:'wallet_switchEthereumChain',params:[{chainId:'0xf22f'}]});}catch(e){throw new Error('Switch your wallet to GenLayer StudioNet (chain 61999).');}}const accounts=await window.ethereum.request({method:'eth_requestAccounts'}) as string[];if(!accounts[0]) throw new Error('Wallet returned no account.');return accounts[0];}
export function isStudioNet(chainId:string){return chainId==='0xf22f'||chainId==='61999';}
declare global { interface Window { ethereum?: {request:(args:{method:string;params?:unknown[]})=>Promise<unknown>; on?:(event:string,cb:(value:any)=>void)=>void} } }
