#ifndef DATA_STRUCTURES_H
#define DATA_STRUCTURES_H

// Stack structure
typedef struct {
    int *items;
    int top;
    int capacity;
} Stack;

// Node for linked list
typedef struct Node {
    int data;
    struct Node* next;
} Node;

// Queue structure
typedef struct {
    Node* front;
    Node* rear;
} Queue;

/**
 * Creates a new stack with given capacity
 * @param capacity Maximum number of elements
 * @return Pointer to new stack, or NULL on failure
 */
Stack* create_stack(int capacity);

/**
 * Pushes an element onto the stack
 * @param stack Stack pointer
 * @param item Item to push
 * @return 0 on success, -1 on failure
 */
int push(Stack* stack, int item);

/**
 * Pops an element from the stack
 * @param stack Stack pointer
 * @return Popped element, or -1 if stack is empty
 */
int pop(Stack* stack);

/**
 * Returns top element without removing it
 * @param stack Stack pointer
 * @return Top element, or -1 if stack is empty
 */
int peek(Stack* stack);

/**
 * Checks if stack is empty
 * @param stack Stack pointer
 * @return 1 if empty, 0 otherwise
 */
int is_empty(Stack* stack);

/**
 * Checks if stack is full
 * @param stack Stack pointer
 * @return 1 if full, 0 otherwise
 */
int is_full(Stack* stack);

/**
 * Destroys the stack and frees memory
 * @param stack Stack pointer
 */
void destroy_stack(Stack* stack);

/**
 * Creates a new queue
 * @return Pointer to new queue, or NULL on failure
 */
Queue* create_queue(void);

/**
 * Enqueues an element
 * @param queue Queue pointer
 * @param data Data to enqueue
 * @return 0 on success, -1 on failure
 */
int enqueue(Queue* queue, int data);

/**
 * Dequeues an element
 * @param queue Queue pointer
 * @return Dequeued element, or -1 if queue is empty
 */
int dequeue(Queue* queue);

/**
 * Destroys the queue and frees memory
 * @param queue Queue pointer
 */
void destroy_queue(Queue* queue);

#endif // DATA_STRUCTURES_H

