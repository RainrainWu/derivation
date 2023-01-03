from json import dumps


class VariantsError(Exception):
    def __str__(self) -> str:

        if len(self.args) <= 1:
            return super().__str__()

        return f"{self.args[0]}\n{dumps(self.args[1], indent=2, default=str)}"


class ConstraintError(VariantsError):

    pass


class GeneratorError(VariantsError):

    pass
