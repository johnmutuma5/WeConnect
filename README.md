[![Codacy Badge](https://api.codacy.com/project/badge/Grade/04753a5f13644b7dbd6078b82e58edbb)](https://app.codacy.com/app/johnmutuma5/WeConnect?utm_source=github.com&utm_medium=referral&utm_content=johnmutuma5/WeConnect&utm_campaign=badger)
[![Build Status](https://travis-ci.org/johnmutuma5/WeConnect.svg?branch=master)](https://travis-ci.org/johnmutuma5/WeConnect)
[![Coverage Status](https://coveralls.io/repos/github/johnmutuma5/WeConnect/badge.svg)](https://coveralls.io/github/johnmutuma5/WeConnect)
[![codecov](https://codecov.io/gh/johnmutuma5/WeConnect/branch/master/graph/badge.svg)](https://codecov.io/gh/johnmutuma5/WeConnect)
[![Maintainability](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability)](https://codeclimate.com/github/codeclimate/codeclimate/maintainability)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/10f06df2cff940048241583bc272615f)](https://www.codacy.com/app/johnmutuma5/WeConnect?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=johnmutuma5/WeConnect&amp;utm_campaign=Badge_Grade)





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
