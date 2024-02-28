import pytest

from md_converter import convert_to_md

class Testbogner_damen_neuheiten:

    def test_case_1(self, data_file_path):
        file_path = data_file_path / 'bogner_damen_neuheiten.html'
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        result = convert_to_md(html_content)
        assert len(result.split()) < 1000

