# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
	raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
	# ---------------------------------------------------------------------
	# if NOT running on Google App Engine use SQLite or other DB
	# ---------------------------------------------------------------------
	db = DAL(configuration.get('db.uri'),
			 pool_size=configuration.get('db.pool_size'),
			 migrate_enabled=configuration.get('db.migrate'),
			 check_reserved=['all'])
else:
	# ---------------------------------------------------------------------
	# connect to Google BigTable (optional 'google:datastore://namespace')
	# ---------------------------------------------------------------------
	db = DAL('google:datastore+ndb')
	# ---------------------------------------------------------------------
	# store sessions and tickets there
	# ---------------------------------------------------------------------
	session.connect(request, response, db=db)
	# ---------------------------------------------------------------------
	# or store session in Memcache, Redis, etc.
	# from gluon.contrib.memdb import MEMDB
	# from google.appengine.api.memcache import Client
	# session.connect(request, response, db = MEMDB(Client()))
	# ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
	response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

db.define_table('prog_lang',
	Field('prog_lang'),
	Field('compile_line', 'string'),
	Field('exec_line', 'string'),
	Field('exec_params', 'string'),
	Field('ace_mode', 'string'),
	Field('extension', 'string'),
	format='%(prog_lang)s')



auth.settings.extra_fields['auth_user']= [
	Field('self_description', 'text'),
	Field('notify_contests', 'boolean', default = False),
	Field('preferred_language', 'reference prog_lang'),
	Field('nproblems', 'integer', default = 0),
	Field('points', 'integer', default = 0),
  ]
# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.define_tables(username=True, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
#auth.settings.profile_fields =[first_name, last_name, email, username, password]
# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
	from gluon.scheduler import Scheduler
	scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)
db.auth_user.preferred_language.readable = db.auth_user.preferred_language.writable = True
db.auth_user.nproblems.readable = db.auth_user.nproblems.writable = False
db.auth_user.points.readable = db.auth_user.points.writable = False
db.auth_user.nproblems.writable = False



#AC: Accepted
#WA: Wrong Answer
#IR: Invalid Return
#RTE: Runtime Exception
#OLE: Output Limit Exceeded
#MLE: Memory Limit Exceeded
#TLE: Time Limit Exceeded
#IE: Internal Error

#db.auth_user.preferred_language.readable = db.auth_user.preferred_language.writable = True
db.define_table('exec_status',
	Field('acronym'),
	Field('description'),
	format='%(acronym)s'
	)

db.define_table('system_parameters',
		Field('file_size', 'integer'),
		Field('case_size', 'integer'),
		Field('cases_zip_size', 'integer'),
	)

db.define_table('contest',
	Field('user_id','reference  auth_user', default=auth.user_id),
	Field('title', 'string'),
	Field('description', 'text'),
	Field('creation_time', 'datetime', default = request.now),
	Field('start_time', 'datetime'),
	Field('end_time', 'datetime'),
	Field('private_event', 'boolean', default = False),
	Field('approved', 'boolean', default=False),
	format='%(title)s'
)

db.contest.id.readable = db.contest.id.writable = False
db.contest.user_id.readable = db.contest.user_id.writable = False
db.contest.creation_time.readable = db.contest.creation_time.writable = False


db.define_table('problem',
	Field('title', 'string', requires=IS_NOT_EMPTY()),
	Field('user_id','reference auth_user', default=auth.user_id),
	Field('contest_id','reference contest'),
	Field('description', 'text', requires=IS_NOT_EMPTY()),
	Field('points', 'integer'),
	Field('classification', 'string', requires=IS_NOT_EMPTY()),
	Field('n_cases', 'integer', requires=IS_NOT_EMPTY()),
	Field('cases_file', 'upload', uploadfield='blob_cases_file', requires=IS_LENGTH(maxsize=2097152)), # 2MB Max size
	Field('blob_cases_file', 'blob'),
	Field('src_code', 'upload', uploadfield='blob_src_code_file', requires=IS_LENGTH(maxsize=10240)),
	Field('blob_src_code_file', 'blob'),
	Field('timeout', 'integer', default=1, requires=IS_NOT_EMPTY()),
	Field('submitted_language', 'reference prog_lang'),
	Field('max_memory','integer', default=128, requires=IS_NOT_EMPTY()),
	Field('ac', 'integer', default = 100),
	Field('approved', 'boolean', default=False),
	Field('allowed_languages', 'list:reference prog_lang'),
	Field('exec_output', 'text'),
	format='%(title)s'
	)

db.problem.id.readable = db.problem.id.writable = False
db.problem.user_id.readable = db.problem.user_id.writable = False
db.problem.ac.writable = False
db.problem.approved.writable = False
#db.problem.problem_status.requires = IS_IN_SET(('In Progress','Finished', 'For a Contest'))
db.problem.title.requires = IS_NOT_IN_DB(db, 'problem.title')
db.problem.cases_file.requires = IS_NOT_EMPTY()
db.problem.src_code.requires = IS_NOT_EMPTY()
#db.problem.description.readable = db.problem.description.writable = False
#db.problem.cases_file.readable = db.problem.cases_file.writable = False
#db.problem.n_cases.readable = db.problem.n_cases.writable = False
#db.problem.timeout.readable = db.problem.timeout.writable = False
#db.problem.max_memory.readable = db.problem.max_memory.writable = False
#db.problem.problem_status.readable = db.problem.problem_status.writable = False

db.define_table('example',
	Field('problem_id','reference problem'),
	Field('test_in' , 'text', requires = IS_NOT_EMPTY()),
	Field('test_out', 'text', requires = IS_NOT_EMPTY()),
	Field('explanation', 'text'),
	)

db.example.id.readable = db.example.id.writable = False

db.define_table('editorial',
	Field('problem_id','reference problem'),
	Field('description', 'text', requires = IS_NOT_EMPTY()),
	Field('src_code', 'upload', uploadfield='blob_file', requires=IS_LENGTH(maxsize=10240)),
	Field('blob_file', 'blob'),
	)

db.editorial.id.readable = db.editorial.id.writable = False
db.editorial.src_code.requires = IS_NOT_EMPTY()

db.define_table('contest_user',
		Field('user_id','reference auth_user'),
		Field('contest_id','reference contest'),
		Field('n_submissions', 'integer'),
		Field('run_perfect', 'integer'),
		Field('run_with_errors', 'integer'),
		Field('no_compiled', 'integer'),
		Field('score','double'),
	)

db.define_table('submission',
		Field('user_id','reference auth_user', default=auth.user_id),
		Field('problem_id','reference problem', label = T('Problem')),
		Field('prog_lang_id', 'reference prog_lang', label = T('Language')),
		Field('src_code', 'text', requires=IS_LENGTH(maxsize=10240), label = 'T(Code)' ),
		Field('filename', 'string'),
		Field('accepted_on', 'datetime', default=request.now),
		Field('sended_on', 'datetime'),
		Field('output_id', 'string'),
		Field('output_tag', 'string'),
		Field('exec_output', 'text'),
		Field('score','double', default=0.0),
		Field('evaluated', 'boolean', default = False),
	)
db.submission.id.readable = db.submission.id.writable = False
db.submission.user_id.readable = db.submission.user_id.writable = False


db.define_table('solution',
		Field('user_id','reference auth_user', default=auth.user_id),
		Field('problem_id','reference problem', label = T('Problem')),
		Field('prog_lang_id', 'reference prog_lang', label = T('Language')),
		Field('src_code', 'text', requires=IS_LENGTH(maxsize=10240), label = 'T(Code)' ),
		Field('filename', 'string'),
		Field('accepted_on', 'datetime', default=request.now),
		Field('sended_on', 'datetime'),
		Field('output_id', 'reference exec_status'),
		Field('exec_output', 'text'),
		Field('score','double',default=0.0),
	)
db.solution.id.readable = db.solution.id.writable = False
db.solution.user_id.readable = db.solution.user_id.writable = False





db.define_table('staff',
		Field('nickname'),
		Field('user_id','reference  auth_user', default=auth.user_id),
		Field('active_staff', 'boolean'),
		format='%(nickname)s'
	)


db.define_table('faq',
		Field('user_id','reference  auth_user', default=auth.user_id),
		Field('staff_id','reference staff'),
		Field('question'),
		Field('answer','text')
	)


db.define_table('post',
		Field('user_id','reference  auth_user', default=auth.user_id),
		Field('problem_id','reference problem'),
		Field('staff_id','reference staff'),
		Field('question'),
		Field('answer','text')
	)


db.define_table('asdf',
	Field('asdf'),
	auth.signature )

