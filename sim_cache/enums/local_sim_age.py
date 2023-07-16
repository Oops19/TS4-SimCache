#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2023 https://github.com/Oops19
#


from ts4lib.common_enums.enum_types.common_enum import CommonEnum


class LocalSimAge(CommonEnum):
    NONE = 0
    BABY = 2 ** 0
    INFANT = 2 ** 1  # EA defines this as 128
    TODDLER = 2 ** 2  # EA defines this as 2, etc.
    CHILD = 2 ** 3
    TEEN = 2 ** 4
    YOUNGADULT = 2 ** 5  # EA name
    YOUNG_ADULT = 2 ** 5  # S4CL name, here not used
    ADULT = 2 ** 6
    ELDER = 2 ** 7
