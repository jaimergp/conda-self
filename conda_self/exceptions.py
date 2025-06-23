from conda.exceptions import CondaError


class SpecsAreNotPlugins(CondaError):
    def __init__(self, specs: list[str]):
        super().__init__(f"The following requested specs are not plugins: {specs}")


class SpecsCanNotBeRemoved(CondaError):
    def __init__(self, specs: list[str]):
        super().__init__(f"Packages '{specs}' can not be removed.")
