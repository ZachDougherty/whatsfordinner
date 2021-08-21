# !/usr/local/bin/zsh zsh

# https://dev.to/meleu/how-to-join-array-elements-in-a-bash-script-303a
joinByChar() {
  local IFS="_"
  echo "$*"
}

export fname=$(joinByChar logfile $(date))
pg_ctl start -l logs/$fname -D /usr/local/var/postgres
