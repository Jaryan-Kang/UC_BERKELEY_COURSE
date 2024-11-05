(define (ascending? s)
  (cond
    ((or (null? s) (null? (cdr s))) #t) ; If the list is empty or has one element, it's non-descending.
    ((>= (car (cdr s)) (car s)) (ascending? (cdr s))) ; If the second element is greater than or equal to the first, continue checking the rest.
    (else #f))) ; If the first element is greater, it's not non-descending.

(define (my-filter pred s)
    (cond ((null? s) '()) ; If list is empty, return an empty list
      ((pred (car s)) (cons (car s) (my-filter pred (cdr s)))) ; If pred is true, keep the element
      (else (my-filter pred (cdr s)))) ; Otherwise, skip the element
    )


(define (interleave lst1 lst2)
    (if (null? lst1)
    lst2 ; If lst1 is empty, return lst2
    (if (null? lst2)
        lst1 ; If lst2 is empty, return lst1
        (cons (car lst1) (interleave lst2 (cdr lst1)))))) ; Alternate elements


(define (no-repeats s)
    (define (appears? x lst)
      (cond ((null? lst) #f)
            ((= x (car lst)) #t)
            (else (appears? x (cdr lst)))))
    
    (define (unique-elements s)
      (cond ((null? s) '())
            ((appears? (car s) (cdr s)) (unique-elements (cdr s)))
            (else (cons (car s) (unique-elements (cdr s))))))
    
    (unique-elements s)
)
  
