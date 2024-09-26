from __future__ import annotations
import cmd
from typing import List
from mocli.command import Command
from mocli.command.function import Function
from mocli.command.subprocess import Subprocess


class CommandLineInterface(cmd.Cmd):

    def __init__(self, builder: Builder) -> None:
        super().__init__()
        self.prompt = builder._prompt
        for command in builder._commands:
            setattr(self, f'do_{command.name}', command.fn)

    @staticmethod
    def builder(prompt: str = '(mocli) ') -> Builder:
        return CommandLineInterface.Builder(prompt)

    def get_names(self):
        # This returns a list of all methods of the class
        # including the dynamically added
        return dir(self)

    def do_exit(self, arg):
        print("bye")
        return True

    def preloop(self):
        return self.do_help('')

    class Builder:

        def __init__(self, prompt: str) -> None:
            self._prompt = prompt
            self._commands: List[Command] = []

        def __enter__(self) -> CommandLineInterface.Builder:
            return self

        def __exit__(self, exc_type, exc_value, traceback) -> None:
            pass

        def command(self, command: Command) -> None:
            self._commands.append(command)

        def build(self) -> CommandLineInterface:
            return CommandLineInterface(self)


def run():
    function = Function(name='1', fn=lambda arg: print("Hello, World!"))
    subprocess = Subprocess(name='2', command='ls -la')

    with CommandLineInterface.builder(
        prompt='(my-cli) ',
    ) as builder:
        builder.command(function)
        builder.command(subprocess)

    builder.build().cmdloop()
