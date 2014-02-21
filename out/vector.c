#include "vector.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void vector_output(Vector* a)
{
    printf("[ ");
    for (int i = 0; i < a->len; i++)
        printf("%f ", a->data[i]);
    printf("]\n");
}

void vector_init(Vector* a)
{
    a->len = 0;
    a->data = NULL;
}

void vector_alloc(Vector* a)
{
    a->data = malloc(DATA_SIZE*a->len);
    if(a->data == NULL) {
        printf("Runtime Error: Cannot Allocate System Memory!\n");
        exit(0);
    }

}

void vector_realloc(Vector* a, unsigned int len)
{
    if (len > a->len) {
        a->data = realloc(a->data, DATA_SIZE*len);

        if(a->data == NULL) {
            printf("Runtime Error: Cannot Allocate System Memory!\n");
            exit(0);
        }
    }
    a->len = len;
}

void vector_free(Vector *a)
{
    free(a->data);
    a->data = NULL;
}

Vector vector_input()
{
    char input[512];
    Vector r;
    vector_init(&r);
    if (fgets(input, 512, stdin) == NULL) {
        printf("Runtime Error: Bogus input!\n");
        return r;
    }

    DATA_TYPE fs[256];
    unsigned int len = 0, i = 0;
    char* c = strtok(input, " ");
    for (; c != NULL; i++) {
        fs[i] = atof(c);
        printf("%f ", fs[i]);
        c = strtok(NULL, " ");
    }

    printf("%d", i);
    r.len = i;
    vector_alloc(&r);
    memcpy(r.data, fs, DATA_SIZE*r.len);

    return r;
}


Vector vector_C(Vector* a)
{
    Vector r;
    r.len = 1;
    vector_alloc(&r);
    r.data[0] = a->len;
    return r;
}

Vector vector_S(Vector* a)
{
    Vector r;
    r.len = 1;
    vector_alloc(&r);
    r.data[0] = 0;
    for (int i = 0; i < a->len; i++) {
        r.data[0] += a->data[i];
    }

    return r;
}

Vector vector_P(Vector* a, Vector* b)
{
    Vector r;
    r.len = a->len;
    vector_alloc(&r);
    for (int i = 0; i < r.len; i++) {
        r.data[i] = a->data[i] * b->data[i];
    }

    return r;
}

Vector vector_E(Vector* a, Vector* b)
{
    Vector r;
    r.len = a->len;
    vector_alloc(&r);
    for (int i = 0; i < r.len; i++) {
        r.data[i] = a->data[i] * b->data[0];
    }

    return r;
}

Vector vector_I(Vector* a)
{
    Vector r;
    r.len = a->len;
    vector_alloc(&r);
    for (int i = 0; i < r.len; i++) {
        r.data[i] = -(a->data[i]);
    }

    return r;
}
