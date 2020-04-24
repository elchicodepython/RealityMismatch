from sdk.level import Level, LevelView

from typing import List


class SayHelloWorld(LevelView):
    def action(cls, *args, **kwargs):
        return {"msg": "hello world"}


class NotCurrent(Level):
    def api(self) -> List[LevelView]:
        return {"say-hello-world": SayHelloWorld()}
