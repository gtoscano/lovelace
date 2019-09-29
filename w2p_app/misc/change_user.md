https://unix.stackexchange.com/questions/113754/allow-user1-to-su-user2-without-password/115090#115090

Add the following lines right below the pam_rootok.so line in your /etc/pam.d/su:
auth  [success=ignore default=1] pam_succeed_if.so user = gtoscano-test
auth  sufficient                 pam_succeed_if.so use_uid user = gtoscano


These lines perform checks using the pam_succeed_if.so module. See also the Linux-PAM configuration file syntax to learn more about the auth lines.

The first line checks whether the target user is martin-test. If it is, nothing happens (success=ignore) and we continue on the next line to check the current user. If it is not, the next line will be skipped (default=1) and we continue on subsequent lines with the usual authentication steps.
The second line checks whether the current user is martin. If it is, the system considers the authentication process as successful and returns (sufficient). If it is not, nothing happens and we continue on subsequent lines with the usual authentication steps.
You can also restrict su to a group, here the group allowedpeople can su without a password:

auth sufficient pam_succeed_if.so use_uid user ingroup allowedpeople