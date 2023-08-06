"""
Execution of an IPython notebook
"""

import os
import re
import ast
import copy

from unittest import mock
from contextlib import redirect_stdout, redirect_stderr
from IPython.display import display
from IPython.core.inputsplitter import IPythonInputSplitter

from .check_wrapper import CheckCallWrapper

from ..utils import hide_outputs

IGNORE_CELL_TAG = "taeg_ignore"
CELL_METADATA_KEY = "taeg"

def filter_ignored_cells(nb):
    """
    Filters out all cells in the notebook ``nb`` that are tagged with ``taeg_ignore``. Returns a copy
    of the original notebook.

    Args:
        nb (``dict``): JSON representation of a notebook

    Returns:
        ``dict``: the notebook with cells removed
    """
    nb = copy.deepcopy(nb)

    for i, cell in enumerate(nb['cells']):
        metadata = cell.get("metadata", {})
        tags = metadata.get("tags", [])

        if IGNORE_CELL_TAG in tags or metadata.get(CELL_METADATA_KEY, {}).get("ignore", False):
            del nb['cells'][i]
    
    return nb

def execute_notebook(nb, secret='secret', initial_env=None, ignore_errors=False, cwd=None, test_dir=None, seed=None):
    """
    Executes a notebook and returns the global environment that results from execution

    Execute notebook & return the global environment that results from execution. If ``ignore_errors`` 
    is ``True``, exceptions are swallowed. ``secret`` contains random digits so ``check_results`` and 
    ``check`` are not easily modifiable. ``nb`` is passed in as a dictionary that's a parsed notebook

    Args:
        nb (``dict``): JSON representation of a notebook
        secret (``str``, optional): randomly generated integer used to rebind check function
        initial_env (``str``, optional): name of initial environment
        ignore_errors (``bool``, optional): whether exceptions should be ignored
        cwd (``str``, optional): working directory of execution to be appended to ``sys.path`` in 
            grading environment
        test_dir (``str``, optional): path to directory of tests in grading environment
        seed (``int``, optional): random seed for intercell seeding
    
    Results:
        ``dict``: global environment resulting from executing all code of the input notebook
    """
    with hide_outputs():
        if initial_env:
            global_env = initial_env.copy()
        else:
            global_env = {}

        # add display from IPython
        global_env["display"] = display

        # add dummy Notebook class so that we can collect results w/out altering how the CheckCallWrapper
        # needs to function
        from ..check.notebook import Notebook
        notebook_class_name = f"Notebook_{secret}"
        global_env[notebook_class_name] = Notebook

        source = ""

        if cwd:
            source = f"import sys\nsys.path.append(r\"{cwd}\")\n"
            exec(source, global_env)
        if seed is not None:
            # source += "import numpy as np\nimport random\n"
            import numpy as np
            import random
            global_env["np"] = np
            global_env["random"] = random

        if test_dir is None:
            test_dir = "/home/tests"

        # Before rewriting AST, find cells of code that generate errors.
        # One round of execution is done beforehand to mimic the Jupyter notebook style of running
        # (e.g. code runs up to the point of execution).
        # The reason this is workaround is introduced is because once the
        # source code is parsed into an AST, there is no sense of local cells

        for cell in nb['cells']:
            if cell['cell_type'] == 'code':
                # transform the input to executable Python
                # FIXME: use appropriate IPython functions here
                isp = IPythonInputSplitter(line_input_checker=False)
                try:
                    code_lines = []
                    cell_source_lines = cell['source']
                    source_is_str_bool = False
                    if isinstance(cell_source_lines, str):
                        source_is_str_bool = True
                        cell_source_lines = cell_source_lines.split('\n')

                    for line in cell_source_lines:
                        # Filter out ipython magic commands
                        # Filter out interact widget
                        if not line.startswith('%'):
                            if "interact(" not in line and not re.search(r"taeg\.Notebook\(.*?\)", line):
                                code_lines.append(line)
                                if source_is_str_bool:
                                    code_lines.append('\n')
                            elif re.search(r"taeg\.Notebook\(.*?\)", line):
                                # TODO: move this check into CheckCallWrapper
                                # if gradescope:
                                #     line = re.sub(r"taeg\.Notebook\(.*?\)", "taeg.Notebook(\"/autograder/submission/tests\")", line)
                                # el
                                line = re.sub(r"taeg\.Notebook\(.*?\)", f"taeg.Notebook(\"{test_dir}\")", line)
                                code_lines.append(line)
                                if source_is_str_bool:
                                    code_lines.append('\n')
                    if seed is not None:
                        cell_source = "np.random.seed({})\nrandom.seed({})\n".format(seed, seed) + isp.transform_cell(''.join(code_lines))
                    else:
                        cell_source = isp.transform_cell(''.join(code_lines))

                    # patch taeg.Notebook.export so that we don't create PDFs in notebooks
                    # TODO: move this patch into CheckCallWrapper
                    m = mock.mock_open()
                    with mock.patch('taeg.Notebook.export', m), mock.patch("taeg.Notebook._log_event", m):
                        exec(cell_source, global_env)
                    source += cell_source

                except:
                    if not ignore_errors:
                        raise

            # add checks from metadata
            taeg_config = cell.get("metadata", {}).get(CELL_METADATA_KEY, {})
            check_results_list_name = f"check_results_{secret}"
            if taeg_config.get("tests", []):
                tests = taeg_config.get("tests", [])
                for test in tests:
                    source += f"\n{check_results_list_name}.append({notebook_class_name}('{test_dir}').check('{test}'))\n"


        tree = ast.parse(source)
        # # CODE BELOW COMMENTED OUT BECAUSE the only check function is within the Notebook class
        # if find_check_assignment(tree) or find_check_definition(tree):
        #     # an empty global_env will fail all the tests
        #     return global_env

        # wrap check(..) calls into a check_results_X.append(check(..))
        transformer = CheckCallWrapper(secret)
        tree = transformer.visit(tree)
        ast.fix_missing_locations(tree)

        try:
            cleaned_source = compile(tree, filename="nb-ast", mode="exec")
            with open(os.devnull, 'w') as f, redirect_stdout(f), redirect_stderr(f):
                # patch taeg.Notebook.export so that we don't create PDFs in notebooks
                m = mock.mock_open()
                with mock.patch('taeg.Notebook.export', m), mock.patch("taeg.Notebook._log_event", m):
                    exec(cleaned_source, global_env)
        except:
            if not ignore_errors:
                raise

        return global_env
