#!/usr/bin/env python
import os
import sys
from lockfile import FileLock, LockTimeout
from datetime import datetime
import traceback
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "estate.settings")

    LOCK =  "_".join(sys.argv[1:2])
    print "time of working %s" % (datetime.now())
    lock = FileLock(LOCK)
    lock.acquire(timeout=3)    # wait up to 60 seconds

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise

    try:
      execute_from_command_line(sys.argv)
    except:
      traceback.print_exc()
    finally:  
      print "release locked"
      print lock.path
      lock.release()

