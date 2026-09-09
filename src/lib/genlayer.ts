import { createClient, createAccount } from 'genlayer-js';
import { studionet } from 'genlayer-js/chains';
export const CONTRACT_ADDRESS = process.env.NEXT_PUBLIC_CREDENTIALMESH_ADDRESS || '';
export const chain = studionet;
export function getReadClient(){return createClient({chain,account:createAccount()});}
export function getWriteClient(address:string){return createClient({chain,account:address as `0x${string}`,provider:typeof window!=='undefined'?window.ethereum:undefined});}
export async function writeMesh(address:string,functionName:string,args:unknown[]){const client=getWriteClient(address);const tx=await client.writeContract({address:CONTRACT_ADDRESS as `0x${string}`,functionName,args:args as any,value:BigInt(0)});const receipt:any=await client.waitForTransactionReceipt({hash:tx.hash ?? tx});const leaders=receipt?.consensus_data?.leader_receipt??receipt?.leader_receipt??[];if(leaders.some((r:any)=>r?.execution_result==='ERROR'))throw new Error('GenVM execution failed; consensus acceptance does not mean the contract write succeeded.');return receipt;}
export async function connectWallet(){if(typeof window==='undefined'||!window.ethereum)throw new Error('No injected EIP-1193 wallet detected. Install MetaMask, Rabby, or another browser wallet.');const current=String(await window.ethereum.request({method:'eth_chainId'}));if(current!=='0xf22f'&&current!=='61999')await window.ethereum.request({method:'wallet_switchEthereumChain',params:[{chainId:'0xf22f'}]});const accounts=await window.ethereum.request({method:'eth_requestAccounts'}) as string[];if(!accounts[0])throw new Error('Wallet returned no account.');return accounts[0];}
export async function readPolicy(targetId:string,version:number){return getReadClient().readContract({address:CONTRACT_ADDRESS as `0x${string}`,functionName:'get_policy',args:[targetId,version] as any});}
export async function readAuthorization(proposalId:string){return getReadClient().readContract({address:CONTRACT_ADDRESS as `0x${string}`,functionName:'get_authorization',args:[proposalId] as any});}
export function isStudioNet(chainId:string){return chainId==='0xf22f'||chainId==='61999';}
declare global {interface Window{ethereum?:{request:(args:{method:string;params?:unknown[]})=>Promise<unknown>;on?:(event:string,cb:(value:any)=>void)=>void}}}
