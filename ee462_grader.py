"""Script to test EE462 lab submissions

Author: Zander Blasingame
"""

import argparse
import subprocess
import signal
import json

parser = argparse.ArgumentParser()

parser.add_argument('grade_file',
                    type=str,
                    help='Location of file containing grading info (json)')
parser.add_argument('students',
                    type=str,
                    help='Name of students seperated by newlines')
parser.add_argument('outdir',
                    type=str,
                    help='Location of output files')
parser.add_argument('lab_dir',
                    type=str,
                    default='.',
                    help='Location of lab directory')

args = parser.parse_args()


# code for handling timeout errors
class TimeoutError(Exception):
    pass


def handler(signum, frame):
    raise TimeoutError()

# dictionary to test data
testing_data = {}

with open(args.lab_dir + '/' + args.grade_file, 'r') as f:
    testing_data = json.load(f)

students = []

with open(args.lab_dir + '/' + args.students, 'r') as f:
    for line in f:
        students.append(line.rstrip())

for student in students:
    print('Processing ' + student)
    output = 'Testing {} {} submission\n'.format(student, args.lab_dir)

    for key in testing_data:
        script_name = '{2}/{0}/{1}{0}'.format(key, student, args.lab_dir)

        output += '='*79 + '\n'

        output += 'Testing file {}\n'.format(key)

        for i, test in enumerate(testing_data[key]['test']):
            command = 'bash {} {}'.format(script_name, test)
            output += 'Testing: `{}`\n'.format(command)

            script_out = ''

            # set timeout handler
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(1)

            try:
                script_out = subprocess.check_output(
                    command.rstrip().split(' '),
                    stderr=subprocess.STDOUT).decode('utf-8')
            except subprocess.CalledProcessError as e:
                err = ('An error was encountered running '
                       'the command: `{}`\n')
                output += err.format(command)
                output += e.output.decode('utf-8') + '\n'
            except TimeoutError as e:
                output += 'The command `{}` timed out\n'.format(command)
            finally:
                signal.alarm(0)

            if testing_data[key]['answer'] is not None:
                script_ans = script_out.split('\n')
                answers = testing_data[key]['answer'][i].split('\n')

                if len(script_ans) >= len(answers):
                    output += '{:^30}|{:^30}\n'.format(
                        'Your answer', 'Correct answer')

                    for j, ans in enumerate(answers):
                        output += '{:^30}|{:^30}\n'.format(
                            script_ans[j], answers[j])
                else:
                    output += 'Correct ouput:\n'
                    for ans in answers:
                        output += '\t' + ans + '\n'
            else:
                output += 'Your answer:\n' + script_out

            output += '-'*79 + '\n'

    with open('{}/{}/{}testlog'.format(args.lab_dir,
                                       args.outdir, student), 'w') as f:
        f.write(output)
