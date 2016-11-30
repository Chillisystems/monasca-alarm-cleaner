import unittest
from mock import MagicMock

'''
For testing we want to test following scenarios:

Alarm list scenarios:
    - All alarms are in OK state
    - We have some alarm in UNDETERMINED state
    - We do not have any alarms

VM list ids:
    - Empty list
    - List not matching any ids from alarm list
    - List matching All alarms regarding state
    - List matching OK state alarms
    - List matching UNDETERMINED state alarms only

'''


class TestMonascaCleanerMethods(unittest.TestCase):

    def test_list_vm_undetermined_alarms(self):
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()
