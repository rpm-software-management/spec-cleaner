Requires:       ((apache2 and apache2-mod_wsgi) or (nginx and uwsgi))
Requires:       ((mariadb and python-MySQL-python) or (postgresql and python-psycopg2))
Requires:       (myPkg-backend-mariaDB if mariaDB else sqlite)
Requires:       (pkgA >= 3.2 or pkgB)
Requires:       (pkgA or (pkgB and pkgC))
Requires:       (pkgA or pkgB or pkgC)
Recommends:     (myPkg-langCZ if langsupportCZ)
Supplements:    (foo and (lang-support-cz or lang-support-all))
Conflicts:      (pkgA and pkgB)

%changelog
