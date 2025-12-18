#include "data_structures.h"
#include <stdlib.h>

Stack* create_stack(int capacity) {
    Stack* stack = (Stack*)malloc(sizeof(Stack));
    if (stack == NULL) {
        return NULL;
    }
    stack->items = (int*)malloc(capacity * sizeof(int));
    if (stack->items == NULL) {
        free(stack);
        return NULL;
    }
    stack->top = -1;
    stack->capacity = capacity;
    return stack;
}

int push(Stack* stack, int item) {
    if (stack == NULL || is_full(stack)) {
        return -1;
    }
    stack->items[++stack->top] = item;
    return 0;
}

int pop(Stack* stack) {
    if (stack == NULL || is_empty(stack)) {
        return -1;
    }
    return stack->items[stack->top--];
}

int peek(Stack* stack) {
    if (stack == NULL || is_empty(stack)) {
        return -1;
    }
    return stack->items[stack->top];
}

int is_empty(Stack* stack) {
    if (stack == NULL) {
        return 1;
    }
    return stack->top == -1;
}

int is_full(Stack* stack) {
    if (stack == NULL) {
        return 0;
    }
    return stack->top == stack->capacity - 1;
}

void destroy_stack(Stack* stack) {
    if (stack != NULL) {
        free(stack->items);
        free(stack);
    }
}

Queue* create_queue(void) {
    Queue* queue = (Queue*)malloc(sizeof(Queue));
    if (queue == NULL) {
        return NULL;
    }
    queue->front = NULL;
    queue->rear = NULL;
    return queue;
}

int enqueue(Queue* queue, int data) {
    if (queue == NULL) {
        return -1;
    }
    Node* new_node = (Node*)malloc(sizeof(Node));
    if (new_node == NULL) {
        return -1;
    }
    new_node->data = data;
    new_node->next = NULL;
    
    if (queue->rear == NULL) {
        queue->front = queue->rear = new_node;
    } else {
        queue->rear->next = new_node;
        queue->rear = new_node;
    }
    return 0;
}

int dequeue(Queue* queue) {
    if (queue == NULL || queue->front == NULL) {
        return -1;
    }
    Node* temp = queue->front;
    int data = temp->data;
    queue->front = queue->front->next;
    
    if (queue->front == NULL) {
        queue->rear = NULL;
    }
    free(temp);
    return data;
}

void destroy_queue(Queue* queue) {
    if (queue != NULL) {
        while (queue->front != NULL) {
            Node* temp = queue->front;
            queue->front = queue->front->next;
            free(temp);
        }
        free(queue);
    }
}

