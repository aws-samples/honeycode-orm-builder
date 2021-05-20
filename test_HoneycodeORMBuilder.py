#  Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance
#  with the License. A copy of the License is located at
#
#  http://aws.amazon.com/apache2.0/
#
#  or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions
#  and limitations under the License.
from unittest import TestCase, mock
from unittest.mock import MagicMock
import os, os.path
from HoneycodeORMBuilder import HoneycodeORMBuilder

mock_list_tables_response = {
        'tables': [{'tableId': '00000000-0000-0000-0000-000000000001', 'tableName': 'test1'},
                   {'tableId': '00000000-0000-0000-0000-000000000002', 'tableName': 'test2'},],
}
mock_list_columns_response = {
    'tableColumns': [
        {'tableColumnId': '00000000-0000-0000-0000-000000000006', 'tableColumnName': 'Parameter',
         'format': 'AUTO'},
        {'tableColumnId': '00000000-0000-0000-0000-000000000007', 'tableColumnName': 'Weight',
         'format': 'AUTO'},
        {'tableColumnId': '00000000-0000-0000-0000-000000000008', 'tableColumnName': 'Color', 'format': 'AUTO'},
        {'tableColumnId': '00000000-0000-0000-0000-000000000009', 'tableColumnName': 'Description',
         'format': 'AUTO'}]}
class TestHoneycodeORMBuilder(TestCase):

    @mock.patch("botocore.client")
    def test_build_orm(self, mock_boto_client):
        hcclient = MagicMock()
        hcclient.list_tables.return_value = mock_list_tables_response
        hcclient.list_table_columns.return_value = mock_list_columns_response
        create_client = MagicMock()
        create_client.create_client.return_value = hcclient
        mock_boto_client.ClientCreator.return_value = create_client

        hcb = HoneycodeORMBuilder("dummy-workbook-id")
        hcb.buildORM()
        numberOfFilesCreated = len(os.listdir(os.getcwd() + '/orm'))
        print(str(numberOfFilesCreated))
        self.assertEqual(2,numberOfFilesCreated)


    # def test_build_insert_for_table(self):
    #     self.fail()
    #
    # def test_build_print_statement(self):
    #     self.fail()
    #
    # def test_build_var_alloc_for_table(self):
    #     self.fail()
    #
    # def test_build_convert(self):
    #     self.fail()
    #
    # def test_build_params_for_table(self):
    #     self.fail()
    #
    # def test_get_table_id_by_name(self):
    #     self.fail()
