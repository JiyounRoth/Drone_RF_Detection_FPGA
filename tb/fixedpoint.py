import numpy as np

class FixedPoint:
    @staticmethod
    def q1_15_to_float(signed_int):
        return signed_int / float(1 << 15)