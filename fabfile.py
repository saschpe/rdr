# -*- coding: utf-8 -*-

from fabric.api import abort, cd, env, local, require, run, settings, sudo
from fabric.contrib.console import confirm

import os


env.project_name = 'rdr'
env.server_name = ''
env.server_user = 'www-data'
env.server_group = 'www-data'
env.webapps_root = '/srv/www/webaps/'

env.project_root = os.path.join(env.webapps_root, env.project_name)
env.activate_script = os.path.join(env.project_root, 'env/bin/active')
env.wsgi_file = os.path.join(env.project_root, 'django.wsgi')
env.repo_root = os.path.join(env.project_root, '')
env.search_index = os.path.join(env.project_root, 'search_index')
env.requirements_file = os.path.join(env.repo_root, 'requirements.txt')
env.manage_dir = os.path.join(env.repo_root, env.project_name)


def production():
    env.hosts = [env.server_name]
prod = production


def virtualenv(command, use_sudo=False):
    if use_sudo:
        func = sudo
    else:
        func = run
    func('source "{0}" && {1}'.format(env.activate_script, command))


def update():
    require('hosts', provided_by=[production])
    with cd(env.repo_root):
        run('git pull origin master')


def install_requirements():
    require('hosts', provided_by=[production])
    virtualenv('pip install -q -r {0}'.format(env.requirements_file))


def manage_py(command, use_sudo=False):
    require('hosts', provided_by=[production])
    with cd(env.manage_dir):
        virtualenv('python manage.py {0}'.format(command), use_sudo)


def syncdb():
    require('hosts', provided_by=[production])
    manage_py('syncdb --noinput')


def migrate():
    require('hosts', provided_by=[production])
    manage_py('migrate')


def schema_migration_auto(app=''):
    require('hosts', provided_by=[production])
    manage_py('schemamigration --auto {0}'.format(app))


def graph_migrations():
    '''Generate a graphviz .dot file for migrations and convert it to PNG.'''
    require('hosts', provided_by=[production])
    manage_py('graphmigrations | dot -Tpng -omigrations.png')


def rebuild_index():
    require('hosts', provided_by=[production])
    manage_py('rebuild_index --noinput', use_sudo=True)
    sudo('chown -R {0}:{1} {2}'.format(env.server_user, env.server_group, env.search_index))


def update_index():
    '''Update the search index.'''
    require('hosts', provided_by=[production])
    manage_py('update_index', use_sudo=True)
    sudo('chown -R {0} .xapian'.format(env.server_user))


def collectstatic():
    require('hosts', provided_by=[production])
    manage_py('collectstatic -l --noinput')


def reload():
    require('hosts', provided_by=[production])
    sudo('supervisorctl status | grep {0} '
        '| sed "s/.*[pid ]\([0-9]\+\)\,.*/\\1/" '
        '| xargs kill -HUP'.format(env.project_name))


def deploy():
    require('hosts', provided_by=[production])
    update()
    install_requirements()
    syncdb()
    migrate()
    collectstatic()
    reload()


def test(args=''):
    manage_py('test ' + args)
   #with settings(warn_only=True):
   #    result = local('./manage.py test ' + args, capture=True)
   #    print result
   #if result.failed and not confirm('Test failed. Continue anyway?'):
   #    abort('Aborting at user request.')


def pep8():
    require('hosts', provided_by=[production])
    to_test = (__file__, env.project_name)
    run('pep8 --ignore=E501 {0}'.format(' '.join(to_test)))
