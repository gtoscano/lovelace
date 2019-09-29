# -*- coding: utf-8 -*-

@auth.requires_login()
def list_all():
	fields=[db.solution.id, db.problem.title,  db.problem.points, db.solution.sended_on, db.solution.score]
	links = [lambda row: A(SPAN(_class='icon magnifier'), "View", _class='btn btn-secondary', _tittle = 'view', _href=URL("solution","show_solution",args=[row.solution.id]))]
	query = ((db.solution.user_id == auth.user_id) & (db.problem.id == db.solution.problem_id))
	form = SQLFORM.grid(query, fields=fields, links=links, paginate=50, maxtextlength=100, csv=False, create=False, deletable=False, editable=False, details=False, user_signature=True ) if auth.user else None
	return dict(form=form)

@auth.requires_login()
def show_solution():
	solution_id = request.args(0)
	solution = db.contest(solution_id) or redirect(URL('index'))
	return dict(solution=solution)


@auth.requires_login()
def list_by_problem():
	links = [lambda row: A(SPAN(_class='icon magnifier'), "View", _class='btn btn-secondary', _tittle = 'view', _href=URL("solution","show_solution_by_problem",args=[row.problem_id]))]
	query = (db.problem_user.user_id == auth.user_id)
	form = SQLFORM.grid(query)#, fields=fields, links=links, paginate=50, maxtextlength=100, csv=False, create=False, deletable=False, editable=False, details=False, user_signature=True ) if auth.user else None
	return dict(form=form)


@auth.requires_login()
def list_by_contest():
	fields=[db.contest_user.contest_id]
	links = [lambda row: A(SPAN(_class='icon magnifier'), "View", _class='btn btn-secondary', _tittle = 'view', _href=URL("solution","show_solution_by_contest",args=[row.contest_id]))]
	query = (db.contest_user.user_id == auth.user_id)
	form = SQLFORM.grid(query, links=links, fields=fields,  paginate=50, maxtextlength=100, csv=False, create=False, deletable=False, editable=False, details=False, user_signature=True ) if auth.user else None
	return dict(form=form)

@auth.requires_login()
def show_solution_by_contest():
	contest_id = request.args(0)
	#print contest_id
	#fields=[db.solution.id, db.solution.sended_on, db.solution.score]
	#links = [lambda row: A(SPAN(_class='icon magnifier'), "View", _class='btn btn-secondary', _tittle = 'view', _href=URL("solution","show_solution",args=[row.id]))]
	query = (db.solution.user_id == auth.user_id) 
	print query
	form = SQLFORM.grid(query)#, fields=fields, links=links, paginate=50, maxtextlength=100, csv=False, create=False, deletable=False, editable=False, details=False, user_signature=True ) if auth.user else None
	return dict(form=form)

@auth.requires_login()
def list_solution_by_contest():
	contest_id = request.args(0)
	#print contest_id
	#fields=[db.solution.id, db.solution.sended_on, db.solution.score]
	#links = [lambda row: A(SPAN(_class='icon magnifier'), "View", _class='btn btn-secondary', _tittle = 'view', _href=URL("solution","show_solution",args=[row.id]))]
	query = (db.solution) 
	print query
	form = SQLFORM.grid(query)#, fields=fields, links=links, paginate=50, maxtextlength=100, csv=False, create=False, deletable=False, editable=False, details=False, user_signature=True ) if auth.user else None
	return dict(form=form)

def compile():
	solution_id  = 1
	work_dir = '%s/%s/'%(request.folder, 'data')
	cases_dir = '%s/cases/' % (work_dir)
	user_dir = '%s/%s/'%(work_dir,'codes')
	
	if not os.path.exists(user_dir):
		os.makedirs(user_dir)
