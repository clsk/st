#include "vector.h"

#include <stdlib.h>
#include <stdio.h>

Vector add_vectors(double * a, double * b, unsigned int len)
{
    Vector result;
    result.len = len;
    result.data = malloc(sizeof(double)*len);
    for (int i = 0; i < len; i++)
        result.data[i] = a[i] + b[i];

    return result;
}

void print_vector(Vector * v)
{
    printf("%c [ ", v->name);
    for (int i = 0; i < v->len; i++)
        printf("%f ", v->data[i]);
    printf("]\n");
}

void input_vector(Vector * vector)
{
}


void vector_init(Vector* v, char name) {
    v->name = name;
    v->len = 0;
    v->data = NULL;
}

void vector_alloc(Vector * v) {
    v->data = malloc(DATA_SIZE*v->len);
    if(v->data == NULL) {
        printf("Runtime Error: Cannot Allocate System Memory!\n");
        exit(0);
    }

}

void vector_realloc(Vector * v, unsigned int len)
{
    if (len > v->len) {
        v->data = realloc(v->data, DATA_SIZE*len);

        if(v->data == NULL) {
            printf("Runtime Error: Cannot Allocate System Memory!\n");
            exit(0);
        }
    }
    v->len = len;
}

void vector_free(Vector *v)
{
    free(v->data);
    v->data = NULL;
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
        r.data[i] += a->data[i] * b->data[i];
    }

    return r;
}

Vector vector_E(Vector* a, Vector* b)
{
    Vector r;
    r.len = a->len;
    vector_alloc(&r);
    for (int i = 0; i < r.len; i++) {
        r.data[i] += a->data[i] * b->data[0];
    }

    return r;
}

Vector vector_I(Vector* a)
{
    Vector r;
    r.len = a->len;
    vector_alloc(&r);
    for (int i = 0; i < r.len; i++) {
        r.data[i] += -(a->data[i]);
    }

    return r;
}
