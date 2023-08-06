import os
import sys
from recycle.lib import my_print, HOME, my_input

shell_config = {
    "zsh": "compdef '_files -W ~/.Trash`pwd`' undel\ncompdef '_files -W ~/.Trash`pwd`' pdel\n",
    "bash": """_undel() {
    local trash_home="$HOME/.Trash"
    local current_path=`pwd`
    local current_arg="${COMP_WORDS[COMP_CWORD]}"
    local trash_dir=$trash_home$current_path/${COMP_LINE:6:999}
    local IFS=$'\t\n'

    if [[ $current_arg =~ ^/ ]] ; then
      # /a/b/c
      return 0
    elif [[ $current_path =~ $trash_home ]] ; then
      # in /root/.Trash/
      return 0
    elif [[ ! -d $trash_dir ]] ; then
      # /root/.Trash/`pwd` don't exists
      return 0
    elif [[ -d $trash_dir ]] ; then
      COMPREPLY=( $(compgen -W "`ls -a $trash_dir|grep -Pv '^\.{1,2}$'`" -- ${current_arg}) )
      return 0
    fi
}

complete -o filenames -o dirnames -o default -F _undel undel
complete -o filenames -o dirnames -o default -F _undel pdel
""",
}


def install(shell, path):
    shellrc_path = "{}/.{}rc".format(HOME, shell)

    if not os.path.exists("/bin/" + shell):
        return my_print("your don't have {}, skip it".format(shell))

    open(shellrc_path, "a+").close()

    if "undel" not in open(shellrc_path, "r").read():
        open(shellrc_path, "a+").write(shell_config[shell])
        my_print("Installed in {}, enjoy it :)".format(shellrc_path))

    if not path:
        return

    path = "export PATH={}\n".format(path)
    if path in open(shellrc_path).readlines():
        return
    my_print('Write "{}" in {}'.format(path.strip(), shellrc_path))
    open(shellrc_path, "a+").write(path)


def main():
    scripts_dir_path = os.path.dirname(sys.argv[0])
    if scripts_dir_path in os.getenv("PATH"):
        path = None
    elif (
        "n"
        in my_input(
            'Add "{}" to your PATH, to enable it?[Y/n]'.format(scripts_dir_path)
        ).lower()
    ):
        path = None
    else:
        path = "{}:$PATH".format(scripts_dir_path)

    install("zsh", path)
    install("bash", path)
    command = "source ~/.{}rc".format(os.getenv("SHELL").split("/")[-1])
    my_print('\nPlease Execute "{}"\n'.format(command))
