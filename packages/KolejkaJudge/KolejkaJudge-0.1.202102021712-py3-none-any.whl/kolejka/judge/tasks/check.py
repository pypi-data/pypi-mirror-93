# vim:ts=4:sts=4:sw=4:expandtab
import glob
import shlex


from kolejka.judge import config
from kolejka.judge.paths import *
from kolejka.judge.typing import *
from kolejka.judge.validators import *
from kolejka.judge.commands import *
from kolejka.judge.tasks.base import TaskBase


__all__ = [ 'AnswerHintDiffTask', ]
def __dir__():
    return __all__


class AnswerHintDiffTask(TaskBase):
    DEFAULT_RESULT_ON_ERROR='ANS'
    DEFAULT_ANSWER_PATH=config.TEST_ANSWER
    DEFAULT_CASE_SENSITIVE=True
    DEFAULT_SPACE_SENSITIVE=False
    @default_kwargs
    def __init__(self, hint_path, answer_path, case_sensitive, space_sensitive, **kwargs):
        super().__init__(**kwargs)
        self.hint_path = get_output_path(hint_path)
        self.answer_path = get_output_path(answer_path)
        self.case_sensitive = bool(case_sensitive)
        self.space_sensitive = bool(space_sensitive)

    def execute(self):
        self.set_result(self.run_command('diff', DiffCommand, path_a=self.hint_path, path_b=self.answer_path, case_sensitive=self.case_sensitive, space_sensitive=self.space_sensitive))
        return self.result
