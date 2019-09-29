#!/usr/bin/env python
# https://gist.github.com/hartror/168a4ddf543c272cd6d8
import os
import psutil
import resource
import subprocess
import sys
import time


MEMORY_LIMIT = 256 * 1024 * 1024


def limit_process_memory(bytes):
    """
    Set the current process's virtual memory limit
    """
    log_rlimit_as("Secondary process pre-setrlimit")
    resource.setrlimit(resource.RLIMIT_AS, (bytes, bytes))
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    log_rlimit_as("Secondary process post-setrlimit")


def log_rlimit_as(message):
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    rlimit = (
        " pid {pid} soft {soft} hard {hard}"
        .format(pid=os.getpid(), soft=soft, hard=hard))
    print message, rlimit


def limit_with_fork():
    print "\nLimit with fork"
    log_rlimit_as("Primary process pre-child")
    pid = os.fork()
    if pid == 0:
        limit_process_memory(MEMORY_LIMIT)
        sys.exit(0)
    else:
        os.wait()
        log_rlimit_as("Primary process post-child")


def limit_with_subprocess():
    print "\nLimit with subprocess"
    log_rlimit_as("Primary process pre-child")
    subprocess.Popen(['./limit.py', '--limit'])
    os.wait()
    log_rlimit_as("Primary process post-child")


def limit_with_preexec_fn():
    print "\nLimit with preexec_fn"
    log_rlimit_as("Primary process preexec_pre-child")
    subprocess.Popen(
        ['touch', '/dev/null'],
        preexec_fn=limit_process_memory(MEMORY_LIMIT))
    os.wait()
    log_rlimit_as("Primary process pre_exec post-child")


def limit_with_ulimit():
    print "\nLimit with ulimit"
    log_rlimit_as("Primary process pre-child")
    command = (
        'ulimit -v {limit} && ./limit.py --print'
        .format(limit=MEMORY_LIMIT/1024))
    subprocess.Popen([command], shell=True)
    os.wait()
    log_rlimit_as("Primary process post-child")


def limit_with_psutil():
    print "\nLimit with psutil"
    log_rlimit_as("Primary process pre-child")
    proc = subprocess.Popen(['./limit.py', '--print'])
    psutil.Process(proc.pid).rlimit(
        psutil.RLIMIT_AS, (MEMORY_LIMIT, MEMORY_LIMIT))
    os.wait()
    log_rlimit_as("Primary process post-child")


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == '--limit':
            limit_process_memory(MEMORY_LIMIT)
        if sys.argv[1] == '--print':
            # Sleep so psutil has time to set our rlimit
            time.sleep(1)
            log_rlimit_as("Secondary process post-setrlimit")
    else:
        limit_with_fork()
        #limit_with_subprocess()
        #limit_with_ulimit()
        #limit_with_psutil()
        limit_with_preexec_fn()


if __name__ == "__main__":
    main()