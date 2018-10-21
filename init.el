;; Clojure dependencies
(defvar my-packages '(better-defaults
                      projectile
                      clojure-mode
                      cider))

(dolist (p my-packages)
  (unless (package-installed-p p)
    (package-install p)))
