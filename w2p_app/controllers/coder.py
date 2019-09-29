# -*- coding: utf-8 -*-
"""
| This file is part of the  Framework
| Copyrighted by Gregorio Toscano <gtoscano@gmail.com>
| License: LGPLv3 (http://www.gnu.org/licenses/lgpl.html)

Background processes made simple
---------------------------------
"""

import os
import datetime
import time
import tempfile
import shutil
import javalang
def my_problems():
	my_problems = db(db.problem).select()
	return dict(my_problems=my_problems)


from compile_and_execute_code import compile_code, execute_code_with_stdin, compile_testing_code
	




def execute_testing_code(code_path, filename, stdin_name,  prog_lang):
	my_timeout = 1
	max_memory = 128*1024
		
	exec_line = db.prog_lang[prog_lang].exec_line
	exec_params = db.prog_lang[prog_lang].exec_params
	[status, stdout0, stderr0] = execute_code_with_stdin (code_path, filename, stdin_name, exec_line, exec_params,  my_timeout, max_memory)
	return [status, stdout0, stderr0]

def compile_and_execute_testing_code(code_src, code_stdin, filename, prog_lang):
	
	compile_line = db.prog_lang[prog_lang].compile_line
	[comp_success, comp_output, code_path] = compile_testing_code(filename, code_src, prog_lang, compile_line)
	stdin_name = 'stdin.txt'
	stdin_filename = os.path.join(code_path, stdin_name)
	stdin_file = open(stdin_filename,"w+")
	stdin_file.write(code_stdin)
	stdin_file.close()

	if comp_success == True:
		os.environ['CLASSPATH'] = code_path
		[status, stdout0, stderr0] = execute_testing_code(code_path, filename, stdin_name, prog_lang)
		execute_output = 'STATUS: %s\nSTDOUT: %s\nSTDERR: %s\n' % (status, stdout0, stderr0)

		return execute_output

	comp_output = comp_output.replace(code_path,'')
	comp_output = 'STDERR: %s' %(comp_output)
	#shutil.rmtree(code_path)
	return comp_output

def compile_and_execute_test():
	code_src = '#include<stdio.h>\nint main() {\nprintf("hola mundo");\n}\n'
	code_stdin = 'a'
	prog_lang = 1
	filename = 'test.c'
	output = compile_and_execute_testing_code(code_src, code_stdin, filename, prog_lang)


def test_compile_and_execute():
	code_src, code_stdin, filename, prog_lang = '#include', '', 'temp.cpp', 3
	output = compile_and_execute_testing_code(code_src, code_stdin, filename, prog_lang)

def compile_and_execute():

	#print request.vars
	
	code_stdin = ""
	code_src = ""
	to_stdout = {}
	# Evaluar que se recibe parametros desde el cliente
	if len(request.vars) > 0:
		# asignar a la variable local el valor del parametro recibido
		code_src = request.vars.code_src
		code_stdin = request.vars.code_stdin
		prog_lang = request.vars.prog_lang
		#print "Code src -> ", code_src
		#print "Stdin -> ", code_stdin
		#print "Prog_lang -> ", prog_lang
		filename = ''
		if 'Java' in db.prog_lang[prog_lang].prog_lang and code_src.find('main') == -1: #it does not contains main
			to_stdout = {
				"stdout":'No main function'
			}
			return response.json(to_stdout)
		if 'Java' in db.prog_lang[prog_lang].prog_lang:
			tree = javalang.parse.parse(code_src)
			filename = next(klass.name for klass in tree.types if isinstance(klass, javalang.tree.ClassDeclaration) for m in klass.methods if m.name == 'main' and m.modifiers.issuperset({'public', 'static'}))
			filename += db.prog_lang[prog_lang].extension
		else:
			filename = 'test'+db.prog_lang[prog_lang].extension
		
		output = compile_and_execute_testing_code(code_src, code_stdin, filename, prog_lang)
		# En la salida crear un objeto json con parametros (por ejemplo) o una respuesta en texto plano
		to_stdout = {
			"stdout":output
		}
		
		#return response.json(to_stdout)
	
	return response.json(to_stdout)
	
	#to_stdout = "salida"
	#return DIV("Message posted")
	#return "jQuery('#edit_stdout').html(%s);" % repr(request.vars.src_code)



@auth.requires_login()
def solve_problem():
	#onchange property
	problem_id = request.args(0)
	problem = db.problem(problem_id) or redirect(URL('index'))
	prog_lang = db(db.prog_lang).select(db.prog_lang.ALL)
	examples = db(db.example.problem_id == problem_id).select()
	preferred_prog_lang = int(db.auth_user[auth.user_id].preferred_language)
	now = datetime.datetime.now()
	if now < db.contest[problem.contest_id].start_time:
		session.flash = (T('This contest has not started yet'))
		redirect(URL('contest','on_my_contest_list'))
	if now > db.contest[problem.contest_id].end_time:
		session.flash = (T('This contest has already finished'))
		redirect(URL('contest','on_my_contest_list'))
	

	form_src = FORM('', INPUT(_name='prog_lang',_id='prog_lang', _type='hidden'), INPUT(_name='src_code',_id='src_code', _type='hidden'), INPUT(_name='src_stdin',_id='src_stdin', _type='hidden'), INPUT(_name='prog_lang',_id='prog_lang', _type='hidden'),  INPUT(_class='btn btn-primary',_type='submit'), formstyle='bootstrap4_inline')

	form_src.element(_type='submit')['_value'] = T("Submit Code")

	posts= db(db.post.problem_id == problem_id).select()
	form_post = SQLFORM.factory(Field('question', label='¿Quieres preguntar algo?, pregúntalo aquí', requires=IS_NOT_EMPTY()), table_name='dummy_question_table')
	
	# Revisar validacion del formulario del editor de codigo
	if form_src.validate():
		# Obtener el valor del campo oculto
		src_code = form_src.vars.src_code
		prog_lang =  form_src.vars.prog_lang
		filename =  form_src.vars.filename
		received_prog_lang =  int(form_src.vars.prog_lang[0])
		
		# Imprimir en la terminal el valor
		selected_output = db().select(db.exec_status.ALL).first()
		previously_sent = db((db.submission.user_id==auth.user_id) & (db.submission.problem_id == problem_id)).select().first()
		if previously_sent != None:
			accepted_on = previously_sent.accepted_on
		else:
			accepted_on = datetime.datetime.now()
		now = datetime.datetime.now()
		#if (now - accepted_on ) >= datetime.timedelta(seconds=5*60*60):
		#	session.flash = 'Tus 5 horas han transcurrido, ya no puedes enviar más soluciones de este desafío.'
		#	redirect(URL('problem','list_problems_in_contest',args=[db.problem[problem_id].contest_id]))


		#db(db.submission.id == form.vars.id).update(problem_id = problem_id, user_id = auth.user_id, output_id = selected_output, accepted_on = accepted_on, sended_on=now )

		#idx = db.submission.insert(problem_id = problem_id, prog_lang_id= form_src.vars.prog_lang, src_code = src_code, output_id = selected_output, sended_on=now)
		if 'Java' in db.prog_lang[received_prog_lang].prog_lang:
			tree = javalang.parse.parse(src_code)
			filename = next(klass.name for klass in tree.types if isinstance(klass, javalang.tree.ClassDeclaration) for m in klass.methods if m.name == 'main' and m.modifiers.issuperset({'public', 'static'}))
			filename += db.prog_lang[received_prog_lang].extension
		else:
			filename = 'test'+db.prog_lang[received_prog_lang].extension
		idx = db.submission.insert(problem_id = problem_id, filename = filename, prog_lang_id= received_prog_lang, src_code = src_code, output_id = selected_output, sended_on=now)
		redirect(URL('problem','list_problems_in_contest',args=[db.problem[problem_id].contest_id]))



	if form_post.process(formname='my_post').accepted:
		db.post.insert(problem_id=problem_id,user_id=auth.user_id,question=form_post.vars.question)
		session.flash = 'Pregunta enviada'
		redirect(URL('problem','list_problems_in_contest',args=[db.problem[problem_id].contest_id]))


	return dict(problem=problem, examples = examples, form = 'hello', preferred_prog_lang = 4, prog_lang = prog_lang, form_src = form_src,  posts = posts, form_post = form_post)

