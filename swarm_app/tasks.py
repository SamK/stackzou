from invoke import task


@task(name="env")
def set_env(c, env):
    c.env = env
