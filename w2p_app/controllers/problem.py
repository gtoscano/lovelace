# -*- coding: utf-8 -*-

import os
import zipfile
from subprocess import PIPE, Popen
import shutil
import datetime
import threading
import re
import tempfile

@auth.requires_membership('problem_designers')
def proposed():
	fields=[db.problem.title, db.problem.classification, db.problem.approved, db.problem.ac]
	links = [lambda row: A(SPAN(_class='icon magnifier'), "View", _class='btn btn-secondary', _tittle = 'view', _href=URL("problem","show_problem",args=[row.id]), user_signature=True),
			 lambda row: A(SPAN(_class='icon magnifier'), "Examples", _class='btn btn-secondary', _tittle = 'view', _href=URL("problem","list_examples",args=[row.id]), user_signature=True),
			 lambda row: A(SPAN(_class='icon magnifier'), "Editorial", _class='btn btn-secondary', _tittle = 'view', _href=URL("problem","list_editorial",args=[row.id]), user_signature=True),
			 lambda row: A(SPAN(_class='icon magnifier'), "Approve", _class='btn btn-secondary', _tittle = 'view', _href=URL("problem","compile_and_execute_problem_tester",args=[row.id]), user_signature=True)]
	query = (db.problem.user_id == auth.user_id)
	if request.args(0) == 'new' or request.args(0) == 'edit':
		db.problem.ac.writable = db.problem.ac.readable = False
		db.problem.approved.writable = False
	form = SQLFORM.grid(query, fields=fields, links=links, paginate=25, maxtextlength=100, csv=False, deletable=False, editable=True, details=False, user_signature=True) if auth.user else None
	return dict(form=form, head_bar = 'Problemas Propuestos')

@auth.requires_membership('problem_designers')
def list_examples():
	problem_id = request.args(0)
	db.example.problem_id.default = problem_id
	db.example.problem_id.writable = db.example.problem_id.readable = False
	form = SQLFORM.grid(db.example.problem_id == problem_id, args=request.args[:1], paginate=25, maxtextlength=100, csv=False, deletable=True, editable=True, details=False, user_signature=False) if auth.user else None
	return dict(form=form, head_bar = 'Administración de Ejemplos')

@auth.requires_membership('problem_designers')
def list_editorial():
	problem_id = request.args(0)
	db.editorial.problem_id.default = problem_id
	db.editorial.problem_id.writable = db.editorial.problem_id.readable = False
	form = SQLFORM.grid(db.editorial.problem_id == problem_id, args=request.args[:1], paginate=25, maxtextlength=100, csv=False, deletable=True, editable=True, details=False, user_signature=False) if auth.user else None
	return dict(form=form, head_bar = 'Administración de Editoriales')

@auth.requires_membership('problem_designers')
def list_all():
	fields=[db.problem.title, db.problem.classification, db.problem.ac]
	links = [lambda row: A(SPAN(_class='icon magnifier'), "View", _class='btn btn-secondary', _tittle = 'view', _href=URL("problem","show_problem",args=[row.id]), user_signature=True), 
			 lambda row: A(SPAN(_class='icon plus'), "Add to my list", _class='btn btn-secondary', _tittle = 'add', _href=URL("problem","add_to_my_list",args=[row.id]), user_signature=True)]
	query = ((db.problem.approved == True) )
	form = SQLFORM.grid(query, fields=fields, links=links, paginate=25, maxtextlength=100, csv=False, create=False, deletable=False, editable=False, details=False, user_signature=False,) if auth.user else None
	return dict(form=form, head_bar = 'Listado de Problemas')

def list_problems_in_contest():
	contest_id = request.args(0)
	now = datetime.datetime.now()
	if now < db.contest[contest_id].start_time:
		session.flash = (T('This contest has not started yet'))
		redirect(URL('contest','on_my_contest_list'))
	if now > db.contest[contest_id].end_time:
		session.flash = (T('This contest has already finished'))
		redirect(URL('contest','on_my_contest_list'))

	fields=[db.problem.title, db.problem.classification, db.problem.ac]
	links = [lambda row: A(SPAN(_class='icon magnifier'), "View", _class='btn btn-secondary', _tittle = 'view', _href=URL("problem","show_problem",args=[row.id]), user_signature=True), 
			 lambda row: A(SPAN(_class='icon plus'), "Solve", _class='btn btn-secondary', _tittle = 'add', _href=URL("coder","solve_problem",args=[row.id]), user_signature=True),
			 lambda row: A(SPAN(_class='icon plus'), "Submissions", _class='btn btn-secondary', _tittle = 'add', _href=URL("submission","list_by_problem",args=[row.id]), user_signature=True)]
	query = ((db.problem.approved == True) & (db.problem.contest_id == contest_id) )
	form = SQLFORM.grid(query, fields=fields, links=links, paginate=25, maxtextlength=100, csv=False, create=False, deletable=False, editable=False, details=False, user_signature=False,) if auth.user else None
	return dict(form=form)



@auth.requires_login()
def show_problem():
	problem_id = request.args(0)
	problem = db.problem(problem_id) or redirect(URL('index'))
	examples = db(db.example.problem_id == problem_id).select()
	return dict(problem=problem, examples = examples)

#@auth.requires_membership('problem_designers')
def donwload_all_test_cases():
	zips = ''
	problems = db().select(db.problem.ALL)
	for problem in problems:
		cases_path = '%s/data/cases/%i' % (request.folder, problem.id)
		if not os.path.exists(cases_path):
			os.makedirs(cases_path)
		try:
			(filename, stream) = db.problem.cases_file.retrieve(problem.cases_file)
			shutil.copyfileobj(stream, open('%s/%s'%(cases_path,filename), 'wb'))
			stream.close()
			zip_cmd = 'unzip -o %s/%s -d %s '%(cases_path, filename, cases_path)
			process = Popen(zip_cmd, shell=True)
			process.communicate()
		except:
			return False
	return True



def donwload_test_cases(problem_id):
	#problem_id = request.args(0)
	problem = db.problem[problem_id]
	cases_path = '%s/data/cases/%i' % (request.folder, problem.id)

	if not os.path.exists(cases_path):
		os.makedirs(cases_path)
	try:
		(filename, stream) = db.problem.cases_file.retrieve(problem.cases_file)
		shutil.copyfileobj(stream, open('%s/%s'%(cases_path,filename), 'wb'))
		stream.close()
		zip_cmd = 'unzip -o %s/%s -d %s '%(cases_path, filename, cases_path)
		process = Popen(zip_cmd, shell=True)
		process.communicate()
	except:
		return dict(message ='not possible')
	return dict()
'''
https://icpc.baylor.edu/worldfinals/programming-environment


# Compilation of Submissions

During the contest, teams will submit proposed solutions to the contest problems to the Judges using the DOMJudge contest control system. Source files submitted to the Judges will be compiled using the following command line arguments for the respective language:



C:

gcc -g -O2 -std=gnu11  -lm ${path}${file} -o ${path}/${file_no_ext}

C++11:
g++ -g -O2 -std=c++11  ${file} -o ${path}/${file_no_ext}

C++14:
g++ -g -O2 -std=c++14  ${file} -o ${path}/${file_no_ext}

C++17:
g++ -g -O2 -std=c++17  ${file} -o ${path}/${file_no_ext}

Java:
javac -encoding UTF-8 -sourcepath . -d . ${path}/${file}

java -Dfile.encoding=UTF-8 -XX:+UseSerialGC -Xss64m -Xms1920m -Xmx1920m

java -Dfile.encoding=UTF-8 -XX:+UseSerialGC -Xss64m -Xms1920m -Xmx1920m -cp codes; suma
java -Dfile.encoding=UTF-8 -XX:+UseSerialGC -Xss64m -Xms1920m -Xmx1920m -cp codes suma

Python 3
python3 -m py_compile ${file}

Kotlin
kotlinc -d . ${file}

The "${files}" in the above commands represents the list of source files from the submission which will actually be compiled. Files with the following suffixes (and only files with these suffixes) will be submitted to the compiler:

For C submissions: files ending with .c
For C++ submissions: files ending with .cc, .cpp, .cxx, or .c++
For Java submissions: files ending with .java
For Python submissions: files ending with .py
For Kotlin submissions: files ending with .kt

'''

from compile_and_execute_code import compile_code, execute_code

def compile_problem_tester(problem_id):

	problem = db.problem[problem_id]
	cases_path = '%s/data/cases/%i' % (request.folder, problem.id)

	code_path = tempfile.mkdtemp()
	os.chmod(code_path, 0o774)
	(filename, stream) = db.problem.src_code.retrieve(problem.src_code)
	if filename != '':
		shutil.copyfileobj(stream, open('%s/%s'%(code_path,filename), 'wb'))
		stream.close()
		compile_line = db.prog_lang[problem.submitted_language].compile_line
		output = compile_code(code_path, filename, compile_line)
	else:
		output = [False, 'No source code file']
	return [output, code_path, cases_path]

def compile_problem_tester22():
	problem_id = 1
	[output, code_path, cases_path] = compile_problem_tester(problem_id)
	return dict(output=output, code_path=code_path, cases_path=cases_path)




	#except:
	#	return ['UE', 'No source code', 0, '']	
	#return ['UE', 'No source code', 0, '']

def execute_problem_tester(problem_id, code_path, cases_path, filename):
	problem = db.problem[problem_id]
	n_cases = problem.n_cases
	my_timeout = problem.timeout
	submitted_language = problem.submitted_language 
	max_memory = problem.max_memory
	#points = problem.points
		
	exec_line = db.prog_lang[submitted_language].exec_line
	exec_params = db.prog_lang[submitted_language].exec_params
	os.environ['CLASSPATH'] = code_path

	[output,  output_str, RA_counter, stderr_data] = execute_code (cases_path, code_path, filename, exec_line, exec_params,  n_cases, my_timeout, max_memory)
	stderr_data = stderr_data.replace(code_path,'')
	return [output,  output_str, RA_counter, stderr_data]


	

def compile_and_execute_problem_tester():
	problem_id = request.args(0)
	problem = db.problem[problem_id]
	donwload_test_cases(problem_id)
	
	[output, code_path, cases_path] = compile_problem_tester(problem_id)
	
	if output[0] == True:
		(filename, stream) = db.problem.src_code.retrieve(problem.src_code)
		stream.close()
		[output,  output_str, RA_counter, stderr_data] = execute_problem_tester(problem_id, code_path, cases_path, filename)
		
		if output == 'AC':
			db(db.problem.id == problem_id).update(approved=True, exec_output='%s\n%s'%(str(output_str), str(stderr_data)))
			return dict(message = 'Accepted', head_bar = 'Listado de Problemas')
			#db(db.problem.id == problem.id).update(output_id=output_id, well_ended=right_ending_counter ,right_answers=right_answer_counter, wrong_answers=wrong_answer_counter, broken_programs=segmentation_fault_counter,  expired_time=time_limit_counter, messages=messages,score=score)
		else:
			db(db.problem.id == problem_id).update(approved=False, exec_output='%s\n%s'%(str(output_str), str(stderr_data)))
			return dict(message = 'Not accepted %s'%(str(output_str), str(stderr_data)), head_bar = 'Listado de Problemas')
	db(db.problem.id == problem_id).update(approved=False, exec_output='')
	return dict(message = 'Not accepted', head_bar = 'Listado de Problemas')
