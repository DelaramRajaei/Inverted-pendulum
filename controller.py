# -*- coding: utf-8 -*-

# python imports
from math import degrees

# pyfuzzy imports
from fuzzy.storage.fcl.Reader import Reader
import Equations


# import numpy as np


class FuzzyController:

    def __init__(self, fcl_path):
        self.system = Reader().load_from_file(fcl_path)
        self.membership_pa = {
            "up_more_right": 0,
            "up_right": 0,
            "up": 0,
            "up_left": 0,
            "up_more_left": 0,
            "down_more_left": 0,
            "down_left": 0,
            "down": 0,
            "down_right": 0,
            "down_more_right": 0
        }
        self.membership_pv = {
            "cw_fast": 0,
            "cw_slow": 0,
            "stop": 0,
            "ccw_slow": 0,
            "ccw_fast": 0,
        }
        self.limit_force = {
            "left_fast": 0,
            "left_slow": 0,
            "stop": 0,
            "right_slow": 0,
            "right_fast": 0,
        }
        self.membership_cv = {
            "left_fast": 0,
            "left_slow": 0,
            "stop": 0,
            "right_fast": 0,
            "right_slow": 0,
        }
        self.membership_cp = {
            "left_far": 0,
            "left_near": 0,
            "stop": 0,
            "right_near": 0,
            "right_far": 0,
        }

    # cp: cart position
    # cv: cart velocity
    # pa: pendilum angular
    # pv: pendilum velocity

    def _make_input(self, world):
        return dict(
            cp=world.x,
            cv=world.v,
            pa=degrees(world.theta),
            pv=degrees(world.omega)
        )

    def _make_output(self):
        return dict(
            force=0.
        )

    def fuzzify_pa(self, input):
        pa = Equations.pa()
        if input < 0:
            input += 360
        self.membership_pa["up_more_right"] = pa.up_more_right(input)
        self.membership_pa["up_right"] = pa.up_right(input)
        self.membership_pa["up"] = pa.up(input)
        self.membership_pa["up_left"] = pa.up_left(input)
        self.membership_pa["up_more_left"] = pa.up_more_left(input)
        self.membership_pa["down_more_left"] = pa.down_more_left(input)
        self.membership_pa["down_left"] = pa.down_left(input)
        self.membership_pa["down"] = pa.down(input)
        self.membership_pa["down_right"] = pa.down_right(input)
        self.membership_pa["down_more_right"] = pa.down_more_right(input)

    def fuzzify_pv(self, input):
        pv = Equations.pv()
        if input > 200:
            input = 200
        elif input < -200:
            input = -200
        self.membership_pv["cw_fast"] = pv.cw_fast(input)
        self.membership_pv["cw_slow"] = pv.cw_slow(input)
        self.membership_pv["stop"] = pv.stop(input)
        self.membership_pv["ccw_slow"] = pv.ccw_slow(input)
        self.membership_pv["ccw_fast"] = pv.ccw_fast(input)

    def fuzzify_cv(self, input):
        cv = Equations.cv()
        self.membership_cv["left_fast"] = cv.left_fast(input)
        self.membership_cv["left_slow"] = cv.left_slow(input)
        self.membership_cv["stop"] = cv.stop(input)
        self.membership_cv["right_fast"] = cv.right_fast(input)
        self.membership_cv["right_slow"] = cv.right_slow(input)

    def fuzzify_cp(self, input):
        cp = Equations.cp()
        self.membership_cp["left_far"] = cp.left_far(input)
        self.membership_cp["left_near"] = cp.left_near(input)
        self.membership_cp["stop"] = cp.stop(input)
        self.membership_cp["right_near"] = cp.right_near(input)
        self.membership_cp["right_far"] = cp.right_far(input)

    def fuzzification(self, input):
        self.fuzzify_pa(input.get('pa'))
        self.fuzzify_pv(input.get('pv'))
        self.fuzzify_cv(input.get('cv'))
        self.fuzzify_cp(input.get('cp'))

    def inference(self):
        # RULE 0: IF (pa IS up AND pv IS stop)
        #         OR (pa IS up_right AND pv IS ccw_slow)
        # 		  OR (pa IS up_left AND pv IS cw_slow)
        # 		  THEN force IS stop;
        # RULE 10: IF (pa IS down_more_right) AND (pv IS cw_slow) THEN force IS stop;
        # RULE 12: IF (pa IS down_more_left) AND (pv IS ccw_slow) THEN force IS stop;
        # RULE 13: IF (pa IS down_more_right) AND (pv IS ccw_fast) THEN force IS stop;
        # RULE 14: IF (pa IS down_more_right) AND (pv IS cw_fast) THEN force IS stop;
        # RULE 15: IF (pa IS down_more_left) AND (pv IS cw_fast) THEN force IS stop;
        # RULE 16: IF (pa IS down_more_left) AND (pv IS ccw_fast) THEN force IS stop;
        # RULE 21: IF (pa IS down_right) AND (pv IS ccw_fast) THEN force IS stop;
        # RULE 23: IF (pa IS down_left) AND (pv IS cw_fast) THEN force IS stop;
        # RULE 36: IF (pa IS down) AND (pv IS cw_fast) THEN force IS stop;
        # RULE 37: IF (pa IS down) AND (pv IS ccw_fast) THEN force IS stop;
        # RULE 42: IF (pa IS up) AND (pv IS stop) THEN force IS stop;
        self.limit_force["stop"] = max(
            min(self.membership_pa["up"], self.membership_pv["stop"]),
            min(self.membership_pa["up_right"], self.membership_pv["ccw_slow"]),
            min(self.membership_pa["up_left"], self.membership_pv["cw_slow"]),
            min(self.membership_pa["down_more_right"], self.membership_pv["cw_slow"]),
            min(self.membership_pa["down_more_left"], self.membership_pv["ccw_slow"]),
            min(self.membership_pa["down_more_right"], self.membership_pv["ccw_fast"]),
            min(self.membership_pa["down_more_right"], self.membership_pv["cw_fast"]),
            min(self.membership_pa["down_more_left"], self.membership_pv["cw_fast"]),
            min(self.membership_pa["down_more_left"], self.membership_pv["ccw_fast"]),
            min(self.membership_pa["up"], self.membership_pv["stop"]),
            min(self.membership_pa["down"], self.membership_pv["ccw_fast"]),
            min(self.membership_pa["down"], self.membership_pv["cw_fast"]),
            min(self.membership_pa["down_left"], self.membership_pv["cw_fast"]),
            min(self.membership_pa["down_right"], self.membership_pv["ccw_fast"]),
            # New Rules
            min(self.membership_pa["up_more_right"], self.membership_pv["ccw_fast"], self.membership_cv["left_slow"]),
            min(self.membership_pa["down_left"], self.membership_pv["ccw_fast"], self.membership_cv["left_slow"]),
            min(self.membership_pa["up_left"], self.membership_pv["cw_slow"], self.membership_cv["left_slow"]),
            min(self.membership_pa["up"], self.membership_pv["ccw_slow"], self.membership_cv["left_slow"]),
            min(self.membership_pa["up_more_left"], self.membership_pv["cw_fast"], self.membership_cv["right_slow"]),
            min(self.membership_pa["down_right"], self.membership_pv["cw_fast"], self.membership_cv["right_slow"]),
            min(self.membership_pa["up_right"], self.membership_pv["ccw_slow"], self.membership_cv["right_slow"]),
            min(self.membership_pa["up"], self.membership_pv["cw_slow"], self.membership_cv["right_slow"])
        )

        # RULE 1: IF (pa IS up_more_right) AND (pv IS ccw_slow) THEN force IS right_fast;
        # RULE 2: IF (pa IS up_more_right) AND (pv IS cw_slow) THEN force IS right_fast;
        # RULE 6: IF (pa IS up_more_right) AND (pv IS cw_fast) THEN force IS right_fast;
        # RULE 9: IF (pa IS down_more_right) AND (pv IS ccw_slow) THEN force IS right_fast;
        # RULE 17: IF (pa IS down_right) AND (pv IS ccw_slow) THEN force IS right_fast;
        # RULE 18: IF (pa IS down_right) AND (pv IS cw_slow) THEN force IS right_fast;
        # RULE 26: IF (pa IS up_right) AND (pv IS cw_slow) THEN force IS right_fast;
        # RULE 27: IF (pa IS up_right) AND (pv IS stop) THEN force IS right_fast;
        # RULE 32: IF (pa IS up_right) AND (pv IS cw_fast) THEN force IS right_fast;
        # RULE 33: IF (pa IS up_left) AND (pv IS cw_fast) THEN force IS right_fast;
        # RULE 35: IF (pa IS down) AND (pv IS stop) THEN force IS right_fast;
        # RULE 41: IF (pa IS up) AND (pv IS cw_fast) THEN force IS right_fast;
        self.limit_force["right_fast"] = max(
            min(self.membership_pa["up_more_right"], self.membership_pv["ccw_slow"]),
            min(self.membership_pa["up_more_right"], self.membership_pv["cw_slow"]),
            min(self.membership_pa["up_more_right"], self.membership_pv["cw_fast"]),
            min(self.membership_pa["down_more_right"], self.membership_pv["ccw_slow"]),
            min(self.membership_pa["down_right"], self.membership_pv["ccw_slow"]),
            min(self.membership_pa["down_right"], self.membership_pv["cw_slow"]),
            min(self.membership_pa["up_right"], self.membership_pv["cw_slow"]),
            min(self.membership_pa["up_right"], self.membership_pv["stop"]),
            min(self.membership_pa["up_right"], self.membership_pv["cw_fast"]),
            min(self.membership_pa["up_left"], self.membership_pv["cw_fast"]),
            min(self.membership_pa["down"], self.membership_pv["stop"]),
            min(self.membership_pa["up"], self.membership_pv["cw_fast"]),
            # New Rules
            min(self.membership_pa["up_more_left"], self.membership_pv["cw_fast"], self.membership_cv["left_slow"]),
            min(self.membership_pa["down_right"], self.membership_pv["cw_fast"], self.membership_cv["left_slow"]),
            min(self.membership_pa["up_right"], self.membership_pv["ccw_slow"], self.membership_cv["left_slow"]),
            min(self.membership_pa["up"], self.membership_pv["cw_slow"], self.membership_cv["left_slow"])
        )

        # RULE 3: IF (pa IS up_more_left) AND (pv IS cw_slow) THEN force IS left_fast;
        # RULE 4: IF (pa IS up_more_left) AND (pv IS ccw_slow) THEN force IS left_fast;
        # RULE 8: IF (pa IS up_more_left) AND (pv IS ccw_fast) THEN force IS left_fast;
        # RULE 11: IF (pa IS down_more_left) AND (pv IS cw_slow) THEN force IS left_fast;
        # RULE 19: IF (pa IS down_left) AND (pv IS cw_slow) THEN force IS left_fast;
        # RULE 20: IF (pa IS down_left) AND (pv IS ccw_slow) THEN force IS left_fast;
        # RULE 29: IF (pa IS up_left) AND (pv IS ccw_slow) THEN force IS left_fast;
        # RULE 30: IF (pa IS up_left) AND (pv IS stop) THEN force IS left_fast;
        # RULE 31: IF (pa IS up_right) AND (pv IS ccw_fast) THEN force IS left_fast;
        # RULE 34: IF (pa IS up_left) AND (pv IS ccw_fast) THEN force IS left_fast;
        # RULE 39: IF (pa IS up) AND (pv IS ccw_fast) THEN force IS left_fast;
        self.limit_force["left_fast"] = max(
            min(self.membership_pa["up_more_left"], self.membership_pv["cw_slow"]),
            min(self.membership_pa["up_more_left"], self.membership_pv["ccw_slow"]),
            min(self.membership_pa["up_more_left"], self.membership_pv["ccw_fast"]),
            min(self.membership_pa["down_more_left"], self.membership_pv["cw_slow"]),
            min(self.membership_pa["down_left"], self.membership_pv["cw_slow"]),
            min(self.membership_pa["down_left"], self.membership_pv["ccw_slow"]),
            min(self.membership_pa["up_left"], self.membership_pv["ccw_slow"]),
            min(self.membership_pa["up_left"], self.membership_pv["stop"]),
            min(self.membership_pa["up_right"], self.membership_pv["ccw_fast"]),
            min(self.membership_pa["up"], self.membership_pv["ccw_fast"]),
            min(self.membership_pa["up_left"], self.membership_pv["ccw_fast"]),
            # New Rules
            min(self.membership_pa["up_more_right"], self.membership_pv["ccw_fast"], self.membership_cv["right_slow"]),
            min(self.membership_pa["down_left"], self.membership_pv["ccw_fast"], self.membership_cv["right_slow"]),
            min(self.membership_pa["up_left"], self.membership_pv["cw_slow"], self.membership_cv["right_slow"]),
            min(self.membership_pa["up"], self.membership_pv["ccw_slow"], self.membership_cv["right_slow"])
        )

        # RULE 5: IF (pa IS up_more_right) AND (pv IS ccw_fast) THEN force IS left_slow;
        # RULE 24: IF (pa IS down_left) AND (pv IS ccw_fast) THEN force IS left_slow;
        # RULE 28: IF (pa IS up_left) AND (pv IS cw_slow) THEN force IS left_slow;
        # RULE 38: IF (pa IS up) AND (pv IS ccw_slow) THEN force IS left_slow;
        self.limit_force["left_slow"] = max(
            min(self.membership_pa["up_more_right"], self.membership_pv["ccw_fast"]),
            min(self.membership_pa["down_left"], self.membership_pv["ccw_fast"]),
            min(self.membership_pa["up_left"], self.membership_pv["cw_slow"]),
            min(self.membership_pa["up"], self.membership_pv["ccw_slow"]),
            # New Rule
            min(self.membership_pa["up_more_left"], self.membership_pv["cw_slow"], self.membership_cv["left_slow"]),
            min(self.membership_pa["up_more_left"], self.membership_pv["ccw_slow"], self.membership_cv["left_slow"]),
            min(self.membership_pa["up_more_left"], self.membership_pv["ccw_fast"], self.membership_cv["left_slow"]),
            min(self.membership_pa["down_more_left"], self.membership_pv["cw_slow"], self.membership_cv["left_slow"]),
            min(self.membership_pa["down_left"], self.membership_pv["cw_slow"], self.membership_cv["left_slow"]),
            min(self.membership_pa["down_left"], self.membership_pv["ccw_slow"], self.membership_cv["left_slow"]),
            min(self.membership_pa["up_left"], self.membership_pv["ccw_slow"], self.membership_cv["left_slow"]),
            min(self.membership_pa["up_left"], self.membership_pv["stop"], self.membership_cv["left_slow"]),
            min(self.membership_pa["up_right"], self.membership_pv["ccw_fast"], self.membership_cv["left_slow"]),
            min(self.membership_pa["up"], self.membership_pv["ccw_fast"], self.membership_cv["left_slow"]),
            min(self.membership_pa["up_left"], self.membership_pv["ccw_fast"], self.membership_cv["left_slow"])
        )

        # RULE 7: IF (pa IS up_more_left) AND (pv IS cw_fast) THEN force IS right_slow;
        # RULE 22: IF (pa IS down_right) AND (pv IS cw_fast) THEN force IS right_slow;
        # RULE 25: IF (pa IS up_right) AND (pv IS ccw_slow) THEN force IS right_slow;
        # RULE 40: IF (pa IS up) AND (pv IS cw_slow) THEN force IS right_slow;
        self.limit_force["right_slow"] = max(
            min(self.membership_pa["up_more_left"], self.membership_pv["cw_fast"]),
            min(self.membership_pa["down_right"], self.membership_pv["cw_fast"]),
            min(self.membership_pa["up_right"], self.membership_pv["ccw_slow"]),
            min(self.membership_pa["up"], self.membership_pv["cw_slow"]),
            # New Rules
            min(self.membership_pa["up_more_right"], self.membership_pv["ccw_slow"], self.membership_cv["right_slow"]),
            min(self.membership_pa["up_more_right"], self.membership_pv["cw_slow"], self.membership_cv["right_slow"]),
            min(self.membership_pa["up_more_right"], self.membership_pv["cw_fast"], self.membership_cv["right_slow"]),
            min(self.membership_pa["down_more_right"], self.membership_pv["ccw_slow"],
                self.membership_cv["right_slow"]),
            min(self.membership_pa["down_right"], self.membership_pv["ccw_slow"], self.membership_cv["right_slow"]),
            min(self.membership_pa["down_right"], self.membership_pv["cw_slow"], self.membership_cv["right_slow"]),
            min(self.membership_pa["up_right"], self.membership_pv["cw_slow"], self.membership_cv["right_slow"]),
            min(self.membership_pa["up_right"], self.membership_pv["stop"], self.membership_cv["right_slow"]),
            min(self.membership_pa["up_right"], self.membership_pv["cw_fast"], self.membership_cv["right_slow"]),
            min(self.membership_pa["up_left"], self.membership_pv["cw_fast"], self.membership_cv["right_slow"]),
            min(self.membership_pa["down"], self.membership_pv["stop"], self.membership_cv["right_slow"]),
            min(self.membership_pa["up"], self.membership_pv["cw_fast"], self.membership_cv["right_slow"])
        )

    def defuzzify_force(self, point):
        force = Equations.force()
        stop = min(force.stop(point), self.limit_force["stop"])
        left_fast = min(force.left_fast(point), self.limit_force["left_fast"])
        right_fast = min(force.right_fast(point), self.limit_force["right_fast"])
        left_slow = min(force.left_slow(point), self.limit_force["left_slow"])
        right_slow = min(force.right_slow(point), self.limit_force["right_slow"])
        return max(stop, left_fast, right_fast, left_slow, right_slow)

    def defuzzification(self):
        n = 10000
        delta = 200. / n
        points_of_force = [-100. + i * delta for i in range(n + 1)]
        sum_numerator = 0
        sum_denominator = 0
        dx = points_of_force[1] - points_of_force[0]
        for point in points_of_force:
            membership = self.defuzzify_force(point)
            sum_numerator += membership * point * dx
            sum_denominator += membership * dx

        try:
            return sum_numerator / sum_denominator
        except:
            return 0

    def invertedPendulum(self, input):
        self.fuzzification(input)
        self.inference()
        return self.defuzzification()

    def decide(self, world):
        # output = self._make_output()
        # self.system.calculate(self._make_input(world), output)
        force = self.invertedPendulum(self._make_input(world))
        return force
