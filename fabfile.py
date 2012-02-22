from fabric.api import abort, cd, local, require, run, settings
from fabric.contrib.console import confirm


# Generic tasks

def hello():
    print("Hello world!")


def host_type():
    run('uname -s')


# Django tasks

def syncdb():
    '''Run syncdb.'''
    require('site_path')
    require('venv_path')

    with cd(env.site_path):
        run(_python('manage.py syncdb --noinput'))


def collectstatic():
    '''Collect static media.'''
    require('site_path')
    require('venv_path')

    with cd(env.site_path):
        sudo(_python('manage.py collectstatic --noinput'))


def rebuild_index():
    '''Rebuild the search index.'''
    require('site_path')
    require('venv_path')
    require('process_owner')

    with cd(env.site_path):
        sudo(_python('manage.py rebuild_index'))
        sudo('chown -R {0} .xapian'.format(env.process_owner))


def update_index():
    '''Update the search index.'''
    require('site_path')
    require('venv_path')
    require('process_owner')

    with cd(env.site_path):
        sudo(_python('manage.py update_index'))
        sudo('chown -R {0} .xapian'.format(env.process_owner))


def test(args=''):
    local('./manage.py test ' + args)
   #with settings(warn_only=True):
   #    result = local('./manage.py test ' + args, capture=True)
   #    print result
   #if result.failed and not confirm('Test failed. Continue anyway?'):
   #    abort('Aborting at user request.')


# South tasks

def migrate(args=''):
    '''Run any needed migrations.'''
    require('site_path')
    require('venv_path')

    with cd(env.site_path):
        sudo(_python('manage.py migrate ' + args))


def migrate_fake(args=''):
    '''Run any needed migrations with --fake.'''
    require('site_path')
    require('venv_path')

    with cd(env.site_path):
        sudo(_python('manage.py migrate --fake ' + args))


def migrate_reset(args=''):
    '''Run any needed migrations with --fake.  No, seriously.'''
    require('site_path')
    require('venv_path')

    with cd(env.site_path):
        sudo(_python('manage.py migrate --fake --delete-ghost-migrations ' + args))


def schema_migration_auto(app=''):
    ''''''
    require('site_path')
    require('venv_path')

    with cd(env.site_path):
        sudo(_python('manage.py schemamigration {0} --auto'.format(app)))


def graph_migrations():
    '''Generate a graphviz .dot file for migrations and convert it to PNG.'''
    require('site_path')
    require('venv_path')

    with cd(env.site_path):
        run(_python('manage.py graphmigrations | dot -Tpng -omigrations.png'))
