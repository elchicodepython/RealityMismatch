import unittest

from ..core.exceptions import (
    EntrypointNotEmpty,
    EntrypointDoesNotExist,
    LevelNotRegistered,
    AlreadyRegisteredLevel,
)
from ..core.game import Entrypoint, Level, Story
from ..core.types import LevelIdentifier, EntrypointCodename


class TestEntrypoint(unittest.TestCase):
    def _get_entrypoint(self, level_identifier="demo", codename="poc"):
        return Entrypoint(
            LevelIdentifier(level_identifier), EntrypointCodename(codename)
        )

    def test_initialization(self):
        entrypoint = self._get_entrypoint()
        self.assertEqual(
            entrypoint.codename,
            EntrypointCodename("poc"),
            msg="Entrypoint codename does not match with the provided entrypoint",
        )
        self.assertEqual(
            entrypoint.level_identifier,
            LevelIdentifier("demo"),
            msg="Entrypoint level identifier does not match with the provided level identifier",
        )
        self.assertFalse(
            entrypoint.has_level(),
            msg="Initialized entrypoint should'nt have any level registered",
        )

    def test_register(self):
        entrypoint = self._get_entrypoint()
        level = Level(LevelIdentifier("defoobarspam"), entrypoint)
        entrypoint.register(level)

        self.assertTrue(entrypoint.has_level())

        with self.assertRaises(EntrypointNotEmpty):
            entrypoint.register(level)


class TestLevel(unittest.TestCase):
    def _get_level(self):
        return Level(
            LevelIdentifier("realityId"),
            Entrypoint(
                LevelIdentifier("mismatchId"), EntrypointCodename("start")
            ),
        )

    def test_initialization(self):
        level = self._get_level()

        self.assertEqual(LevelIdentifier("realityId"), level.identifier)

        self.assertEqual(
            LevelIdentifier("mismatchId"), level.startpoint.level_identifier
        )
        self.assertEqual(
            EntrypointCodename("start"), level.startpoint.codename
        )

        self.assertListEqual([], level._entrypoints)

    def test_get_entrypoint(self):
        level = self._get_level()

        level.add_entrypoint(EntrypointCodename("demo"))

        level.get_entrypoint("demo")

        with self.assertRaises(EntrypointDoesNotExist):
            level.get_entrypoint(EntrypointCodename("invisible"))

    def test_add_entrypoint(self):
        level = self._get_level()

        level.add_entrypoint(EntrypointCodename("demo"))
        self.assertEqual(len(level._entrypoints), 1)

        level.add_entrypoint(EntrypointCodename("demo"))
        self.assertEqual(len(level._entrypoints), 1)

        level.add_entrypoint(EntrypointCodename("foo"))
        self.assertEqual(len(level._entrypoints), 2)


class TestStory(unittest.TestCase):
    def test_initialization(self):
        story = Story()
        self.assertEqual(len(story._levels), 1)

    def test_add_level(self):

        level = Level(
            LevelIdentifier("intro"),
            Entrypoint(
                LevelIdentifier("origin"), EntrypointCodename("origin")
            ),
        )
        story = Story()

        story.add_level(level)

        with self.assertRaises(AlreadyRegisteredLevel):
            story.add_level(level)

        level2 = Level(
            LevelIdentifier("end"),
            Entrypoint(
                LevelIdentifier("origin"), EntrypointCodename("origin")
            ),
        )

        with self.assertRaises(EntrypointNotEmpty):
            story.add_level(level2)

    def test__get_entrypoint(self):
        level = Level(
            LevelIdentifier("intro"),
            Entrypoint(
                LevelIdentifier("origin"), EntrypointCodename("origin")
            ),
        )
        level.add_entrypoint(EntrypointCodename("matrix"))
        story = Story()

        story.add_level(level)
        entrypoint = story._get_entrypoint(
            Entrypoint(LevelIdentifier("intro"), EntrypointCodename("matrix"))
        )

        self.assertIsInstance(entrypoint, Entrypoint)

        with self.assertRaises(EntrypointDoesNotExist):
            story._get_entrypoint(
                Entrypoint(LevelIdentifier("intro"), EntrypointCodename("bar"))
            )

        with self.assertRaises(EntrypointDoesNotExist):
            story._get_entrypoint(
                Entrypoint(
                    LevelIdentifier("foo"), EntrypointCodename("matrix")
                )
            )
