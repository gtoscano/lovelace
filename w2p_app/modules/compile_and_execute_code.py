from gluon import *
from gluon import current
import os
import zipfile
from subprocess import PIPE, Popen
import shutil
import datetime
import threading
import re
import tempfile

'''
# Execution of Submissions

For each language, if the above compilation step is successful then the submission will be executed as follows:

For C/C++:  the executable file generated by the compiler will be executed to generate the output of the submission.  
For Python 3: the main source file will be executed by the CPython Python3 interpreter to generate the output of the submission.
For Java: the compiled main class will be executed using the following command:
java -Dfile.encoding=UTF-8 -XX:+UseSerialGC -Xss64m -Xms1920m -Xmx1920m -cp ${directory} ${file}

For Kotlin: the compiled main class will be executed using the following command:
kotlin -Dfile.encoding=UTF-8 -J-XX:+UseSerialGC -J-Xss64m -J-Xms1920m -J-Xmx1920m



ret = _judger.run(max_cpu_time=1000,
				  max_real_time=2000,
				  max_memory=128 * 1024 * 1024,
				  max_process_number=200,
				  max_output_size=10000,
				  max_stack=32 * 1024 * 1024,
				  # five args above can be _judger.UNLIMITED
				  exe_path="main2",
				  input_path="1.in",
				  output_path="1.out",
				  error_path="1.err",
				  args=[],
				  # can be empty list
				  env=[],
				  log_path="judger.log",
				  # can be None
				  seccomp_rule_name="c_cpp",
				  uid=0,
				  gid=0)
'''
# check the following
# https://stackoverflow.com/questions/1770209/run-child-processes-as-different-user-from-a-long-running-python-process/6037494#6037494
# https://askubuntu.com/questions/294736/run-a-shell-script-as-another-user-that-has-no-password
class Command(object):
	def __init__(self, cmd,input_file=''):
		self.cmd = cmd
		self.process = None
		self.input_file = input_file
		self.output = None
		self.status = None
		self.error = None
	def run(self, timeout):
		def target():
			#print 'Thread started'
			print self.cmd
			self.process = Popen(self.cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
			stream=None
			if self.input_file != '':
				a = open(self.input_file)
				stream  = a.read()
				a.close()
			[self.output,self.error] = self.process.communicate(input=stream)
			#print 'Thread finished'

		thread = threading.Thread(target=target)
		thread.start()

		thread.join(timeout)
		if thread.is_alive():
			#print 'Terminating process'
			self.process.terminate()
			thread.join()
			self.status =-1
		return  [self.process.returncode,self.output,self.error]


#gtp repetido

def compile_code(code_path, filename, compile_line):
	
	compile_line = compile_line.replace('${path}', code_path)
	compile_line = compile_line.replace('${file}', filename)
	compile_line = compile_line.replace('${file_no_ext}', os.path.splitext(filename)[0])
	output = ''
	try:
		process = Popen(compile_line, shell=True, stdout=PIPE, stderr=PIPE)
		(stdout, stderr) = process.communicate()
	except:
		output = [False,  T('Impossible to compile')]

	if (stderr.upper()).find('ERROR') != -1:
		output = [False, stdout + stderr]
	else:
		output =  [True, stdout + stderr]
	
	return output







def execute_code_with_stdin (code_path, filename, filename_stdin, exec_line, exec_params,  my_timeout, max_memory):
	stderr_data  = ''
	output_str = ''
	os.environ['CLASSPATH'] = code_path
	file_no_ext = os.path.splitext(filename)[0]
	exec_line = exec_line.replace('${path}', code_path)
	exec_line = exec_line.replace('${file}', filename)
	exec_line = exec_line.replace('${file_no_ext}', file_no_ext)

	if exec_params == None:
		exec_params = ''
	else:
		exec_params = exec_params.replace('${path}', code_path)
		exec_params = exec_params.replace('${file}', filename)
		exec_params = exec_params.replace('${file_no_ext}', file_no_ext)
	
	cmd0 = [[exec_line, exec_params], '%s/%s' % (code_path, filename_stdin)]
	
	process0 = Command(cmd0[0],cmd0[1])
	a = datetime.datetime.now()
	[status, stdout0, stderr0] = process0.run(timeout=my_timeout)
	b = datetime.datetime.now()
	c = b - a
	if c.seconds > my_timeout:
		print "time exceed"
	
	return [status, stdout0, stderr0]


########
########
########
########
########
########
########



def compile_testing_code(filename, code_src, prog_lang, compile_line):

    code_path = tempfile.mkdtemp()
    os.chmod(code_path, 0o774)
    
    if filename != '':
        code_filename = os.path.join(code_path, filename)
        code_file = open(code_filename,"w+")
        code_file.write(code_src)
        code_file.close()
        #compile_line = db.prog_lang[prog_lang].compile_line
        compile_output = compile_code(code_path, filename, compile_line)
        output = compile_output
    else:
        output = [False, 'No source code file']
    return output + [code_path]


def execute_code (cases_path, code_path, filename, exec_line, exec_params,  n_cases, my_timeout, max_memory):
	stderr_data  = ''
	output_str = ''
	flag = False
	output = ''
	os.environ['CLASSPATH'] = code_path
	file_no_ext = os.path.splitext(filename)[0]
	exec_line = exec_line.replace('${path}', code_path)
	exec_line = exec_line.replace('${file}', filename)
	exec_line = exec_line.replace('${file_no_ext}', file_no_ext)

	if exec_params == None:
		exec_params = ''
	else:
		exec_params = exec_params.replace('${path}', code_path)
		exec_params = exec_params.replace('${file}', filename)
		exec_params = exec_params.replace('${file_no_ext}', file_no_ext)
	AC_counter = 0
	for i in range(n_cases):
		cmd0 = [[exec_line, exec_params], '%s/cases/case_%i.in' % (cases_path, i + 1)]
		cmd1 = '%s/cases/case_%i.out' % (cases_path, i + 1)
		print cmd0[0], cmd0[1]
		process0 = Command(cmd0[0],cmd0[1])
		a = datetime.datetime.now()
		[status, stdout0, stderr0] = process0.run(timeout=my_timeout)
		b = datetime.datetime.now()
		c = b - a
		if c.seconds > my_timeout:
			 print "time exceed"

		stderr_data += stderr0
		case_file = open (cmd1)
		case_output = case_file.read()
		case_file.close()
		if status == -15 or status ==143: # Timelimit
			output_str += 'Test %i: TLE\n'%(i+1)
			flag = True
		elif status == -11: #segmentation fault
			output_str += 'Test %i: RTE\n'%(i+1)
			flag = True
		elif status == 0: # Right answer
			case_output = re.sub(r'\s', '', case_output)
			stdout0 = re.sub(r'\s', '', stdout0)
			if stdout0 == case_output:
				output_str += 'Test %i: AC\n'%(i+1)
				AC_counter += 1
			else:
				output_str += 'Test %i: WA\n'%(i+1)
				flag = True
		else : #unknown error
			output_str += 'Test %i: UE\n'%(i+1)
			flag = True

		if flag == True:
			output = "AE"
		else:
			output = "AC"
                print output
		
	return [output,  output_str, AC_counter, stderr_data]
