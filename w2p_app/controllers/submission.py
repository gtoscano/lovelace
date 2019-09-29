# -*- coding: utf-8 -*-
import tempfile
import os
import zipfile
from subprocess import PIPE, Popen
import shutil
import datetime
import threading
import re

@auth.requires_login()
def list_all():
	fields=[db.submission.id, db.problem.title,  db.problem.points, db.submission.sended_on, db.submission.output_tag,  db.submission.score]
	links = [lambda row: A(SPAN(_class='icon magnifier'), "View", _class='btn btn-secondary', _tittle = 'view', _href=URL("submission","show_submission",args=[row.submission.id]))]
	query = ((db.submission.user_id == auth.user_id) & (db.problem.id == db.submission.problem_id))
	form = SQLFORM.grid(query, fields=fields, links=links, orderby=~db.submission.sended_on, paginate=50, maxtextlength=100, csv=False, create=False, deletable=False, editable=False, details=False, user_signature=True ) if auth.user else None
	return dict(form=form, head_bar = 'Listado de envíos')

@auth.requires_membership('admin')
def list_all_all_users():
	form = SQLFORM.grid(db.submission, orderby=~db.submission.sended_on, paginate=50, maxtextlength=100, csv=False, create=False, deletable=False, editable=True, details=True, user_signature=True ) if auth.user else None
	return dict(form=form, head_bar = 'Listado de envíos')


@auth.requires_login()
def show_submission():
	submission_id = request.args(0)
	submission = db.submission(submission_id) or redirect(URL('index'))
	if submission.evaluated == True:
		code = submission.src_code
		label_text2 = 'El código enviado es el siguiente:'
		feedback = submission.exec_output 
		label_text1 = 'Tu solución obtuvo **%.2f** puntos. \n\n\nLa retroalimentación de tu programa es la siguiente:\n\n'%(submission.score)
	else:
		code = ''
		label_text1 = 'Tu código no ha sido evaluado'
		label_text2 = ''
		feedback = ''

	return dict(label_text1=label_text1, label_text2=label_text2, code = code, feedback =feedback, head_bar = 'Detalles del envío')


@auth.requires_login()
def list_by_problem():
	problem_id = request.args(0)
	fields=[db.submission.id, db.submission.problem_id, db.problem.points, db.submission.sended_on, db.submission.score]
	links = [lambda row: A(SPAN(_class='icon magnifier'), "View", _class='btn btn-secondary', _tittle = 'view', _href=URL("submission","show_submission",args=[row.id]), user_signature=True)]
	query = ((db.submission.problem_id == problem_id) & (db.submission.user_id == auth.user_id))
	form = SQLFORM.grid(query, fields=fields, links=links, paginate=25, maxtextlength=100, csv=False, create=False, deletable=False, editable=False, details=False, user_signature=False,) if auth.user else None
	return dict(form=form)



def queue_task():
	scheduler.queue_task('compile_and_execute_remaining_submissions', prevent_drift = True, repeats = 5, period = 300)
	

def compile_and_execute_all_submissions():
	rows = db(db.submission.id>0).select()
	for row in rows:
		print row.id
		compile_and_execute_submission(row.id)

        
from compile_and_execute_code import execute_code, compile_code, compile_testing_code



def execute_problem_tester(problem_id, code_path, cases_path, filename, submitted_language):
    problem = db.problem[problem_id]
    n_cases = problem.n_cases
    my_timeout = problem.timeout
    max_memory = problem.max_memory
    points = problem.points
        
    exec_line = db.prog_lang[submitted_language].exec_line
    exec_params = db.prog_lang[submitted_language].exec_params
    [output,  output_str, AC_counter, stderr_data] = execute_code (cases_path, code_path, filename, exec_line, exec_params,  n_cases, my_timeout, max_memory)
    stderr_data = stderr_data.replace(code_path,'')
    return [output,  output_str, points*AC_counter/float(n_cases), stderr_data]





def compile_and_execute_submission(submission_id):
    submission = db.submission[submission_id]
    submitted_language = submission.prog_lang_id
    prog_lang = submission.prog_lang_id
    compile_line = db.prog_lang[prog_lang].compile_line
    cases_path = '%s/data/cases/%i' % (request.folder, submission.problem_id)

    [comp_success, comp_output, code_path] = compile_testing_code(submission.filename, submission.src_code, prog_lang, compile_line)

    if comp_success == True:

        [output,  output_str, score, stderr_data] = execute_problem_tester(submission.problem_id, code_path, cases_path, submission.filename,submitted_language)
        exec_output = '%s\n%s'%(str(output_str), str(stderr_data))
        exec_output = exec_output.replace(code_path,'')
        #submission['output_id'] = output_id
        #submission.update_record()
        #query = (db.submission.id == submission_id) & (db.submission.user_id == auth.user_id) & (db.submission.problem_id == submission.problem_id))
        db(db.submission.id == submission_id).update(output_tag = output, score = score, exec_output=exec_output, evaluated=True)
        db.commit()
    else:
        comp_output = comp_output.replace(code_path,'')
        db(db.submission.id == submission_id).update(output_tag = 'CE', score = 0.0, exec_output=comp_output, evaluated=True)
        db.commit()
    
    return dict()

def compile_and_execute_remaining_submissions():
    rows = db(db.submission.output_tag == None).select()
    for row in rows:
        print row.id
        compile_and_execute_submission(row.id)

    return dict()
