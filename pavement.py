import behave
import json
from paver.setuputils import setup
from paver.easy import task
from paver.easy import consume_nargs
from paver.easy import sh
import threading, os, platform

setup(
    name = "behave-sample",
    version = "1.0.0",
    url="https://www.lambdatest.com/",
    author="Lambdatest",
    description=("Behave Integration with Lambdatest"),
    license="MIT",
    author_email="support@lambdatest.com",
    packages=['features'],
)

def run_behave_test(config, feature, task_id=0, tags = "all"):
    if tags == "all":
        if platform.system() == 'Windows':
            sh('SET CONFIG_FILE=config/%s.json & SET TASK_ID=%s & behave features/%s.feature' % (config, task_id, feature))
        else:
            sh('export CONFIG_FILE=config/%s.json && export TASK_ID=%s && behave features/%s.feature' % (config, task_id, feature))
    else:
        if platform.system() == 'Windows':
            sh('SET CONFIG_FILE=config/%s.json & SET TASK_ID=%s & behave --tags=%s' % (config, task_id, tags))
        else:
            sh('export CONFIG_FILE=config/%s.json && export TASK_ID=%s && behave --tags=%s' % (config, task_id, tags))
    
@task
@consume_nargs(1)
def run(args):
    """Run single and parallel test using different config."""
    fileName = args[0]
    filePath = open('config/'+ fileName +'.json')
    fileData = json.load(filePath)
    env_details = fileData['environments']
    parallelLevel = len(env_details)
    
    if parallelLevel == 1:
        run_behave_test(args[0], args[0])
    else:
        jobs = []
        for i in range(2):
            p = threading.Thread(target=run_behave_test,args=(args[0], args[0],i))
            jobs.append(p)
            p.start()

        for th in jobs:
         th.join()

@task
@consume_nargs(2)
def run_tags(args):
    """Run single and parallel test using different config."""
    fileName = args[0]
    tags = args[1]
    filePath = open('config/'+ fileName +'.json')
    fileData = json.load(filePath)
    env_details = fileData['environments']
    parallelLevel = len(env_details)

    
    if parallelLevel == 1:
        run_behave_test(args[0], args[0], 0, tags)
    else:
        jobs = []
        for i in range(2):
            p = threading.Thread(target=run_behave_test,args=(args[0], args[0], i, tags))
            jobs.append(p)
            p.start()

        for th in jobs:
         th.join()

@task
def test():
    """Run all tests"""
    entries = os.listdir('config')
    allConfigFiles = [x.split(".")[0] for x in entries ]
    excludedFiles = ['single', 'parallel', 'local']
    eligibleFiles = [x for x in allConfigFiles if x not in excludedFiles]
    for configFile in eligibleFiles:
        sh("paver run "+ configFile)
    
@task
@consume_nargs(1)
def local(args):
    """Run local feature"""
    sh("behave features/" + args[0] + ".feature")

@task
@consume_nargs(1)
def tags(args):
    """Run local tag"""
    sh("behave --tags=" + args[0])

