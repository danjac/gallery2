import os
import sys
import time
import schedule

from pyramid.paster import bootstrap

env = None


def sample_job():
    print("Working...")


schedule.every(10).minutes.do(sample_job)

    
def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    global env

    if len(argv) != 2:
        usage(argv)

    config_uri = argv[1]
    env = bootstrap(config_uri)
    while True:
        # in production, probably better to run this 
        # using e.g. supervisord or monit
        schedule.run_pending()
        time.sleep(1)
