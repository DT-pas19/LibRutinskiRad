import unittest
from document_processor import (get_associated_works, get_associated_work_filenames)


class DocumentProcessorTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_associated_works_1(self):
        input_data_files = ['162289_б-НФГД11_2017_8.docx', '162290_б-НФГД11_2017_7_1.docx',
                            '162291_б-НФГД11_2017_7_1.docx', '162292_б-НФГД11_2019_7.docx']
        input_data_contents = ['162289_б-НФГД11_2017_8.docx', '162289_б-НФГД11_2017_8.xlsx',
                               '162290_б-НФГД11_2017_7_1.docx', '162290_б-НФГД11_2017_7_2.xlsx',
                               '162291_б-НФГД11_2017_7_2.xlsx', '162291_б-НФГД11_2017_7_1.docx',
                               '162291_б-НФГД11_2017_7_3.accdb', '162292_б-НФГД11_2019_7.docx']

        expected_output = [
            ['162289_б-НФГД11_2017_8.docx', '162289_б-НФГД11_2017_8.xlsx'],
            ['162290_б-НФГД11_2017_7_1.docx', '162290_б-НФГД11_2017_7_2.xlsx'],
            ['162291_б-НФГД11_2017_7_1.docx', '162291_б-НФГД11_2017_7_3.accdb', '162291_б-НФГД11_2017_7_2.xlsx'],
            ['162292_б-НФГД11_2019_7.docx']
        ]

        output = get_associated_works(input_data_files, input_data_contents)

        self.assertEqual(expected_output, output, 'Groupping for multiple documents doesn''t work as expected')

    def test_get_associated_works_2(self):
        input_data_files = ['182036_б1-ТТПРз-11_2019_7_1.docx', '182034_б1-ТТПРз-11_2019_7_1.docx',
                            '182038_б1ТТПРз11_2019_7_1.docx', '181894_б1-ТТПРз11_2019_7_1.docx',
                            '182029_б1-ТТПРз11_2019_7_1.docx', '181899_б1-ТТПРз-11_2019_7_1.docx',
                            '182032_б1-ТТПРз-11_2019_7_1.docx', '181896_б1ТТПРз11_2019_7_1.docx',
                            '181895_б1ТТПРз11_2019_7_1.docx', '181902_б-ТТПРз11_2019_7_1.docx',
                            '182035_б1-ТТПРз11_2019_7_1.docx']
        input_data_contents = ['182036_б1-ТТПРз-11_2019_7_1.docx', '182029_б1-ТТПРз11_2019_7_2.xlsx',
                               '182034_б1-ТТПРз-11_2019_7_2.xlsx', '182034_б1-ТТПРз-11_2019_7_1.docx',
                               '182038_б1ТТПРз11_2019_7_1.docx', '181895_б1ТТПРз11_2019_7_2.xlsx',
                               '181894_б1-ТТПРз11_2019_7_1.docx', '182038_б1ТТПРз11_2019_7_2.xlsx',
                               '182036_б1-ТТПРз-11_2019_7_2.xlsx', '181894_б1-ТТПРз11_2019_7_2.xlsx',
                               '182035_б1-ТТПРз11_2019_7_2.xlsx', '182029_б1-ТТПРз11_2019_7_1.docx',
                               '181902_б-ТТПРз11_2019_7_2.xlsx', '181899_б1-ТТПРз-11_2019_7_1.docx',
                               '182032_б1-ТТПРз-11_2019_7_1.docx', '181896_б1ТТПРз11_2019_7_1.docx',
                               '181895_б1ТТПРз11_2019_7_1.docx', '181902_б-ТТПРз11_2019_7_1.docx',
                               '182032_б1-ТТПРз-11_2019_7_2.xlsx', '182035_б1-ТТПРз11_2019_7_1.docx',
                               '181899_б1-ТТПРз-11_2019_7_1.xls']

        expected_output = [
            ['182036_б1-ТТПРз-11_2019_7_1.docx', '182036_б1-ТТПРз-11_2019_7_2.xlsx'],
            ['182034_б1-ТТПРз-11_2019_7_1.docx', '182034_б1-ТТПРз-11_2019_7_2.xlsx'],
            ['182038_б1ТТПРз11_2019_7_1.docx', '182038_б1ТТПРз11_2019_7_2.xlsx'],
            ['181894_б1-ТТПРз11_2019_7_1.docx', '181894_б1-ТТПРз11_2019_7_2.xlsx'],
            ['182029_б1-ТТПРз11_2019_7_1.docx', '182029_б1-ТТПРз11_2019_7_2.xlsx'],
            ['181899_б1-ТТПРз-11_2019_7_1.docx', '181899_б1-ТТПРз-11_2019_7_1.xls'],
            ['182032_б1-ТТПРз-11_2019_7_1.docx', '182032_б1-ТТПРз-11_2019_7_2.xlsx'],
            ['181896_б1ТТПРз11_2019_7_1.docx'],
            ['181895_б1ТТПРз11_2019_7_1.docx', '181895_б1ТТПРз11_2019_7_2.xlsx'],
            ['181902_б-ТТПРз11_2019_7_1.docx', '181902_б-ТТПРз11_2019_7_2.xlsx'],
            ['182035_б1-ТТПРз11_2019_7_1.docx', '182035_б1-ТТПРз11_2019_7_2.xlsx']
        ]

        output = get_associated_works(input_data_files, input_data_contents)

        self.assertEqual(expected_output, output, 'Groupping for multiple documents doesn''t work as expected')

    def test_get_associated_work_filenames(self):
        input_data_file = '162289_б-НФГД11_2017_8.docx'
        input_data_contents = ['162289_б-НФГД11_2017_8.docx', '162289_б-НФГД11_2017_8.xlsx',
                               '162289_б-НФГД11_2017_8_1.docx', '162289_б-НФГД11_2017_8_2.xlsx']

        expected_output = [
            '162289_б-НФГД11_2017_8.docx', '162289_б-НФГД11_2017_8.xlsx'
        ]

        output = get_associated_work_filenames(input_data_file, input_data_contents)

        self.assertEqual(expected_output, output, 'Groupping for a single document doesn''t work as expected')


if __name__ == '__main__':
    unittest.main()
