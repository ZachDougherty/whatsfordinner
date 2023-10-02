# !/usr/local/bin/zsh zsh

# create the log directory if it doesn't already exist
if [ ! -d "./logs" ]; then
  mkdir logs
  echo "Created ./logs directory."
fi

# https://dev.to/meleu/how-to-join-array-elements-in-a-bash-script-303a
joinByChar() {
  local IFS="_"
  echo "$*"
}

export fname=$(joinByChar logfile $(date))

# check if database name supplied
if [ "$#" -ge 1 ]; then
  export db=$1
else
  export db=/usr/local/var/postgres  # default db location
fi

pg_ctl start -l logs/$fname -D $db

# hostname:port:database:username:password
if [ "$#" -eq 2 ]; then
  if [ ! -f "~/.pgpass" ]; then
    touch ~/.pgpass
    chmod 0600 ~/.pgpass
    echo $2 > ~/.pgpass
    echo "Created ~/.pgpass"
  fi
fi
