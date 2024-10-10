import unittest
from utils.gitUtils import extract_owner_and_repo, get_repo_structure, get_file_content

#input
repo_url = "https://github.com/domenicodegioia/cobolProject2"
owner = 'domenicodegioia'
repo = 'cobolProject2'
file_url = "https://api.github.com/repos/domenicodegioia/cobolProject2/contents/mainprogram.cbl"

#output
output_owner_repo = ('domenicodegioia', 'cobolProject2')
output_structure = [{'folder': '/', 'files': ['.gitattributes', 'README.md', 'contributionmodule.cbl', 'mainprogram.cbl', 'pensionmodule.cbl', 'taxmodule.cbl', 'user-structure.cbl', 'userdata.dat']}]
output_file = '''IDENTIFICATION DIVISION.
PROGRAM-ID. MAINPROGRAM.
ENVIRONMENT DIVISION.
DATA DIVISION.
WORKING-STORAGE SECTION.
COPY "USER-STRUCTURE.CPY".
PROCEDURE DIVISION.
    PERFORM INITIALIZE-SYSTEM
    PERFORM MENU-SELECTION
    STOP RUN.

INITIALIZE-SYSTEM.
    DISPLAY "Welcome to the Public Administration System".

MENU-SELECTION.
    DISPLAY "Choose an option:"
    DISPLAY "1. Manage Taxes"
    DISPLAY "2. Manage Contributions"
    DISPLAY "3. Manage Pensions"
    ACCEPT USER-INPUT
    EVALUATE USER-INPUT
        WHEN "1" PERFORM TAX-OPERATIONS
        WHEN "2" PERFORM CONTRIBUTION-OPERATIONS
        WHEN "3" PERFORM PENSION-OPERATIONS
        WHEN OTHER DISPLAY "Invalid option".
    END-EVALUATE.

TAX-OPERATIONS.
    CALL "TAXMODULE" USING USER-STRUCTURE.

CONTRIBUTION-OPERATIONS.
    CALL "CONTRIBUTIONMODULE" USING USER-STRUCTURE.

PENSION-OPERATIONS.
    CALL "PENSIONMODULE" USING USER-STRUCTURE.'''

class TestUtilsFunctions(unittest.TestCase):

    def test_git_utils(self):
        self.assertEqual(extract_owner_and_repo(repo_url), output_owner_repo)
        self.assertEqual(get_repo_structure(owner, repo), output_structure)
        self.assertEqual(get_file_content(file_url), output_file)

if __name__ == '__main__':
    unittest.main()