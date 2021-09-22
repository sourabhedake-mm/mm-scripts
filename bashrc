# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
	# We have color support; assume it's compliant with Ecma-48
	# (ISO/IEC-6429). (Lack of such support is extremely rare, and such
	# a case would tend to support setf rather than setaf.)
	color_prompt=yes
    else
	color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
PS1=
#    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
PS1=
#    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# colored GCC warnings and errors
export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'

# some more ls aliases
alias ll='ls -alrt'
alias la='ls -A'
alias l='ls -CF'
alias vi='vim'
alias 'cd..'='cd ..'

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

alias apt="sudo apt"
alias apti="sudo apt -y install"

# C8 Alias
alias ccdb="cd ~/sandbox/c8db"
alias ccop="cd ~/sandbox/c8operator/configs"
alias ccdep="cd ~/sandbox/deployer-ci"
alias ccui="cd ~/sandbox/c8gui"
alias ccapi="cd ~/sandbox/c8apiserver"
alias cccom="cd ~/sandbox/c8compute"
alias ccauto="cd ~/sandbox/c8automation"
alias ccbill="cd ~/sandbox/c8billing"
alias cchealth="cd ~/sandbox/c8health"

alias teledb="while true ; do clear; echo \"Connecting to DB Telepresence=================\"; telepresence --namespace c8 --deployment c8db-coord --run-shell --expose 8529; echo \"Retrying in 5 seconds... Press CTRL+C to exit\"; sleep 5; done;"
alias teleapi="while true ; do clear; echo \"Connecting to API Server Telepresence========\"; telepresence --swap-deployment c8apiserver --expose 8081 --run-shell --namespace c8; echo \"Retrying in 5 seconds... Press CTRL+C to exit\"; sleep 5; done;"
#alias telebill="while true ; do clear; echo \"Connecting to Billing Telepresence========\"; telepresence --swap-deployment c8billing --expose 4183 --run-shell --namespace c8; echo \"Retrying in 5 seconds... Press CTRL+C to exit\"; sleep 5; done;"
#alias c8apid="ccapi; ./bin/c8apid -c config/c8apid.json"

export C8SWAGGER_FULL_FILE_PATH=/home/cortex/sandbox/c8db/js/actions/_admin/api/c8-swagger.json
#export BUILD_DIR=/home/cortex/sandbox/c8apiserver/build/
#export BOOST_ROOT=/home/cortex/.boost/
export DEFAULT_PLANS_DIR=/home/cortex/sandbox/c8db/js/plans

# Asus Alias
# alias rgb="sudo rogauracore initialize_keyboard; sudo rogauracore"
# alias rgboff="sudo rogauracore initialize_keyboard ; sudo rogauracore brightness 0;"

# Kube Alias/Exports
export KUBECONFIG=/home/cortex/kubeconfig
alias k="kubectl"
alias kgp="kubectl -n c8 get pods"
alias kgd="kubectl -n c8 get deployments"
alias kdp="kubectl -n c8 delete pod"
alias kdd="kubectl -n c8 delete deployment"
alias kedit="kubectl -n c8 edit "
alias klog="kubectl -n c8 logs"
alias getkubes='aws s3 cp --recursive s3://sre-infra-eng-kubeconfig/ ~/kubeconfigs/ --exclude "*" --include "*kubeconfig" ; aws s3 cp --recursive s3://sre-infra-paas-kubeconfig/ ~/kubeconfigs/ --exclude "*" --include "*kubeconfig"'
alias loadap="loadkube sourabh-ap-west"
alias loadeu="loadkube sourabh-eu-west"

klogin() {
        kubectl -n c8 exec -it "$@" -- bash;
}

# GIT Alias
alias gcm="git commit -m"
alias gp="git pull"
alias gb="git branch"
alias gst="git status"

gpp() {
        master=`git remote show origin | grep "HEAD branch" | sed 's/.*: //'`
        current=`git branch --show-current`

        if [[ -z $master ]];
        then
                echo "Unable to push to git branch"
                return
        fi

        if [[ $master == $current ]];
        then
                echo "Attention! You are trying to push to default master branch"
        else
                echo "Pushing to $current"
                git push origin HEAD "$@"
        fi
}

feddeploy() {
        mode=`ccop; cat c8deploy* | grep "^MODE"`
        region=`ccop; cat c8deploy* | grep "^REGION"`
        peers=`ccop; cat c8deploy* | grep "^PEERS" | cut -d"." -f1`

        if [[ -z $mode ]];
        then
                echo "Use correct mode in the c8deploy config";
        else
                git add c8deployer_inputs.cfg ; gcm "$mode $region $peers"; gpp;
        fi
}

gsquash() {
        master=`git remote show origin | grep "HEAD branch" | sed 's/.*: //'`
        current=`git branch --show-current`

        echo "Squashing $current from $master"

        if [[ -z $master || -z $current ]];
        then
                echo "Unable to get master / current git branch"
        else
                git reset --soft `git merge-base $master $current`
        fi
}

loadkube() {
        region=$1

        if [[ -z $region ]];
        then
                echo "specify federation-region."
        else
		if [ -f  ~/kubeconfigs/$1.eng.macrometa.io/kubeconfig ]; then
	                rm -f ~/kubeconfig
        	        ln -s ~/kubeconfigs/$1.eng.macrometa.io/kubeconfig ~/kubeconfig
		elif [ -f ~/kubeconfigs/$1.paas.macrometa.io/kubeconfig ]; then
	                rm -f ~/kubeconfig
        	        ln -s ~/kubeconfigs/$1.paas.macrometa.io/kubeconfig ~/kubeconfig
		fi
        fi
}

# Update PS Colors and info
psGBranch() {
        pgbranch=`git branch --show-current 2> /dev/null`
        if [[ ! -z $pgbranch ]];
        then
                pgbranch=" (Branch: $pgbranch)"
        fi
}

psKubeC() {
        pkubec=$(readlink -eqs ~/kubeconfig 2> /dev/null)
        if [[ ! -z $pkubec ]];
        then
                pkubec=`basename $(dirname $pkubec 2> /dev/null) 2> /dev/null`
                pkubec=" (KubeConfig: $(echo $pkubec | cut -d"." -f1))"
        fi

}

kubeProxySet() {
        kubeProxy=""
	if [ "$http_proxy" != "" ] && [ "$https_proxy" != "" ]  ;  then kubeProxy=" *Kube Proxy Set*"; fi
}

set_kube_proxy() {
	port=$1
	if [ "$1" == "" ]; then
		port="1614"
	fi
	export https_proxy="localhost:$port"
	export http_proxy="localhost:$port"
}

PROMPT_COMMAND="psGBranch; psKubeC; kubeProxySet"

PS1='\n${debian_chroot:+($debian_chroot)}\[\033[01;31m\]☠   \u ☠   \[\033[01;34m\]\[\w\]\[\033[01;35m\]$pgbranch\[\033[01;32m\]$pkubec\[\033[01;35m\]$kubeProxy\n\[\033[01;36m\]\[\033[00m\] >>> ☣   '

LD_LIBRARY_PATH="/usr/local/lib"

export PATH=$PATH:~/scripts:/home/cortex/.local/bin

# FOR API SERVER
# export LDFLAGS="-Wl,--copy-dt-needed-entries"

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
cd ~
# /home/cortex/.anaconda3/bin/conda shell.bash hook > /dev/null
# <<< conda initialize <<<


export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

alias ssh="ssh -o PubKeyAcceptedAlgorithms=+ssh-rsa-cert-v01@openssh.com "

export VAGRANT_WSL_ENABLE_WINDOWS_ACCESS="1"
export PATH="$PATH:/mnt/c/Program Files/Oracle/VirtualBox"

load_kube_completion() {
	local cur=${COMP_WORDS[COMP_CWORD]}
	COMPREPLY=($(compgen -W "$(ls  ~/kubeconfigs/ | cut -f1 -d ".")" -- $cur))
}

complete -F load_kube_completion loadkube
