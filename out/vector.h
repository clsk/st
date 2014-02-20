#define DATA_TYPE float
#define DATA_SIZE sizeof(float)

typedef struct
{
    char name;
    unsigned int len;
    double *data;
} Vector;

Vector from_input();
Vector add_vectors(double * a, double *  b, unsigned int len);
void print_vector(Vector *vector);
