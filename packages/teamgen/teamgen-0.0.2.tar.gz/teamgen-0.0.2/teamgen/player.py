from dataclasses import dataclass


@dataclass
class Player:

    pk: int
    gender: str
    ntrp: float
    microntrp: float
    phone: str
    name: str

    @property
    def Name(self):
        return self.name

    def __hash__(self):
        return hash((self.pk, self.name))

    def todict(self):
        return self.__dict__
