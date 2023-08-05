from cleo import option

from .base import Command
from kal.utils.config import Config


class GitConfigCommand(Command):
    name = 'config'
    description = 'set git global config'

    options = [
        option('no-input', description='run with no confirm')
    ]

    def handle(self):
        git_config_list = Config.get('git', 'config', default=list())
        if not self.option('no-input') and not self.confirm('git config 세팅을 실행하시겠습니까?', default=True):
            self.line_error('실행 거부')
            return 1

        for line in git_config_list:
            command = "git config --global {}".format(line)
            self.line(command)
            self.shell_call(command)
        self.line('Done')


class GitCommand(Command):
    name = 'git'
    description = 'git helper command'
    commands = [
        GitConfigCommand()
    ]

    def handle(self):
        self.line_error('하위 명령어를 입력해주세요.')
        return 1
