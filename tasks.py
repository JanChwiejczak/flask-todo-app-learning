from invoke import task, run

@task
def test_local():
    run("python -m py.test tests")

@task
def commit():
    message = input("Enter a git commit message:")
    run("git add .")
    run('git commit -am "{}"'.format(message))

@task
def push():
    run("git push origin master")

@task
def prepare():
    test_local()
    commit()
    push()
