# -*- coding: utf-8 -*-
@auth.requires_membership('problem_designers')
def proposed():
    fields=[db.contest.title, db.contest.start_time, db.contest.end_time, db.contest.private_event, db.contest.approved]
    links = [lambda row: A(SPAN(_class='icon magnifier'), "View", _class='btn btn-secondary', _tittle = 'view', _href=URL("contest","show_contest", args=[row.id]), user_signature=True),
             #lambda row: A(SPAN(_class='icon magnifier'), "Add problem", _class='btn btn-secondary', _tittle = 'problem', _href=URL("contest","add_problems_to_contest", args=[row.id]), user_signature=True),
             lambda row: A(SPAN(_class='icon magnifier'), "Add users", _class='btn btn-secondary', _tittle = 'users', _href=URL("contest","add_users_to_contest", args=[row.id]),user_signature=True)]
    query = (db.contest.user_id == auth.user_id)
    if request.args(0) == 'new':
        db.contest.approved.readable = db.contest.approved.writable = False
    if request.args(0) == 'edit':
        db.contest.approved.readable = db.contest.approved.writable = True
    form = SQLFORM.grid(query, fields=fields, links=links, paginate=50, maxtextlength=100, csv=False, deletable=False, editable=True, details=False, user_signature=True)
    return dict(form=form, head_bar = 'Administración de Eventos')

#@auth.requires_membership('problem_designers')
#def add_problems_to_contest():
#    contest_id = request.args(0)
#    db.contest_problem.contest_id.default = contest_id
#    db.contest_problem.contest_id.writable = db.contest_problem.contest_id.readable = False
#    fields=[db.contest_problem.problem_id]
#    query  = (db.contest_problem.contest_id == contest_id)
#    form = SQLFORM.grid(query, args=request.args[:1], fields=fields, paginate=50, maxtextlength=100, csv=auth.has_membership('creator_group'), deletable=False, editable=True, details=False, user_signature=True) if auth.user else None
#    #back_button = A(T('Back'), _href=URL('contest', 'function', user_signature=True), _class='btn')
#    return dict(form=form)#, back_button = back_button)


@auth.requires_membership('problem_designers')
def add_users_to_contest():
    contest_id = request.args(0)
    db.contest_user.contest_id.default = contest_id
    fields=[db.contest_user.user_id]
    query = (db.contest_user.contest_id == contest_id )
    form = SQLFORM.grid(query, args=request.args[:1], fields=fields, paginate=50, maxtextlength=100, csv=False, deletable=False, editable=True, details=False, user_signature=True)
    return dict(form=form)


@auth.requires_login()
def list_all():
    fields=[db.contest.id, db.contest.title, db.contest.start_time, db.contest.end_time]
    links = [lambda row: A(SPAN(_class='icon magnifier'), "View", _class='btn btn-secondary', _tittle = 'view', _href=URL("contest","show_contest",args=[row.id])), 
             lambda row: A(SPAN(_class='icon plus'), "Add to my list", _class='btn btn-secondary', _tittle = 'add', _href=URL("contest","add_to_my_list",args=[row.id]), user_signature=True)]
    query = ((db.contest.private_event == False) & (db.contest.approved == True))
    form = SQLFORM.grid(query, fields=fields, links=links, paginate=50, maxtextlength=100, csv=False, create=False, deletable=False, editable=False, details=False, user_signature=True)
    return dict(form=form)

@auth.requires_login()
def on_my_contest_list():
    #db.contest_user.user_id.default = auth.user_id
    #db.contest_user.user_id.writable = db.contest_user.user_id.readable = False
    fields=[db.contest.id, db.contest.title, db.contest.start_time, db.contest.end_time]
    links = [lambda row: A(SPAN(_class='icon magnifier'), T('View'), _class='btn btn-secondary', _tittle = 'view', _href=URL("contest","show_contest",args=[row.contest.id]), user_signature=True),
    lambda row: A(SPAN(_class='icon magnifier'), T('Problems'), _class='btn btn-secondary', _tittle = 'view', _href=URL("problem","list_problems_in_contest",args=[row.contest.id]), user_signature=True)]
    query = ( (db.contest.id == db.contest_user.contest_id) & (db.contest_user.user_id == auth.user_id))
    #links=links
    form = SQLFORM.grid(query, fields=fields, links=links, paginate=50, maxtextlength=100, csv=False, create=False,  deletable=False, editable=False, details=False, user_signature=True)
    return dict(form=form)

@auth.requires_login()
def show_contest():
    contest_id = request.args(0)
    contest = db.contest(contest_id) or redirect(URL('index'))
    contest_data = "####%s\nFecha de inicio: **%s**\n Fecha de Término: **%s**\n" %(contest.description, str(contest.start_time), str(contest.end_time))
    return dict(contest=contest_data, head_bar = 'Detalles: %s'%(contest.title))

@auth.requires_login()
def add_to_my_list():
    contest_id = request.args(0)
    db.contest_user.update_or_insert(user_id = auth.user_id, contest_id = contest_id)
    redirect(URL('contest','on_my_contest_list'))
