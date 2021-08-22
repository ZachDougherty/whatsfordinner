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

if [ "$#" -eq 1 ]; then
  export db=$1
else
  export db=/usr/local/var/postgres
fi

pg_ctl start -l logs/$fname -D $db
