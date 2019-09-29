# -*- coding: utf-8 -*-
#response.logo = A(B(SPAN('ASOJ')),XML('<sub><small><small><small><em>@Cinvestav</em></small></small></small></sub>'),
#                  _class="brand",_href="http://www.tamps.cinvestav.mx/")
#response.title = 'ASOJ'
#response.subtitle = T('@Cinvestav-Tamaulipas')

## read more at http://dev.w3.org/html5/markup/meta.name.html
#response.meta.author = 'Gregorio Toscano <gtoscano@cinvestav.mx>'
#response.meta.description = 'A Simple Online Judge, Cinvestav-Tamaulipas'
#response.meta.keywords = 'Online judge, Tam-Coder, Cinvestav-Tamaulipas, tamcoder, concurso programación'
#response.meta.generator = 'Web2py Web Framework'


# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
]

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

if not configuration.get('app.production'):
    _app = request.application
    response.menu += [
        (T('Contests'), False, '#', [
            (T('List all'), False, URL('contest', 'list_all')),
            (T('On my list'), False, URL('contest', 'on_my_contest_list')),
        ]),
        (T('Submissions'), False, URL('submission', 'list_all')),
        (T('Scoreboard'), False, URL('scoreboard', 'list_scoreboard')),
        (T('Architects'), False, '#', [
            (T('List of Problems'), False, URL('problem', 'list_all')),
            (T('Proposed Problems'), False, URL('problem', 'proposed')),
            (T('Proposed Contest'), False, URL('contest', 'proposed')),
        ]),
        (T('Admin'), False, '#', [
            (T('Parameters'), False, URL('manage', 'list_parameters')),
            (T('Languages'), False, URL('manage', 'list_languages')),
            (T('Exec status'), False, URL('manage', 'list_exec_status')),
            (T('Users'), False, URL('manage', 'list_users')),
            (T('Submissions'), False, URL('submission', 'list_all_all_users')),
            (T('Groups'), False, URL('manage', 'list_groups')),
            (T('Membership'), False, URL('manage', 'list_memberships')),
        ]),
        (SPAN('Documentación'), False, '', [
                (T('Manual de referencia C'), False,'https://code-reference.com/c'),
                (T('Manual de referencia C++'), False,'http://www.cplusplus.com/reference/'),
                (T('Manual de referencia Java'), False,'http://docs.oracle.com/javase/specs/jls/se11/html/index.html'),
            ])
    ]
