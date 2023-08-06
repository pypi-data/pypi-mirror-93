from invoke import task
from invoke.tasks import call

from invoke import run

@task
def clean(c, source='Unknown'):
    print(f'cleaning requested from: {source}')

@task
def tweet(c):
    print('tweeting')

@task(
    pre=[call(clean, source='build_bot')],
    post=[tweet])
def build(c, notification=False):
    print('building')

    if notification:
        print('notifying administrator')

@task
def git_clone(c, repo_url):
    c.('mkdir test_directory')
    with c.cd('test_directory'):
        # # c.run('mkdir bbb')
        # with c.cd('bbb'):
        c.run('git init')
        c.run('git clone https://github.com/steinwurf/lms')
        c.run('git init')
        # c.run('del /F /Q my.txt')

    # res = run('mkdir aaa')
    # res = res('cd aaa')
    # res('mkdir bbb')