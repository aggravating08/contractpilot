import copy
import json
import unittest
from pathlib import Path
from contractpilot.core import analyze, validate_plan, generate_plan
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]

class CompatibilityTests(unittest.TestCase):
    def setUp(self):
        self.before = json.loads((ROOT / 'examples/before.json').read_text())
        self.after = json.loads((ROOT / 'examples/after.json').read_text())

    def test_three_distinct_breaks_and_stable_ids(self):
        report = analyze(self.before, self.after)
        self.assertEqual(report['breaking_count'], 3)
        self.assertEqual({x['kind'] for x in report['changes']}, {'operation_removed','required_parameter','success_response_removed'})
        self.assertEqual(report, analyze(self.before, self.after))
        self.assertEqual(len({x['id'] for x in report['changes']}), 3)

    def test_nonbreaking_addition(self):
        new = copy.deepcopy(self.before)
        new['paths']['/health'] = {'get': {'responses': {'200': {'description': 'OK'}}}}
        self.assertEqual(analyze(self.before, new)['breaking_count'], 0)

    def test_optional_parameter_does_not_break(self):
        new = copy.deepcopy(self.before)
        new['paths']['/parcels']['get']['parameters'] = [{'in':'query','name':'limit','required':False}]
        self.assertEqual(analyze(self.before, new)['breaking_count'], 0)

    def test_path_parameter_override_uses_operation_value(self):
        old = copy.deepcopy(self.before)
        new = copy.deepcopy(old)
        new['paths']['/parcels']['parameters'] = [{'in':'query','name':'region','required':True}]
        new['paths']['/parcels']['get']['parameters'] = [{'in':'query','name':'region','required':False}]
        self.assertEqual(analyze(old, new)['breaking_count'], 0)

    def test_required_body(self):
        new = copy.deepcopy(self.before)
        new['paths']['/parcels']['get']['requestBody'] = {'required': True}
        self.assertEqual(analyze(self.before, new)['changes'][0]['kind'], 'required_request_body')

    def test_reject_wrong_spec(self):
        with self.assertRaises(ValueError): analyze({'swagger':'2.0','paths':{}}, self.after)

    def test_invalid_plan_reference(self):
        report=analyze(self.before,self.after)
        with self.assertRaises(ValueError): validate_plan({'steps':[{'action':'Migrate','change_ids':['invented']}]},report['changes'])

    def test_missing_plan_reference(self):
        with self.assertRaises(ValueError): validate_plan({'steps':[{'action':'Migrate','change_ids':[]}]},[])

    def test_valid_plan_reference(self):
        changes=analyze(self.before,self.after)['changes']
        plan={'steps':[{'action':'Pass region in list requests.','change_ids':[changes[0]['id']]}]}
        self.assertEqual(validate_plan(plan,changes),plan)

    def test_missing_key_fails_without_fallback(self):
        with patch.dict('os.environ',{},clear=True), self.assertRaises(ValueError):
            generate_plan(analyze(self.before,self.after))

    def test_no_changes_makes_no_provider_call(self):
        with patch('urllib.request.urlopen') as request:
            self.assertEqual(generate_plan(analyze(self.before,self.before))['provider'],'none')
            request.assert_not_called()

if __name__ == '__main__': unittest.main()
