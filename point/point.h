#ifndef POINT
#define POINT

#define export __attribute__((visibility("default")))

typedef struct Point {
    float x;
    float y;
    float vx;
    float vy;
    int _error;
} Point;

export void Point_rotate(Point *p, Point *center, float angle);
export void Point_update(Point *p);
export void Point_create(Point *p);
export void Point_destroy(Point *p);
export int Point__error(Point *p);
export void Point_throw(Point *p, int code);
#endif