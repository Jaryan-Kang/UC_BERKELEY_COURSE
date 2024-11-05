; Curry a function by progressively wrapping its parameters
(define (curry-cook formals body)
(if (null? (cdr formals))  ; If there's only one formal left
    (list 'lambda formals body)  ; Return a simple lambda
    (list 'lambda (list (car formals))  ; Otherwise, nest lambdas
          (curry-cook (cdr formals) body))))

; Apply a curried function to a list of arguments
(define (curry-consume curry args)
(if (null? args)  ; If no more arguments,
    curry  ; return the final value or function
    (if (procedure? curry)  ; If it's still a function,
        (curry-consume (curry (car args)) (cdr args))  ; apply an arg and recurse
        curry)))  ; Otherwise, return the value

; Macro to implement 'switch' as nested 'cond'
(define-macro (switch expr options)
(cons `cond  ; Start the 'cond' structure
      (map (lambda (option)  ; Map over each case
             (cons `(equal? ,expr ,(car option)) (cdr option)))  ; Compare and action
           options)))

