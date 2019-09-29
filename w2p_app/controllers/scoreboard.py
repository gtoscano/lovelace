@auth.requires_login()
def contest_list():
	#db.contest_user.user_id.default = auth.user_id
	#db.contest_user.user_id.writable = db.contest_user.user_id.readable = False
	fields=[db.contest.id, db.contest.title, db.contest.start_time, db.contest.end_time]
	links = [lambda row: A(SPAN(_class='icon magnifier'), T('View'), _class='btn btn-secondary', _tittle = 'view', _href=URL("scoreboard","list_scoreboard",args=[row.contest.id]), user_signature=True)]
	query = ( (db.contest.id == db.contest_user.contest_id) & (db.contest_user.user_id == auth.user_id))
	#links=links
	form = SQLFORM.grid(query, fields=fields, links=links, paginate=50, maxtextlength=100, csv=False, create=False,  deletable=False, editable=False, details=False, user_signature=True)
	return dict(form=form)
@auth.requires_login()
def list_scoreboard():
	contest_id = 2#request.args(0)
	fields=[db.auth_user.id, db.auth_user.username, db.contest_user.n_submissions,db.contest_user.run_perfect,db.contest_user.run_with_errors, db.contest_user.no_compiled, db.contest_user.score]
	query = ((db.contest_user.contest_id == contest_id) & (db.contest_user.user_id == db.auth_user.id))
	form = SQLFORM.grid(query, fields=fields, orderby=~db.contest_user.score, paginate=5, maxtextlength=100, csv=False, create=False,  deletable=False, editable=False, details=False, user_signature=True)
	return dict(form=form, head_bar = 'Puntuación General')

#from update_scoreboard_module import update_scoreboard_funct




def queue_task():
	scheduler.queue_task('update_score_board', prevent_drift = True, repeats = 5, period = 120*4)


def update_scoreboard_funct():
    contest_id = 2
    contest_users = db(db.contest_user.contest_id == contest_id).select(db.contest_user.ALL)

    for user in contest_users:

        run_perfect = 0
        run_with_errors = 0
        no_compiled = 0
        score =0.0
        n_submissions = 0
        submissions = db(db.submission.user_id == user.id).select(db.submission.ALL)

        for submission in submissions:
            n_submissions += 1
            if submission.output_tag == 'AC':
                run_perfect +=1
            elif submission.output_tag == 'EC':
                no_compiled += 1
            elif submission.output_tag == 'AE':
                run_with_errors +=1
        
        max_values = {}
        submissions = db(db.submission.user_id == user.id).select(db.submission.ALL)

        for submission in submissions:
            max_values[submission.problem_id] = max(max_values.get(submission.problem_id,0), submission.score)
        score = sum(max_values.values())

        db(db.contest_user.user_id==user.id).update(n_submissions=n_submissions, run_perfect=run_perfect, run_with_errors=run_with_errors, no_compiled=no_compiled, score=score)
        db.commit()
    return 

def update_score_board():
    update_scoreboard_funct()
