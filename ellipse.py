from dataclasses import dataclass


@dataclass
class Ellipse:
    xLen: float
    yLen: float

    def xAxis(self):
        return self.xLen / 2

    def yAxis(self):
        return self.yLen / 2
