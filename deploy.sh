#!/bin/bash
# Deploy the Donilla server.

# Parse options
usage() { echo 'Usage: ./deploy.sh [d|create-db] [t|test] [s|shell] [r|run-server]'; }
if ! [ "$1" ]; then
    usage
    exit 1
fi
while [ "$1" ]; do
    case "$1" in
        d|create-db)
            create_db=1;;
        t|test)
            _test=1;;
        s|shell)
            shell=1;;
        r|run-server)
            run=1;;
        *)
            usage
            return 0 2>/dev/null
            exit 0;;
    esac
    shift
done

# Requires python3 and python packages (as specified in requirements.txt).
if ! which python3; then
    echo 'python3 not found'
    exit 2
fi

missing_packages="$(comm -23 <(sort requirements.txt) <(pip freeze | grep -v '0.0.0' | sort))"
if [ "$missing_packages" ]; then
    echo "The following packages are missing: $missing_packages"
    exit 2
fi

if [ "$create_db" ]; then
    rm -i *.db
    python -c 'import db; db.init_db()'
fi

if [ "$_test" ]; then
    python -m unittest test
    which pycodestyle && pycodestyle --max-line-length=120 *.py
    which pylint && pylint --max-line-length=120 *.py
fi

DONILLA_DEBUG=1
FLASK_ENV=development
FLASK_APP=web
export DONILLA_DEBUG
export FLASK_ENV
export FLASK_APP

[ "$shell" ] && python -ic 'import db; import web'

[ "$run" ] && flask run --host ${DONILLA_HOST:-0.0.0.0} --port ${DONILLA_PORT:-8000}

exit 0
