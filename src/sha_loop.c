#include <math.h>
#include <stdio.h>
#include <stdbool.h>
#include <openssl/sha.h>

void sha256_loop(unsigned char * buffer, int n_values, unsigned char * out)
{
    int i;
    // i moves from bytes to bytes, input of size lambda is on 16 bytes and 256 = 32 bytes
    for(i=0;i<n_values;i++){
        SHA256(buffer+(16*i), 16, out+(32*i));
    }
}

void sha512_loop(unsigned char * buffer, int n_values, unsigned char * out)
{
    int i;
    // i moves from bytes to bytes, input of size lambda is on 16 bytes and 512 = 64 bytes
    for(i=0;i<n_values;i++){
        SHA512(buffer+(16*i), 16, out+(64*i));
    }
}