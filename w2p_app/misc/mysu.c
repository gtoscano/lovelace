// https://www.matteomattei.com/how-to-execute-commands-with-specific-user-privilege-in-c-under-linux/
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <pwd.h>

int main(int argc, char* argv[])
{
    if(argc != 3)
    {
        printf("Usage: %s [USERNAME] [COMMAND]\n",argv[0]);
        return 1;
    }
    char *env[16];
    char envc[16][64];
    struct passwd *pw = getpwnam(argv[1]);
    if(pw==NULL)
    {
        printf("User %s does not exists!\n",argv[1]);
        return 1;
    }

    sprintf(env[0]=envc[0],"TERM=xterm");
    sprintf(env[1]=envc[1],"USER=%s",pw->pw_name);
    sprintf(env[2]=envc[2],"HOME=%s",pw->pw_dir);
    sprintf(env[3]=envc[3],"SHELL=%s",pw->pw_shell);
    sprintf(env[4]=envc[4],"LOGNAME=%s",pw->pw_name);
    sprintf(env[5]=envc[5],"PATH=/usr/bin:/bin:/opt/bin");
    env[6]=0;

    initgroups(argv[1],pw->pw_gid);
    setgid(pw->pw_gid);
    setuid(pw->pw_uid);
    execve(argv[2],NULL,env);

    return 0;
}