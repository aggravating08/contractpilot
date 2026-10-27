import http.client
import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from server import Handler

class CompanionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
    @classmethod
    def tearDownClass(cls): cls.server.shutdown();cls.server.server_close();cls.thread.join()
    def request(self,method,path,body=None,headers=None):
        conn=http.client.HTTPConnection(*self.server.server_address);conn.request(method,path,body,headers or {});resp=conn.getresponse();result=(resp.status,resp.read());conn.close();return result
    def test_status_has_no_credential(self):
        status,body=self.request('GET','/api/status');self.assertEqual(status,200);self.assertEqual(set(json.loads(body)),{'live_ready'})
    def test_cross_origin_plan_rejected(self):
        status,_=self.request('POST','/api/plan','{}',{'Origin':'https://example.com'});self.assertEqual(status,403)
    def test_rebinding_host_rejected(self):
        status,_=self.request('POST','/api/plan','{}',{'Host':'evil.example','Origin':'http://evil.example'});self.assertEqual(status,403)
    def test_secret_file_unavailable(self):
        status,_=self.request('GET','/.env.example');self.assertEqual(status,404)
