#!/usr/bin/env bash

set -x

if [[ $EUID == 0 ]]; then
  # changes path setup for all users, puts homebrew first
  sed -e '/^\/usr\/local/d' -i .orig /etc/paths
  echo -e "/usr/local/bin\n/usr/local/sbin\n/usr/local/opt/coreutils/libexec/gnubin\n$(cat /etc/paths)" > /etc/paths

  # restarts to install brew as non-root user
  exec su ${1} -c "$(which bash) ${0}"
fi

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew=/usr/local/bin/brew
if [ ! -x ${brew} ]; then
    brew=/opt/homebrew/bin/brew
fi

${brew} install curl git coreutils highlight neovim tmux htop python@3 pygments gitlab-runner
${brew} services list #forces the installation of "services" support
${brew} install --cask mactex
