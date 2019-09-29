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
        compile_and_execute_submission(row.id)

compile_and_execute_remaining_submissions()
