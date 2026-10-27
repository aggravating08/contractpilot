const methods=new Set(['get','post','put','patch','delete','head','options','trace']);
export async function analyze(before,after){
 const object=v=>v!==null&&typeof v==='object'&&!Array.isArray(v);
 for(const spec of [before,after]){
 if(!object(spec)||!String(spec.openapi).startsWith('3.')||!object(spec.paths))throw Error('Supply OpenAPI 3 JSON objects with a paths object.');
 for(const[path,item]of Object.entries(spec.paths)){
 if(!path.startsWith('/')||!object(item))throw Error('Each paths entry must be a slash-prefixed path and an object.');
 for(const operation of [item,...Object.entries(item).filter(([k])=>methods.has(k)).map(([,v])=>v)]){
 if(!object(operation))throw Error('Each operation must be an object.');
 const params=operation.parameters??[];
 if(!Array.isArray(params)||('parameters'in operation&&operation.parameters===null)||params.some(p=>!object(p)))throw Error('Parameters must be an array of objects.');
 for(const p of params){if(!('$ref'in p)&&(typeof p.name!=='string'||!['query','path','header','cookie'].includes(p.in)))throw Error('Inline parameters need a name and a valid location.');if('required'in p&&typeof p.required!=='boolean')throw Error('Parameter required flags must be booleans.');}
 if(('responses'in operation&&!object(operation.responses))||('requestBody'in operation&&!object(operation.requestBody)))throw Error('Responses and requestBody must be objects.');
 if(operation.requestBody&&'required'in operation.requestBody&&typeof operation.requestBody.required!=='boolean')throw Error('Request body required flags must be booleans.');
 }}}

 const changes=[];
 const add=async(kind,pointer,message)=>{const text=JSON.stringify({kind,message,pointer});const hash=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(text));changes.push({kind,pointer,message,id:Array.from(new Uint8Array(hash)).map(x=>x.toString(16).padStart(2,'0')).join('').slice(0,16)});};
 for(const[path,oldPath]of Object.entries(before.paths)){const newPath=after.paths[path]||{};for(const[method,old]of Object.entries(oldPath)){if(!methods.has(method))continue;const pointer='/paths/'+path.replaceAll('~','~0').replaceAll('/','~1')+'/'+method,newOp=newPath[method];if(!newOp){await add('operation_removed',pointer,`${method.toUpperCase()} ${path} was removed.`);continue;}
 const params=(p,o)=>new Map([...(p.parameters||[]),...(o.parameters||[])].filter(x=>!x.$ref).map(x=>[JSON.stringify([x.in,x.name]),x]));const prev=params(oldPath,old),next=params(newPath,newOp);for(const[key,p]of next)if(p.required&&!prev.get(key)?.required)await add('required_parameter',pointer,`${method.toUpperCase()} ${path} now requires ${p.in} parameter ${p.name}.`);
 for(const status of Object.keys(old.responses||{}))if(status.startsWith('2')&&!(status in(newOp.responses||{}))&&!('2XX'in(newOp.responses||{}))&&!('default'in(newOp.responses||{})))await add('success_response_removed',pointer+'/responses/'+status,`${method.toUpperCase()} ${path} no longer declares success response ${status}.`);
 if(newOp.requestBody?.required&&!old.requestBody?.required)await add('required_request_body',pointer+'/requestBody',`${method.toUpperCase()} ${path} now requires a request body.`);
 }}return{changes,breaking_count:changes.length,coverage:'Operation removal, newly required inline parameters/request bodies, removed success codes. References, schema compatibility, authentication and runtime behavior are not evaluated.',mode:'analysis-only'};
}
