#!/usr/bin/env python
# https://www.matteomattei.com/how-to-execute-commands-with-specific-user-privilege-in-c-under-linux/

import sys,pwd,os

pw = pwd.getpwnam(sys.argv[1])
os.initgroups(sys.argv[1],pw.pw_gid)
env={"TERM":"xterm","USER":pw.pw_name,"HOME":pw.pw_dir,"SHELL":pw.pw_shell,"LOGNAME":pw.pw_name,"PATH":"/usr/bin:/bin:/opt/bin"};
os.setgid(pw.pw_gid);
os.setuid(pw.pw_uid);
os.execve(sys.argv[2],[],env);
