#include <stdio.h>

int main(int argc, char * argv[]) {
   int i, sum = 0;
 
   if (argc != 3) {
      printf("You have to provide two integer numbers.\n");
      return (1);
   }
 
   for (i = 1; i < argc; i++)
      sum = sum + atoi(argv[i]);
 
   //printf("%d\n", sum);
   printf("%d+%d=%d\n", atoi(argv[1]),atoi(argv[2]),sum);

   return (0);
 
}
