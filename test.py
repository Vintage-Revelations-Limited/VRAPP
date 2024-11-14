import compare
import numpy as np
import employee as e
is_in_time = compare.fuzzy_time_check(10.45, 11.44, 1)

not_in_time = compare.fuzzy_time_check(10.45, 22.45, 1)

print(is_in_time)
print(not_in_time)


in_mins = 1.13

in_hours = compare.convert_to_hours_value(in_mins)

print(in_hours)