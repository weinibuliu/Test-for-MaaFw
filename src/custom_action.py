from maa.custom_action import CustomAction
from maa.context import Context


def act_name():
    return ["A", "B"]


def acts():
    return [A(), B()]


class A(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:
        print("A")
        return True


class B(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:
        print("B")
        return True
