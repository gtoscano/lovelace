# -*- coding: utf-8 -*-
@auth.requires_membership('admin')
def list_parameters():
	form = SQLFORM(db.system_parameters) if auth.user else None
	return dict(form=form, head_bar = 'Administración de Parámetros del Sistema')


@auth.requires_membership('admin')
def list_languages():
	form = SQLFORM.grid(db.prog_lang, paginate=50, maxtextlength=100, csv=True, create=True, deletable=True, editable=True, details=True, user_signature=True,) if auth.user else None
	return dict(form=form, head_bar = 'Administración de Lenguajes Aceptados')

@auth.requires_membership('admin')
def list_exec_status():
	form = SQLFORM.grid(db.exec_status, paginate=50, maxtextlength=100, csv=True, create=True, deletable=True, editable=True, details=True, user_signature=True,) if auth.user else None
	return dict(form=form, head_bar = 'Administración de Estados de ejecución')

@auth.requires_membership('admin')
def list_users():
	links = [lambda row: A(SPAN(_class='icon magnifier'), 'Membership',_class='btn btn-secondary', _href=URL("manage","add_membership",args=[row.id], user_signature=True))]
	form = SQLFORM.grid(db.auth_user, links=links, paginate=50, maxtextlength=100, csv=True, create=True, deletable=True, editable=True, details=True, user_signature=True,) if auth.user else None
	return dict(form=form, head_bar = 'Administración de Usuarios')

@auth.requires_membership('admin')
def list_groups():
	form = SQLFORM.grid(db.auth_group, paginate=50, maxtextlength=100, csv=True, create=True, deletable=True, editable=True, details=True, user_signature=True,) if auth.user else None
	return dict(form=form, head_bar = 'Administración de Usuarios')

@auth.requires_membership('admin')
def list_memberships():
	form = SQLFORM.grid(db.auth_membership, paginate=50, maxtextlength=100, csv=True, create=True, deletable=True, editable=True, details=True, user_signature=True,) if auth.user else None
	return dict(form=form, head_bar = 'Administración de Usuarios')


@auth.requires_membership('admin')
def add_membership():
	user_id = request.args(0)
	db.auth_membership.user_id.default = user_id
	db.auth_membership.user_id.writable = db.auth_membership.user_id.readable = False

	form = SQLFORM.grid(db.auth_membership.user_id == user_id, args=request.args[:1], paginate=50, maxtextlength=100, csv=True, create=True, deletable=True, editable=True, details=True, user_signature=True,) if auth.user else None
	return dict(form=form, head_bar = 'Administración de Usuarios')


