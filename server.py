"""Loopback-only companion. Credentials are environment-only and never sent to the browser."""
import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from contractpilot.core import analyze, generate_plan

WEB = Path(__file__).resolve().parent / 'web/dist'
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(WEB),**kwargs)
    def answer(self,status,data):
        payload=json.dumps(data).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(payload)));self.end_headers();self.wfile.write(payload)
    def do_GET(self):
        if self.path=='/api/status':
            self.answer(200,{'live_ready':bool(os.getenv('NEBIUS_API_KEY') and os.getenv('NEBIUS_MODEL','').lower().startswith('nvidia/'))});return
        super().do_GET()
    def do_POST(self):
        if self.path!='/api/plan':self.answer(404,{'error':'Unknown route'});return
        host=self.headers.get('Host','')
        if host.split(':')[0] not in ('127.0.0.1','localhost'):self.answer(403,{'error':'Loopback host required'});return
        expected='http://'+host
        if self.headers.get('Origin')!=expected:self.answer(403,{'error':'Same-origin requests only'});return
        try:
            size=int(self.headers.get('Content-Length','0'))
            if size<=0 or size>1_000_000:raise ValueError('Request must be under 1 MB.')
            data=json.loads(self.rfile.read(size));result=generate_plan(analyze(data['before'],data['after']));self.answer(200,result)
        except (ValueError,KeyError,TypeError):self.answer(400,{'error':'Could not generate a validated plan. Check OpenAPI inputs, Nebius credentials, model access and credits. No fallback plan was used.'})

if __name__=='__main__':
    port=int(os.getenv('CONTRACTPILOT_PORT','8787'));print(f'ContractPilot: http://127.0.0.1:{port}',flush=True);ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()
