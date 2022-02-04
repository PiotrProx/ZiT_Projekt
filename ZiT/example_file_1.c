#include <stdio.h>
#include <unistd.h>
#include <sys/utsname.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
int main() {
    struct utsname buffer;
    struct stat st = {0};
    for (int i=0; i<5; i++)
    {
        printf("Hello, World!\n");       
        sleep(1);
        errno = 0;
         if (uname(&buffer) < 0) {
             perror("uname");
             exit(EXIT_FAILURE);
        }
        
        printf("system name = %s\n", buffer.sysname);
        printf("node name   = %s\n", buffer.nodename);
        printf("release     = %s\n", buffer.release);
        printf("version     = %s\n", buffer.version);
        printf("machine     = %s\n", buffer.machine);
        }
   int result = mkdir("NewFolder", 0777);
   return 0;
}
