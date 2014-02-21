#define DATA_TYPE double
#define DATA_SIZE sizeof(DATA_TYPE)

typedef struct
{
    unsigned int len;
    double *data;
} Vector;

void vector_output(Vector* a);
void vector_init(Vector* a);
void vector_alloc(Vector* a);
void vector_realloc(Vector* a, unsigned int len);
void vector_free(Vector* a);
Vector input_vector(Vector* a);
Vector vector_C(Vector* a);
Vector vector_S(Vector* a);
Vector vector_P(Vector* a, Vector* b);
Vector vector_E(Vector* a, Vector* b);
Vector vector_I(Vector* a);

