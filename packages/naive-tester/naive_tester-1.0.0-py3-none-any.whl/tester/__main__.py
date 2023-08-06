"""Naive Tester

Usage:
-----

    $ tester [script] [test_case_folder]

script - a script to test
test_case_folder - a folder containing pairs of .in and .out files,
where
    .in holds [script] argument
    .out holds expected output

Contact:
-------

More information is available at:
- https://github.com/FilippSolovev/naive-tester

Version:
-------

- naive-tester v1.0.0
"""
import sys
import logging

from tester.io import check_files_existence, get_files, do_files_comply
from tester.runner import run_jobs

logger = logging.getLogger(__name__)


def main():
    if len(sys.argv) > 1:
        script_name = sys.argv[1]
        dir_name = sys.argv[2]
    else:
        sys.exit()

    check_files_existence(script_name, 'Script given does not exist')
    check_files_existence(script_name, 'Directory given does not exist')

    jobs_arguments = get_files(dir_name, '.in')
    output_files = get_files(dir_name, '.out')
    if not do_files_comply(jobs_arguments, output_files):
        logger.error('Input and output files do not comply')
        sys.exit()

    reference_outputs = []
    for file_name in output_files:
        with open(file_name, 'r') as output_file:
            output = output_file.read().strip()
            reference_outputs.append(output)

    jobs = zip([script_name for _ in jobs_arguments],
               jobs_arguments)

    jobs_with_outputs = zip(jobs, reference_outputs)

    run_jobs(jobs_with_outputs)


if __name__ == '__main__':
    main()
