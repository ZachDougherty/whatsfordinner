migrate-up:
	psql -d postgres -c "SELECT 1 FROM pg_database WHERE datname = 'whatsfordinner'" | grep -q 1 || psql -d postgres -c "CREATE DATABASE whatsfordinner"
	psql -d whatsfordinner -f ./database/migrations/1_up.sql
	echo "Migration successful."

migrate-down:
	psql -d whatsfordinner -f ./database/migrations/1_down.sql
	echo "Migration unsuccessful."

startdb:
	./scripts/startdb.sh

stopdb:
	pg_ctl stop -D /usr/local/var/postgres

serve:
	flask run
