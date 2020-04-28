Development of levels
=====================

Backend level development
--------------------------

To start a new level development you should
create a folder inside the levels folder defined
in configuration.

`mkdir backend/levels/demo_level`

Each backend should have at least 2 files.

- manifest.json
- level.py

Lets create our new level.py file with some dummy content:

.. code-block:: python

    from sdk.level import Level, LevelView

    from typing import List


    class HelloWorldActionView(LevelView):

        def action(cls, *args, **kwargs):
            return {
                'msg': 'hello world'
            }


    class Current(Level):

        def api(self) -> List[LevelView]:
            return [
                HelloWorldActionView(),
            ]


