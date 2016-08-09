#!/bin/sh

if [ $# = 2 ]; then

	chown www-data:www-data ./ -R
	chmod g+w logs/core.log

	/etc/init.d/apache2 restart

	mysql --user=$1 --password=$2 < install.sql

	./manage.py syncdb
else
	echo "Use Parameters DBUser, DBPassword"
fi
