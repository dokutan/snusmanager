# calculate missing values and check logical consistency using the z3 solver

from snus import Snus

def calculate_missing(snus: Snus):
    from z3 import Real, Solver, Or, sat

    # define variables
    nicotine_g = Real("nicotine_g")
    nicotine_portion = Real("nicotine_portion")
    portion_g = Real("portion_g")
    weight_g = Real("weight_g")
    portions = Real("portions")

    s = Solver()

    # constraints
    s.add(nicotine_portion == nicotine_g * portion_g)
    s.add(weight_g == portion_g * portions)
    s.add(nicotine_g >= 0)
    s.add(nicotine_portion >= 0)
    s.add(portion_g > 0)
    s.add(weight_g > 0)
    s.add(portions > 0)

    # known values
    if snus.nicotine_g: s.add(nicotine_g == snus.nicotine_g)
    if snus.nicotine_portion: s.add(nicotine_portion == snus.nicotine_portion)
    if snus.portion_g: s.add(portion_g == snus.portion_g)
    if snus.weight_g: s.add(weight_g == snus.weight_g)
    if snus.portions: s.add(portions == snus.portions)

    if s.check() == sat:
        m = s.model()
        solved_nicotine_g = m[nicotine_g]
        solved_nicotine_portion = m[nicotine_portion]
        solved_portion_g = m[portion_g]
        solved_weight_g = m[weight_g]
        solved_portions = m[portions]

        # check if the solution is unique
        s.add(Or(
            nicotine_g != m[nicotine_g],
            nicotine_portion != m[nicotine_portion],
            portion_g != m[portion_g],
            weight_g != m[weight_g],
            portions != m[portions],
        ))
        if s.check() == sat:
            return None

        snus.nicotine_g = float(solved_nicotine_g.as_fraction())
        snus.nicotine_portion = float(solved_nicotine_portion.as_fraction())
        snus.portion_g = float(solved_portion_g.as_fraction())
        snus.weight_g = float(solved_weight_g.as_fraction())
        snus.portions = float(solved_portions.as_fraction())
        return snus
    else:
        return None
