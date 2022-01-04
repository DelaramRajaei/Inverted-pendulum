class pa:
    # up_more_right := (0, 0)(30, 1)(60, 0)
    def up_more_right(self, input):
        if (0 <= input) and (input < 30):
            return 0.033 * input
        elif (30 <= input) and (input <= 60):
            return (-0.033 * input) + 1.99
        else:
            return 0

    # up_right := (30, 0)(60, 1)(90, 0)
    def up_right(self, input):
        if (30 <= input) and (input < 60):
            return (0.033 * input) - 0.99
        elif (60 <= input) and (input <= 90):
            return (-0.033 * input) + 2.99
        else:
            return 0

    # up := (60, 0)(90, 1)(120, 0)
    def up(self, input):
        if (60 <= input) and (input < 90):
            return (0.033 * input) - 1.99
        elif (90 <= input) and (input <= 120):
            return (-0.033 * input) + 3.99
        else:
            return 0

    # up_more_left := (120, 0)(150, 1)(180, 0)
    def up_more_left(self, input):
        if (120 <= input) and (input < 150):
            return (0.033 * input) - 3.6
        elif (150 <= input) and (input <= 180):
            return (-0.033 * input) + 5.5
        else:
            return 0

    # up_left := (90, 0)(120, 1)(150, 0)
    def up_left(self, input):
        if (90 <= input) and (input < 120):
            return (0.033 * input) - 2.7
        elif (120 <= input) and (input <= 150):
            return (-0.033 * input) + 4.6
        else:
            return 0

    # down_more_left := (180, 0)(210, 1)(240, 0);
    def down_more_left(self, input):
        if (180 <= input) and (input < 210):
            return (0.033 * input) - 5.4
        elif (210 <= input) and (input <= 240):
            return (-0.033 * input) + 7.3
        else:
            return 0

    # down_left := (210, 0)(240, 1)(270, 0);
    def down_left(self, input):
        if (210 <= input) and (input < 240):
            return (0.033 * input) - 6.3
        elif (240 <= input) and (input <= 270):
            return (-0.033 * input) + 8.2
        else:
            return 0

    # down := (240, 0)(270, 1)(300, 0);
    def down(self, input):
        if (240 <= input) and (input < 270):
            return (0.033 * input) - 7.2
        elif (270 <= input) and (input <= 300):
            return (-0.033 * input) + 9.1
        else:
            return 0

    # down_more_right := (300, 0)(330, 1)(360, 0);
    def down_more_right(self, input):
        if (300 <= input) and (input < 330):
            return (0.033 * input) - 9
        elif (330 <= input) and (input <= 360):
            return (-0.033 * input) + 10.9
        else:
            return 0

    # down_right := (270, 0)(300, 1)(330, 0);
    def down_right(self, input):
        if (270 <= input) and (input < 300):
            return (0.033 * input) - 8.1
        elif (300 <= input) and (input <= 330):
            return (-0.033 * input) + 10
        else:
            return 0


class pv:
    # cw_fast := (-200, 1)(-100, 0);
    def cw_fast(self, input):
        if (-200 <= input) and (input <= -100):
            return (-0.01 * input) - 1
        else:
            return 0

    # cw_slow := (-200, 0)(-100, 1)(0, 0);
    def cw_slow(self, input):
        if (-200 <= input) and (input < -100):
            return (0.01 * input) + 2
        elif (-100 <= input) and (input <= 0):
            return -0.01 * input
        else:
            return 0

    # stop := (-100, 0) (0, 1) (100, 0);
    def stop(self, input):
        if (-100 <= input) and (input < 0):
            return (0.01 * input) + 1
        elif (0 <= input) and (input <= 100):
            return (-0.01 * input) + 1
        else:
            return 0

    # ccw_slow := (0, 0) (100, 1) (200, 0);
    def ccw_slow(self, input):
        if (0 <= input) and (input < 100):
            return 0.01 * input
        elif (100 <= input) and (input <= 200):
            return (-0.01 * input) + 2
        else:
            return 0

    # ccw_fast := (100, 0) (200, 1);
    def ccw_fast(self, input):
        if (100 <= input) and (input <= 200):
            return (0.01 * input) - 1
        else:
            return 0


class force:
    # left_fast := (-100, 0) (-80, 1) (-60, 0);
    def left_fast(self, input):
        if (-100 <= input) and (input < -80):
            return (0.05 * input) + 5
        elif (-80 <= input) and (input <= -60):
            return (-0.05 * input) - 3
        else:
            return 0

    # left_slow := (-80, 0) (-60, 1) (0, 0);
    def left_slow(self, input):
        if (-80 <= input) and (input < -60):
            return (0.05 * input) + 4
        elif (-60 <= input) and (input <= 0):
            return -0.05 * input
        else:
            return 0

    # stop := (-60, 0) (0, 1) (60, 0);
    def stop(self, input):
        if (-60 <= input) and (input < 0):
            return (0.0166 * input) + 0.999
        elif (0 <= input) and (input <= 60):
            return (-0.0166 * input) + 0.999
        else:
            return 0

    # right_slow := (0, 0) (60, 1) (80, 0);
    def right_slow(self, input):
        if (0 <= input) and (input < 60):
            return 0.0166 * input
        elif (60 <= input) and (input <= 80):
            return (-0.0166 * input) + 1.33
        else:
            return 0

    # right_fast := (60, 0) (80, 1) (100, 0);
    def right_fast(self, input):
        if (60 <= input) and (input < 80):
            return (0.05 * input) - 3
        elif (80 <= input) and (input <= 100):
            return (-0.05 * input) + 5
        else:
            return 0


class cp:
    # left_far := (-10, 1) (-5, 0);
    def left_far(self, input):
        if (-10 <= input) and (input <= -5):
            return (-0.1 * input) - 0.5
        else:
            return 0

    # left_near := (-10, 0) (-2.5, 1) (0, 0);
    def left_near(self, input):
        if (-10 <= input) and (input < -2.5):
            return (0.133 * input) - 1.33
        elif (-2.5 <= input) and (input <= 0):
            return -0.133 * input
        else:
            return 0

    # stop := (-2.5, 0) (0, 1) (2.5, 0);
    def stop(self, input):
        if (-2.5 <= input) and (input < 0):
            return (0.4 * input) + 1
        elif (0 <= input) and (input <= 2.5):
            return (-0.4 * input) - 1
        else:
            return 0

    # right_near := (0, 0) (2.5, 1) (10, 0);
    def right_near(self, input):
        if (0 <= input) and (input < 2.5):
            return 0.4 * input
        elif (2.5 <= input) and (input <= 10):
            return (-0.4 * input) + 4
        else:
            return 0

    # right_far := (5, 0) (10, 1);
    def right_far(self, input):
        if (5 <= input) and (input <= 10):
            return (0.2 * input) - 1
        else:
            return 0


class cv:
    # left_fast := (-5, 1) (-2.5, 0);
    def left_fast(self, input):
        if (-5 <= input) and (input <= -2.5):
            return (-0.4 * input) - 1
        else:
            return 0

    # left_slow := (-5, 0) (-1, 1) (0, 0);
    def left_slow(self, input):
        if (-5 <= input) and (input < -1):
            return (0.25 * input) - 1.25
        elif (-1 <= input) and (input <= 0):
            return -0.25 * input
        else:
            return 0

    # stop := (-1, 0) (0, 1) (1, 0);
    def stop(self, input):
        if (-1 <= input) and (input < 0):
            return (1 * input) + 1
        elif (0 <= input) and (input <= 1):
            return (-1 * input) + 1
        else:
            return 0

    # right_slow := (0, 0) (1, 1) (5, 0);
    def right_slow(self, input):
        if (0 <= input) and (input < 1):
            return 1 * input
        elif (1 <= input) and (input <= 5):
            return (-1 * input) + 5
        else:
            return 0

    # right_fast := (2.5, 0) (5, 1);
    def right_fast(self, input):
        if (2.5 <= input) and (input <= 5):
            return (0.4 * input) - 1
        else:
            return 0
