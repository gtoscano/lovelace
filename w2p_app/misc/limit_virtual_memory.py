#!/usr/bin/env python3
#https://gist.github.com/s3rvac/f97d6cbdfdb15c0a32e7e941f7f4a3fa

# check the resource page
# https://docs.python.org/2/library/resource.html
#
# Limits the maximal virtual memory for a subprocess in Python.
#
# Linux only.
#
# https://thraxil.org/users/anders/posts/2008/03/13/Subprocess-Hanging-PIPE-is-your-enemy/
# should we use?
# subprocess.Popen (cmd, shell=True, stdout=file_hndl, stderr=file_hndl)

#ostia, good place https://pymotw.com/2/subprocess/

#python resource limits
#https://stackoverflow.com/questions/37519632/python-resource-limits

import subprocess
import resource

# Maximal virtual memory for subprocesses (in bytes).
#MAX_VIRTUAL_MEMORY = 10 * 1024 * 1024 # 10 MB
MAX_VIRTUAL_MEMORY = 1*1024  # 10 MB

def limit_virtual_memory():
    # The tuple below is of the form (soft limit, hard limit). Limit only
    # the soft part so that the limit can be increased later (setting also
    # the hard limit would prevent that).
    # When the limit cannot be changed, setrlimit() raises ValueError.
    resource.setrlimit(resource.RLIMIT_AS, (MAX_VIRTUAL_MEMORY, MAX_VIRTUAL_MEMORY))

p = subprocess.Popen(
    ['./a.out'],
    # preexec_fn is a callable object that will be called in the child process
    # just before the child is executed.
    preexec_fn=limit_virtual_memory
)
p.communicate()
print (p.returncode)
