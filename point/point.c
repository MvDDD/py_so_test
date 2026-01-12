#include <math.h>
#include "point.h"  // your header defining struct Point

// Rotate a point p around another point "center" by angle radians
void Point_rotate(Point* p, Point* center, float angle) {
    if (!p || !center) return; // safety check

    float s = sinf(angle);
    float c = cosf(angle);

    // translate point to origin
    float x = p->x - center->x;
    float y = p->y - center->y;

    // rotate
    float xnew = x * c - y * s;
    float ynew = x * s + y * c;

    // translate back
    p->x = xnew + center->x;
    p->y = ynew + center->y;
}

// Update point by velocity
void Point_update(Point* p) {
    if (!p) return;
    p->x += p->vx;
    p->y += p->vy;
}

void Point_create(Point *p) {}
void Point_destroy(Point *p) {}
void Point_throw(Point *p, int code){p->_error = code;}
int Point__error(Point *p){return p->_error;}