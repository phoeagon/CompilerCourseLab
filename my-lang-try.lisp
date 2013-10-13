;;basic types
(defvar *basic-types* '(void int float char))

;;simple function call syntax, just a try ^_^
(defmacro $[ (funname &rest args)
  (let ((arg-list (delete '] args)))
    `(,funname ,@arg-list)))


;;macro used to define hirachy of exp
(defmacro def-exp-parser (funname operators next-parser)
  `(defun ,funname (stat)
     ,(append '(cond)
	    (loop for sym in operators collect
		 (list (list 'find sym 'stat) 
		       (list 'let `((pos (position ,sym stat)))
			     (list 'list sym 
				   (list next-parser '(subseq stat 0 pos))
				   (list funname '(subseq stat (1+ pos)))))))
	    `((t (,next-parser stat))))))

;;postfix exp (funcall and array access)
(defun trans-postfix-exp (stat)
  (cond ((eql 1 (length stat)) (car stat))
	((eql '$[ (car stat)) (trans-funcall stat))
	((eql '[ (cadr stat)) 
	 (list 'aref (car stat)
	       (trans-exp (delete '] (delete '[ (cdr stat))))))))

;;factor exp (* and /)
(defun trans-factor-exp (stat)
  (cond ((find '* stat) (let ((pos (position '* stat)))
			  (list '* 
				(trans-postfix-exp (subseq stat 0 pos))
				(trans-factor-exp (subseq stat (1+ pos))))))
	((find '/ stat) (let ((pos (position '/ stat)))
			  (list '/
				(trans-postfix-exp (subseq stat 0 pos))
				(trans-factor-exp (subseq stat (1+ pos))))))
	(t (trans-postfix-exp stat))))


;;translate expression
(defun trans-sum-exp (stat)
  (cond ((find '+ stat) (let ((pos (position '+ stat)))
			  (list '+ 
				(trans-factor-exp (subseq stat 0 pos))
				(trans-exp (subseq stat (1+ pos))))))
	((find '- stat) (let ((pos (position '- stat)))
			  (list '-
				(trans-factor-exp (subseq stat 0 pos))
				(trans-exp (subseq stat (1+ pos))))))
	(t (trans-factor-exp stat))))

;; compare func
(def-exp-parser trans-comp-exp ('> '< '>= '<=) trans-sum-exp)

;; logical func
(def-exp-parser trans-logical-exp ('and 'or) trans-comp-exp)

;; the trans exp func
(defun trans-exp (stat)
  (trans-logical-exp stat))

;; helper
(defun trans-defun-helper1 (stat)
  (cond ((eql '] (car stat)) (cdr stat))
	(t (trans-defun-helper1 (cdr stat)))))

(defun trans-defun-helper2 (stat)
  (cond ((eql '] (car stat)) nil)
	(t (cons (car stat) (trans-defun-helper2 (cdr stat))))))

;;translate function define
(defun trans-defun (stat)
  (cond ((eql '$[ (car stat)) 
	 (append (list 'defun (cadr stat) (trans-defun-helper2 (cddr stat)))
		 (map 'list #'trans-eval (trans-defun-helper1 stat))))))

;;translate declaration
(defun trans-decl (stat)
  (let ((decl (cdr stat)))
    (cond ((eql '$[ (car decl)) (trans-defun decl))
	  ((eql 1 (length decl)) (list 'defparameter (car decl) '()))
	  ((eql '[ (cadr decl)) 
	   (list 'defparameter (car decl) 
		 (list 'make-array (cons 'list 
					 (delete '[ 
						 (delete '] (cdr decl))))))))))

;;translate funcall 
(defun trans-funcall (stat)
  (delete '] (delete '$[ stat)))

;;translate assignment
(defun trans-assignment (stat)
  (list 'setf 
	(trans-exp (subseq stat 0 (position '<-- stat))) 
	(trans-exp (subseq stat (1+ (position '<-- stat))))))

;; translate if 
(defun trans-if (stat)
  (let ((tmp-list (list 'if 
			(trans-exp (car (subseq stat 1 2)))
			(append '(progn) 
				(map 'list 
				     #'trans-eval 
				     (subseq stat 
					     (1+ (position '{ stat)) 
					     (position '} stat)))))))
    (cond ((find 'else stat) 
	   (let ((else-stat (subseq stat (position 'else stat))))
	     (append tmp-list (list (append '(progn) 
					    (map 'list 
						 #'trans-eval 
						 (subseq else-stat 
							 (1+ (position '{ else-stat)) 
							 (position '} else-stat))))))))
	  (t tmp-list))))

;;translate while loop
(defun trans-while-loop (stat)
  (append (list 'do '() (list (list 'not (trans-eval (cadr stat))) '()))
	  (map 'list #'trans-eval (subseq stat 2))))
					 

;;eval single stat
(defun trans-eval (stat)
  (cond ((find (car stat) *basic-types*) (trans-decl stat))
	((eql '$[ (car stat)) (trans-funcall stat))
	((find '<-- stat) (trans-assignment stat))
	((eql 'for (car stat)) (trans-for-loop stat))
	((eql 'while (car stat)) (trans-while-loop stat))
	((eql 'if (car stat)) (trans-if stat))
	(t (trans-exp stat))))
	

;;eval macro
(defmacro mylang-eval (&body args)
  (let ((a-list (map 'list #'trans-eval args)))
    `(progn
       ,@a-list)))

;;sample quick sort program
(defparameter *qsort-prog* 
  '(int $[ qsort a l r i j ]
    (int pivot)
    (pivot <-- a [ l ])
    (i <-- l)
    (j <-- r)
    (while (i < j) 
      (while ( a [ j ] >= pivot and i < j)
	(j <-- j - 1))
      (while ( a [ i ] < pivot and i < j)
	(i <-- i + 1))
      (if (i < j) {
	  (int tmp)
	  (tmp <-- a [ i ])
	  (a [ i ] <-- a [ j ])
	  (a [ j ] <-- tmp)
	  })
      
      (if (l < j) {
	  ($[ qsort a l (1- j) 0 0 ]) })
      (if (i < r) {
	  ($[ qsort a (1+ i) r 0 0 ]) }))))