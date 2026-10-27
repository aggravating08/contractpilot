import assert from 'node:assert/strict';import{readFileSync}from'node:fs';import{spawnSync}from'node:child_process';import{analyze}from'../web/dist/engine.mjs';
const before=JSON.parse(readFileSync('examples/before.json')),after=JSON.parse(readFileSync('examples/after.json'));
const result=await analyze(before,after);assert.equal(result.breaking_count,3);
const py=spawnSync('python3',['-m','contractpilot','examples/before.json','examples/after.json'],{encoding:'utf8'});assert.equal(py.status,0);assert.deepEqual(result,JSON.parse(py.stdout));
assert.equal((await analyze(before,before)).breaking_count,0);
await assert.rejects(()=>analyze({swagger:'2.0',paths:{}},after));
const unicode=structuredClone(before);unicode.paths['/مرحبا:one,two']={get:{responses:{200:{description:'ok'}}}};const js=await analyze(unicode,before);
const parity=spawnSync('python3',['-c','import json,sys;from contractpilot.core import analyze;data=json.load(sys.stdin);print(json.dumps(analyze(*data)))'],{encoding:'utf8',input:JSON.stringify([unicode,before])});assert.equal(parity.status,0);assert.deepEqual(js,{...JSON.parse(parity.stdout),mode:'analysis-only'});
console.log('5 browser-engine checks passed, including Python parity and Unicode.');
