from django.test import TestCase
from policyengine.filter import *

def is_valid(code):
    errors = filter_code(code)
    return len(errors) == 0

dangerous_modules = [
    "os",
    "sys",
]

dangerous_functions = [
    "compile",
    "dir",
    "exec",
    "execfile",
    "eval",
    "file",
    "globals",
    "input",
    "locals",
    "open",
    "raw_input",
    "vars",
]

code = [
# Code 1
"""
action.execute()
""",

# Code 2
"""
if action.initiator.groups.filter(name = "Moderator").exists():
    return PASSED
else:
    return FAILED
""",

# Code 3
"""
import math

voter_users = users.filter(groups__name__in=['Moderator'])
yes_votes = action.proposal.get_yes_votes(users=voter_users, value=True)
if len(yes_votes) >= math.ceil(voter_users.count()/2):
    return PASSED
elif action.proposal.get_time_elapsed() > datetime.timedelta(days=1):
    return FAILED
""",

# Code 4
"""
usernames = [u.username for u in users]
jury = random.sample(usernames, k=3)
action.data.add('jury', jury)
""",

# Code 5
"""
jury = action.data.get('jury')
jury_users = users.filter(username__in=jury)
yes_votes = action.proposal.get_yes_votes(users=jury_users, value=True)
if len(yes_votes) >= 2:
    return PASSED
elif action.proposal.get_time_elapsed() > datetime.timedelta(days=2):
    return FAILED
""",
]

# Create your tests here.
class FilterTests(TestCase):
    def test_import_whitelisted_modules(self):
        for module in whitelisted_modules:
            code = "import " + module
            self.assertTrue(is_valid(code))

    def test_dangerous_modules(self):
        for module in dangerous_modules:
            code = "import " + module
            self.assertFalse(is_valid(code))

    def test_dangerous_functions(self):
        for function in dangerous_functions:
            code = function + "()"
            self.assertFalse(is_valid(code))

    def test_policy_code_1(self):
        self.assertTrue(is_valid(code[0]))

    def test_policy_code_2(self):
        self.assertTrue(is_valid(code[1]))

    def test_policy_code_3(self):
        self.assertTrue(is_valid(code[2]))

    def test_policy_code_4(self):
        self.assertTrue(is_valid(code[3]))

    def test_policy_code_5(self):
        self.assertTrue(is_valid(code[4]))