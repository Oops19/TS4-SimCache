#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2023 https://github.com/Oops19
#


from ts4lib.common_enums.enum_types.common_enum import CommonEnum


class LocalOccultType(CommonEnum):
    NONE = 0
    HUMAN = 2 ** 10
    VAMPIRE = 2 ** 11
    ALIEN = 2 ** 12
    MERMAID = 2 ** 13
    WITCH = 2 ** 14
    WEREWOLF = 2 ** 15
    # Future use = 2 ** 16
    # Future use = 2 ** 17
    # Future use = 2 ** 18
    # These are not TS4 occults
    GHOST = 2 ** 19
    ROBOT = 2 ** 20
    SCARECROW = 2 ** 21
    SKELETON = 2 ** 22
    PLANT_SIM = 2 ** 23
