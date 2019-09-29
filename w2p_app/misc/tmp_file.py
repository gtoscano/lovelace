import tempfile
import os, stat
import shutil

dirpath = tempfile.mkdtemp()
# ... do stuff with dirpath
# Write files in that directory
filename = os.path.join(dirpath,'step1.txt')

os.chmod(dirpath, 0o774)
print dirpath
print filename
#shutil.rmtree(dirpath)