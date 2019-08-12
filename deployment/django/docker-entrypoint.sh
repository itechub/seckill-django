#! /bin/sh

set -e

until nc -z -v -w30 $SECKILL_DB_HOST 3306
do
  echo "Waiting for database mysql connection..."
  sleep 1
done >&2

echo "Mysql is up - continuing"

# Make db migrations when switch turn on
if [ "x$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then
    /env/bin/python manage.py migrate --noinput
fi

# Collect static files when switch turn on
if [ "x$DJANGO_MANAGEPY_COLLECTSTATIC" = 'xon' ]; then
    /env/bin/python manage.py collectstatic --noinput
fi

# Create super user
if [ $SECKILL_ADMIN_PASS ]; then
echo "Processing admin creation, username: $SECKILL_ADMIN_NAME ( $SECKILL_ADMIN_EMAIL )"
echo "\
from django.contrib.auth import get_user_model; \
User = get_user_model(); \
exit(0) \
if User.objects.filter(username='$SECKILL_ADMIN_NAME').exists() \
else \
User.objects.create_superuser(username='$SECKILL_ADMIN_NAME', email='$SECKILL_ADMIN_EMAIL',password='$SECKILL_ADMIN_PASS') \
" | python manage.py shell >&2
fi

exec "$@"
