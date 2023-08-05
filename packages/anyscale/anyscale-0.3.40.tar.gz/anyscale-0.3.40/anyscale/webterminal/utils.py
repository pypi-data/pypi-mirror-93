import re
import secrets
from typing import Any, List, Optional, Tuple

import base62


def generate_session_command_id() -> str:
    """
    generate_session_command_id is a mirror from
    backend/server/utils/id_gen.py. Consult this
    source of truth for changes
    """
    id_part = base62.encodebytes(secrets.token_bytes(16))
    return f"scd_{id_part}"


# *_DELIMITER are used within preexec / precmd zsh hooks to so that
# we can parse out command information for logging commands, their outputs
# and their statuses.
START_COMMAND_DELIMITER = "71DbDeuXGpbEn8KO93V4kH56xr992Zu3RoUAW0lWesqPWCFff9PVr1RE"
START_OUTPUT_DELIMITER = "YJipyPN4Quh41VbKKHoYqS6bUzw8d0soTo8W61jeBTQUm9F4IRZvQoqg"
END_OUTPUT_DELIMITER = "jjVvK9ydZGXScXs5G89zgqVtwCSYMGdmV2Za9VaTVV3jraSP6hCB5F"
END_COMMAND_DELIMITER = "FwCsfKV6Xfg7PbUJD9sJfZWRBgfAG9uQBj4BBx6uWnss5k2HA3VXtuwb"

ANYSCALE_PREFIX = "7JexUxYaAJfstcUh5rN5CD3nAP24FbpfDAP4Uk8NP879H2N2CntNKk"
CMD_MATCH_TEXT = f"{ANYSCALE_PREFIX}_command="
RET_STATUS_MATCH_TEXT = f"{ANYSCALE_PREFIX}_return_status="

# The default zshrc file that will be used by our zsh terminal.
# This includes output delimiters
zshrc = """
autoload -U add-zsh-hook

print_start_output_delimiter() {{
  echo "{START_COMMAND_DELIMITER}"
  # the command
  echo {CMD_MATCH_TEXT}$1
  echo "{START_OUTPUT_DELIMITER}"
}}

print_end_output_delimiter() {{
  # save the command exit code, then emit it.
  RET_STAT=$?
  echo "{END_OUTPUT_DELIMITER}"
  echo {RET_STATUS_MATCH_TEXT}$RET_STAT
  echo "{END_COMMAND_DELIMITER}"
}}
add-zsh-hook preexec print_start_output_delimiter
add-zsh-hook precmd print_end_output_delimiter

""".format(
    START_COMMAND_DELIMITER=START_COMMAND_DELIMITER,
    START_OUTPUT_DELIMITER=START_OUTPUT_DELIMITER,
    END_COMMAND_DELIMITER=END_COMMAND_DELIMITER,
    END_OUTPUT_DELIMITER=END_OUTPUT_DELIMITER,
    CMD_MATCH_TEXT=CMD_MATCH_TEXT,
    RET_STATUS_MATCH_TEXT=RET_STATUS_MATCH_TEXT,
)


# EXEC_ZSH_CMD starts zsh. It should be run from bash
# The reason we need to run this instead of just bash
# is so that we can inherit all the environment variables
# from .bashrc like anaconda for example. This is a temporary solution
EXEC_ZSH_CMD = "ZDOTDIR=/tmp zsh"


def write_zshrc(zshrc_dir: str = "/tmp/") -> None:
    """
    write_zshrc will create a .zshrc file within /tmp/.zshrc
    Use /tmp/ rather than ~ because WT does not write to same
    relative paths as the user.
    When instatiating each zsh, we can use ZDOTDIR=/tmp zsh
    so that it uses this .zshrc file.
    """
    zshrc_file = open(f"{zshrc_dir}.zshrc", "w")
    zshrc_file.write(zshrc)
    zshrc_file.close()


class Command:
    def __init__(
        self,
        scid: str = "",
        finished: bool = False,
        output: str = "",
        command: str = "",
        status_code: Optional[int] = None,
    ):
        self.scid = scid
        self.finished = finished
        self.output = output
        self.command = command
        self.status_code = status_code

    def __eq__(self, other: Any) -> bool:
        if isinstance(self, other.__class__):
            return bool(
                self.finished == other.finished
                and self.output == other.output
                and self.command == other.command
                and self.status_code == other.status_code
            )
        return False


def extract_commands(
    stdout: str, last_command: Optional[Command]
) -> Tuple[str, List[Command]]:
    """
    extract_commands parse the stdout into commands.
    It also removes any emitted anyscale values like delimiters.
    This functions as follows:
    -- split out all delimiters. All anyscale values are wrapped
    by delimiters so they will be a separate value in the resulting array
    for example:
        "DELIM CMD DELIM STDOUT STDOUT DELIM RET_VAL DELIM" =>
        ["CMD", "STDOUT STDOUT", "RET_VAL"]
    -- for each value
    -- If its a command: Create a new CMD
    -- If its a return status: Mark the last CMD as finished if its not
    -- If its output: Associate with any running commands

    Assumption:
    -- Both DELIMITERS wrapping an emitted value will always be present.
    e.g. "START_CMD cmd START_OUTPUT" will be emitted togeter. This is empirically
    how zsh emits the precmd / preexec function fortunately.
    """
    values = re.split(
        f"{START_COMMAND_DELIMITER}\r?\n?|{START_OUTPUT_DELIMITER}\r?\n?|{END_COMMAND_DELIMITER}\r?\n?|{END_OUTPUT_DELIMITER}\r?\n?",
        stdout,
    )
    output_to_user = ""
    commands = [last_command] if last_command is not None else []
    for val in values:
        if CMD_MATCH_TEXT in val:
            # remove white space from end of command. Then remove the cmd_match_text prefix.
            cmd_text = val.rstrip().split(CMD_MATCH_TEXT)[-1]
            command = Command(command=cmd_text, scid=generate_session_command_id())
            commands.append(command)
        elif RET_STATUS_MATCH_TEXT in val:
            # We emit a return status even for entered new lines
            # So check to make sure there is a command running
            if len(commands) > 0 and commands[-1].finished is False:
                status_code = val.rstrip().split(RET_STATUS_MATCH_TEXT)[-1]
                cmd = commands[-1]
                cmd.status_code = int(status_code)
                cmd.finished = True
        else:
            output_to_user += val
            # If there is a running command, add this output to it to be logged.
            if len(commands) > 0 and commands[-1].finished is False:
                cmd = commands[-1]
                cmd.output += val
    return (output_to_user, commands)
