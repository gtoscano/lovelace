def update_scoreboard_funct():
    contest_id = 2
    contest_users = db(db.contest_user.contest_id == contest_id).select(db.contest_user.ALL)

    for contest_user in contest_users:
        print (contest_user.id)
        run_perfect = 0
        run_with_errors = 0
        no_compiled = 0
        score =0.0
        n_submissions = 0
        submissions = db((db.submission.user_id == contest_user.user_id) ).select(db.submission.ALL)

        for submission in submissions:
            n_submissions += 1
            if submission.output_tag == 'AC':
                run_perfect +=1
            elif submission.output_tag == 'EC':
                no_compiled += 1
            elif submission.output_tag == 'AE':
                run_with_errors +=1
        
        max_values = {}
        submissions = db(db.submission.user_id == contest_user.user_id).select(db.submission.ALL)

        for submission in submissions:
            max_values[submission.problem_id] = max(max_values.get(submission.problem_id,0), submission.score)
        score = sum(max_values.values())

        db(db.contest_user.user_id==contest_user.user_id).update(n_submissions=n_submissions, run_perfect=run_perfect, run_with_errors=run_with_errors, no_compiled=no_compiled, score=score)
        db.commit()
    return 


update_scoreboard_funct()

