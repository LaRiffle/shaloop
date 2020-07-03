#include <math.h>
#include <stdio.h>
#include <stdbool.h>
#include <openssl/sha.h>
#include <pthread.h>

void sha256_loop(unsigned char * buffer, int n_values, unsigned char * out)
{
    int i;
    // i moves from bytes to bytes, input of size lambda is on 16 bytes and 256 = 32 bytes
    for(i=0;i<n_values;i++){
        SHA256(buffer+(16*i), 16, out+(32*i));
    }
}

// Arguments for a thread are given as a struct
struct loop_args
{
    unsigned char * buffer;
    int n_values; 
    int thread_id;
    int n_threads;
    unsigned char * out;
};


void* sha256_loop_onethread(void *args)
{
    // Each thread works on a different part of the array
    struct loop_args *arg = args;
    int i;
    // i moves from bytes to bytes, input of size lambda is on 16 bytes and 256 = 32 bytes
    // modulo n_thread
    for(i=arg->thread_id;i<arg->n_values;i+=arg->n_threads){
        SHA256((arg->buffer)+(16*i), 16, (arg->out)+(32*i));
    }

    // p_thread expects a pointer but will not use it
    return NULL;
}

void sha256_loop_parallel(unsigned char * buffer, int n_values, unsigned char * out, int n_threads)
{
    pthread_t threads[n_threads];
    struct loop_args args[n_threads];

    int thread_id;

    for(thread_id=0; thread_id<n_threads;thread_id++){

        args[thread_id].buffer = buffer;
        args[thread_id].n_values = n_values;
        args[thread_id].thread_id = thread_id;
        args[thread_id].n_threads = n_threads;
        args[thread_id].out = out;

        pthread_create(&threads[thread_id], NULL, &sha256_loop_onethread, (void *)&args[thread_id]);
    }

    // Wait for all the threads
    for(thread_id=0; thread_id<n_threads;thread_id++){
        pthread_join(threads[thread_id], NULL);
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