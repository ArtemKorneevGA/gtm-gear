import unittest, sys
sys.path.append("..") 
from helpers.request_builder import get_mock_workspace

class TestEntity(unittest.TestCase):
    # Change GAS variable name and check that depended tag has new gaSettings value equal to new variable name
    def test_rename_references_ga3_gas_variable(self):
        source_workspace = get_mock_workspace('./data/ga3_migration_container.json')
        gas = [t for t in source_workspace.variables if t.type == "gas"][0]  
        tag_name =source_workspace.variables[0].get_depended()['tags']['dependent_variables'][0]
        tag = [t for t in source_workspace.tags if t.name == tag_name][0]  
        new_gas_name = "new_test_name"
        gas.rename_references(new_gas_name, gas.name, False)
        self.assertEqual(tag.get_template_param("gaSettings"), '{{'+new_gas_name+'}}')
  
if __name__ == '__main__':
    unittest.main()