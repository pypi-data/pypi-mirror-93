# vim:ts=4:sts=4:sw=4:expandtab


from kolejka.judge import config
from kolejka.judge.parse import *
from kolejka.judge.paths import *
from kolejka.judge.typing import *
from kolejka.judge.validators import *
from kolejka.judge.tasks.base import *
from kolejka.judge.systems.base import *


__all__ = [ 'RulesTask', 'SolutionSourceRulesTask', 'SolutionBuildRulesTask' ]
def __dir__():
    return __all__


class RulesTask(TaskBase):
    DEFAULT_RESULT_ON_ERROR='RUL'
    @default_kwargs
    def __init__(self, target, max_size=None, **kwargs):
        super().__init__(**kwargs)
        self.target = get_output_path(target)
        self.max_size = parse_memory(max_size)
    
    def execute(self):
        if self.max_size:
            used_size = sum(
                    [ self.resolve_path(f).stat().st_size for f in self.find_files(self.target) ]
                    )
            if used_size > self.max_size:
                self.set_result(self.result_on_error)
        return self.result


class SolutionSourceRulesTask(RulesTask):
    DEFAULT_TARGET=config.SOLUTION_SOURCE
    @default_kwargs
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SolutionBuildRulesTask(RulesTask):
    DEFAULT_TARGET=config.SOLUTION_BUILD
    @default_kwargs
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
