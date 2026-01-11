#include <stdlib.h>
#include <unistd.h>

int main() {
    setuid(0);
    system("echo Checking system...");
    return 0;
}