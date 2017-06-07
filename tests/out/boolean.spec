Requires:       (myPkg-backend-mariaDB if mariaDB else sqlite)
Requires:       (pkgA >= 3.2 or pkgB)
Requires:       (pkgA or (pkgB and pkgC))
Requires:       (pkgA or pkgB or pkgC)
Recommends:     (myPkg-langCZ if langsupportCZ)
Supplements:    (foo and (lang-support-cz or lang-support-all))
Conflicts:      (pkgA and pkgB)

%changelog
