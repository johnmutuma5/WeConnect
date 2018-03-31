[![Build Status](https://travis-ci.org/johnmutuma5/WeConnect.svg?branch=master)](https://travis-ci.org/johnmutuma5/WeConnect)
[![Maintainability](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability)](https://codeclimate.com/github/codeclimate/codeclimate/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/johnmutuma5/WeConnect/badge.svg?branch=master)](https://coveralls.io/github/johnmutuma5/WeConnect?branch=master)


WeConnect provides a platform that brings businesses and individuals together.
This platform creates awareness for businesses and gives the users the ability to write reviews about the businesses they have interacted with.

More guidelines as the project proceeds.



HOW TO:

    Set up environmnet:
      Inside project folder:
        * Auto for (Unix):
          - run 'source ./Configure'

        * Manual:
          - run 'make venv' to install virtualenv
          - run 'source ./venv/bin/activate'
          - run 'make install' to install dependencies

        Database tables:

          * Create
            - run 'python tables.py create'  or
            - run 'make tables'
          * Drop
            - run 'python tables.py drop'  or
            - run 'make drop_all'

        Run:
          * run 'python run.py'   or
          * run 'make run'

        Test:
          * run 'py.test -vv' or
          * run 'nosetests --exe -v --with-coverage --cover-package=app'  or
          * run 'make test'
