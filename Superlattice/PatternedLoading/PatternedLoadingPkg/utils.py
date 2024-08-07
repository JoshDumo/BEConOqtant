def RangeValidator(variable, variable_name, lower_lim, upper_lim):
    if (variable < lower_lim or variable > upper_lim) : # later use isclose for such comparisons
            raise ValueError(variable_name + " should be in the range [" + str(lower_lim) + ", " + str(upper_lim) + "]")  