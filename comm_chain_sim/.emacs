(custom-set-variables
  ;; custom-set-variables was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
 '(column-number-mode t)
 '(display-time-mode t)
 '(scroll-bar-mode (quote right))
 '(show-paren-mode t)
 '(text-mode-hook (quote (turn-on-auto-fill text-mode-hook-identify)))
 '(tool-bar-mode nil)
 '(transient-mark-mode t))
  '(tooltip-mode nil)
(custom-set-faces
  ;; custom-set-faces was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
 )

;; remove annoying splash screen
(setq inhibit-splash-screen t)

;; Don't make me type out 'yes' and 'no'
(fset 'yes-or-no-p 'y-or-n-p)

;; goto line
(global-set-key "\M-g" 'goto-line)

;; set org mode
(add-to-list 'auto-mode-alist '("\\.org\\'" . org-mode))

;; auctex mode
(load "auctex.el" nil t t)

;; disable M-TAB
(put 'lisp-complete-symbol 'disabled t)

;; turn on auctex autofill
(add-hook 'LaTeX-mode-hook 'turn-on-auto-fill)

;;  Start GNUServe process when starting up.  This lets us send new files
;; to previously spawned emacs process.
(load "gnuserv-compat")
(load-library "gnuserv")
(gnuserv-start)

