#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2023 https://github.com/Oops19
#


from typing import Set, Dict, Tuple, List

import services
from sim_cache.const.sim_cache_definition import SimCacheDefinition
from sim_cache.enums.local_occult_type import LocalOccultType
from sim_cache.modinfo import ModInfo
from sims.occult.occult_enums import OccultType
from sims.sim_info import SimInfo
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from sims4communitylib.events.zone_spin.events.zone_teardown import S4CLZoneTeardownEvent
from sims4communitylib.utils.common_log_registry import CommonLogRegistry, CommonLog
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from ts4lib.utils.singleton import Singleton

mod_name = ModInfo.get_identity().name
log: CommonLog = CommonLogRegistry.get().register_log(f"{ModInfo.get_identity().name}", ModInfo.get_identity().name)
log.enable()
log.info(f"Starting {mod_name}")


class SimCache(object, metaclass=Singleton):
    """
    This class allocates memory. The memory lightweight variant allocates it only temporarily.
    Use `set_memory_allocation(False)` if needed.
    """
    allocate_memory = True
    is_ready: bool = False
    _sim_ids: Set = set()  # Store all processed _sim_ids, also for pets etc.
    _sims: Dict = {}  # {sim_id: { sim_data }, ...}
    _sim_names: Dict = {}  # {'sim_name': sim_id, ...}
    _gender_females: Dict = {}  # {sim_id: 'sim_name', ...}
    _gender_males: Dict = {}  # {sim_id: 'sim_name', ...}
    _age_baby: Dict = {}  # {sim_id: 'sim_name', ...}
    _age_infant: Dict = {}  # {sim_id: 'sim_name', ...}
    _age_toddler: Dict = {}  # {sim_id: 'sim_name', ...}
    _age_child: Dict = {}  # {sim_id: 'sim_name', ...}
    _age_teen: Dict = {}  # {sim_id: 'sim_name', ...}
    _age_youngadult: Dict = {}  # {sim_id: 'sim_name', ...}
    _age_adult: Dict = {}  # {sim_id: 'sim_name', ...}
    _age_elder: Dict = {}  # {sim_id: 'sim_name', ...}
    _occult_human: Dict = {}
    _occult_alien: Dict = {}
    _occult_vampire: Dict = {}
    _occult_mermaid: Dict = {}
    _occult_witch: Dict = {}
    _occult_werewolf: Dict = {}
    _occult_ghost: Dict = {}
    _occult_robot: Dict = {}
    _occult_scarecrow: Dict = {}
    _occult_skeleton: Dict = {}
    _occult_plant_sim: Dict = {}

    def __init__(self):
        pass
    
    @property
    def sim_ids(self):
        return SimCache._sim_ids.copy()

    @property
    def sim_names(self):
        return SimCache._sim_names.copy()

    @property
    def sims(self):
        return SimCache._sims.copy()

    @property
    def gender_females(self):
        return SimCache._gender_females.copy()

    @property
    def gender_males(self):
        return SimCache._gender_males.copy()

    @property
    def gender_males(self):
        return SimCache._gender_males.copy()

    @property
    def age_baby(self):
        return SimCache._age_baby.copy()

    @property
    def age_infant(self):
        return SimCache._age_infant.copy()

    @property
    def age_toddler(self):
        return SimCache._age_toddler.copy()

    @property
    def age_child(self):
        return SimCache._age_child.copy()

    @property
    def age_teen(self):
        return SimCache._age_teen.copy()

    @property
    def age_youngadult(self):
        return SimCache._age_youngadult.copy()

    @property
    def age_adult(self):
        return SimCache._age_adult.copy()

    @property
    def age_elder(self):
        return SimCache._age_elder.copy()

    @property
    def occult_human(self):
        return SimCache._occult_human.copy()

    @property
    def occult_alien(self):
        return SimCache._occult_alien.copy()

    @property
    def occult_vampire(self):
        return SimCache._occult_vampire.copy()

    @property
    def occult_mermaid(self):
        return SimCache._occult_mermaid.copy()

    @property
    def occult_witch(self):
        return SimCache._occult_witch.copy()

    @property
    def occult_werewolf(self):
        return SimCache._occult_werewolf.copy()

    @property
    def occult_ghost(self):
        return SimCache._occult_ghost.copy()

    @property
    def occult_robot(self):
        return SimCache._occult_robot.copy()

    @property
    def occult_scarecrow(self):
        return SimCache._occult_scarecrow.copy()

    @property
    def occult_skeleton(self):
        return SimCache._occult_skeleton.copy()

    @property
    def occult_plant_sim(self):
        return SimCache._occult_plant_sim.copy()

    @classmethod
    def free_memory(cls):
        SimCache._sim_ids = set()  # Store all processed _sim_ids, also for pets etc.
        SimCache._sim_names = {}  # {'sim_name': sim_id, ...}
        SimCache._sims = {}  # {sim_id: { sim_data }, ...}
        SimCache._gender_females = {}  # {sim_id: 'sim_name', ...}
        SimCache._gender_males = {}
        SimCache._age_baby = {}
        SimCache._age_infant = {}
        SimCache._age_toddler = {}
        SimCache._age_child = {}
        SimCache._age_teen = {}
        SimCache._age_youngadult = {}
        SimCache._age_adult = {}
        SimCache._age_elder = {}
        SimCache._occult_human = {}
        SimCache._occult_alien = {}
        SimCache._occult_vampire = {}
        SimCache._occult_mermaid = {}
        SimCache._occult_witch = {}
        SimCache._occult_werewolf = {}
        SimCache._occult_ghost = {}
        SimCache._occult_robot = {}
        SimCache._occult_scarecrow = {}
        SimCache._occult_skeleton = {}
        SimCache._occult_plant_sim = {}
        SimCache.is_ready = False

    @classmethod
    def update_sim_ids(cls, force_refresh: bool = False):
        if force_refresh:
            cls.free_memory()
        elif SimCache.is_ready:
            return

        all_sim_ids = services.sim_info_manager().get_all()
        for sim_info in all_sim_ids:
            sim_id = 0
            name = ''
            try:
                gender = ''
                occult_types = set()
                sim_info: SimInfo = sim_info
                sim_id: int = sim_info.sim_id
                if not sim_id:
                    log.warn(f"Failed to get sim_id for sim_info: {sim_info}")
                    continue
                if sim_id in SimCache._sims:
                    continue
                SimCache._sim_ids.add(sim_id)
                name = search_name = f'unknown firstname{SimCacheDefinition.SIM_NAMES_SEP}unknown lastname'
                try:
                    f_name = CommonSimNameUtils.get_first_name(sim_info)
                    l_name = CommonSimNameUtils.get_last_name(sim_info)
                    name = f"{f_name}{SimCacheDefinition.SIM_NAMES_SEP}{l_name}"
                    search_name = name.lower()
                    SimCache._sim_names.update({search_name: sim_id})
                    SimCache._sims.update({sim_id: {
                        'name': name,
                        'search_name': search_name,
                    }})
                except Exception as e:
                    log.warn(f"Failed to get name for sim_id: {sim_id} ({e}")

                is_female = CommonGenderUtils.is_female(sim_info)
                if is_female:
                    SimCache._gender_females.update({sim_id: name})
                    gender = 'FEMALE'
                else:
                    is_male = CommonGenderUtils.is_male(sim_info)
                    if is_male:
                        SimCache._gender_males.update({sim_id: name})
                        gender = 'MALE'

                # Process the occults which are not handled by TS4 as occults:
                if CommonOccultUtils.is_ghost(sim_info):
                    SimCache._occult_ghost.update({sim_id: name})
                    occult_types.add('GHOST')
                if CommonOccultUtils.is_robot(sim_info):
                    SimCache._occult_robot.update({sim_id: name})
                    occult_types.add('ROBOT')
                if CommonOccultUtils.is_scarecrow(sim_info):
                    SimCache._occult_robot.update({sim_id: name})
                    occult_types.add('SCARECROW')
                if CommonOccultUtils.is_skeleton(sim_info):
                    SimCache._occult_robot.update({sim_id: name})
                    occult_types.add('SKELETON')
                if CommonOccultUtils.is_plant_sim(sim_info):
                    SimCache._occult_robot.update({sim_id: name})
                    occult_types.add('PLANT_SIM')
                if CommonOccultUtils.is_witch(sim_info):
                    SimCache._occult_robot.update({sim_id: name})

                # for occult_type in [e.name for e in LocalOccultType if (LocalOccultType.HUMAN.value <= e.value <= LocalOccultType.WEREWOLF.value)]:
                for e in [LocalOccultType.HUMAN, LocalOccultType.VAMPIRE, LocalOccultType.ALIEN, LocalOccultType.MERMAID, LocalOccultType.WITCH, LocalOccultType.HUMAN]:
                    occult_type = e.name
                    if CommonOccultUtils.has_occult_type(sim_info, OccultType[occult_type]):
                        occult_dict_name = f"_occult_{occult_type.lower()}"
                        occult_dict = getattr(SimCache, occult_dict_name)
                        occult_dict.update({sim_id: name})
                        setattr(SimCache, occult_dict_name, occult_dict)
                        occult_types.add(occult_type)

                age = ''
                try:
                    age: str = str(CommonAgeUtils.get_age(sim_info))
                    age = age.split('.')[1]  # everything behind 'Age.', e.g. TEEN
                    age_dict_name = f"_age_{age.lower()}"
                    age_dict = getattr(SimCache, age_dict_name)
                    age_dict.update({sim_id: name})
                    setattr(SimCache, age_dict_name, age_dict)
                except Exception as e:
                    log.warn(f"Could not handle age for sim_id: {sim_id} ({e}")

                SimCache._sims.update({sim_id: {
                    'name': name,
                    'search_name': search_name,
                    'gender': gender,
                    'age': age,
                    'occult_types': occult_types
                }})
                SimCache.is_ready = True

            except Exception as e:
                log.error(f"Failed to get data for sim_id: {sim_id} '{name}' ({e})", throw=True)

    @classmethod
    def set_memory_allocation(cls, allocate_memory: bool = True):
        """
        If disable set ot to True before calling multiple methods of this class.
        Set it to False afterwards to free memory
        :param allocate_memory: Whether to persist data in memory or not
        :return:
        """
        SimCache.allocate_memory = allocate_memory
        if SimCache.allocate_memory is True:
            # Initialize or update the cache
            cls.update_sim_ids(force_refresh=False)
        else:
            # Clear the cache
            cls._post_get_sim_ids()

    @classmethod
    def _pre_get_sim_ids(cls):
        if SimCache.allocate_memory is False:
            # Initialize the cache for this run
            cls.update_sim_ids(force_refresh=False)

    @classmethod
    def _post_get_sim_ids(cls):
        if SimCache.allocate_memory is False:
            cls.free_memory()

    @classmethod
    def get_sim_ids_by_occult_types(cls, occult_types: List[str]) -> Dict[int, str]:
        """
        Return 0-n _sims matching the specified IDs.
        :param occult_types: List with occult_types, eg ['HUMAN', ]
        :return: {sim_id: name, ...}
        """
        cls._pre_get_sim_ids()
        rv: Dict[int, str] = {}
        for occult_type in occult_types:
            try:
                occult_dict_name = f"_occult_{occult_type.lower()}"
                occult_dict = getattr(SimCache, occult_dict_name)
                rv = {**rv, **occult_dict}
            except Exception as e:
                log.warn(f"Oops: {e}")
        cls._post_get_sim_ids()
        return rv

    @classmethod
    def get_sim_ids_by_ages(cls, ages: List[str]) -> Dict[int, str]:
        """
        Return 0-n _sims matching the specified IDs.
        :param ages: List with ages, eg ['TEEN', ]
        :return: {sim_id: name, ...}
        """
        cls._pre_get_sim_ids()
        rv: Dict[int, str] = {}
        for age in ages:
            try:
                age_dict_name = f"_age_{age.lower()}"
                age_dict = getattr(SimCache, age_dict_name)
                log.debug(f"__sim_ids: {SimCache.sim_ids}")  # TODO _remove_
                log.debug(f"__age_dict: {age_dict_name} - {age_dict}")  # TODO _remove_
                rv = {**rv, **age_dict}
            except Exception as e:
                log.warn(f"Oops: {e}")
        cls._post_get_sim_ids()
        return rv

    @classmethod
    def get_sim_ids_by_ids(cls, sim_ids: List[int], return_missing: bool = False) -> Dict[int, str]:
        """
        Return 0-n _sims matching the specified IDs.
        :param sim_ids: List with IDs, eg [123, ]
        :param return_missing: Set to true to return also missing sims instead of skipping them.
        :return: {sim_id: name, ...}
        """
        cls._pre_get_sim_ids()
        rv: Dict[int, str] = {}
        for sim_id in sim_ids:
            sim_name = f'{sim_id}#{sim_id}'
            try:
                sim_name = SimCache._sims.get(sim_id).get('name')
            except Exception as e:
                log.warn(f"Oops: {e}")
            finally:
                if return_missing:
                    rv.update({sim_id: sim_name})
        cls._post_get_sim_ids()
        return rv

    @classmethod
    def get_sim_ids_by_gender(cls, gender_female: bool = True) -> Dict[int, str]:
        """
        Return 0-n _sims matching the specified gender.
        :param gender_female: True or False, defaults to True
        :return: {sim_id: name, ...}
        """
        cls._pre_get_sim_ids()
        if gender_female:
            rv = SimCache._gender_females.copy()
        else:
            rv = SimCache._gender_males.copy()
        cls._post_get_sim_ids()
        return rv

    @classmethod
    def get_sim_ids_by_sim_name(cls, sim_name: str = SimCacheDefinition.SIM_NAMES_SEP) -> Dict[int, str]:
        """
        Return 0-n _sims matching the specified name.
        Equals, startswith, endswith and contains tests are performed.
        'bella#goth' will likely find one sim named 'Bella#Goth'.
        'be#g' may find a sim named 'Be#G' or 'Bella#Goth', 'Ben#Gur', ... as the fist char(s) match.
        'a#h' may fina a sim named 'A#H' or 'Ann#Hur', ... or 'Bella#Goth', ... as the last char(s) matches.
        'll#ot' may find 'Bella#Goth' as the chars are contained in the name.
        :param sim_name: Full or partial sim name with '#' to separate first and last name. Default is '#' so all _sims are returned.
        :return: {sim_id: name, ...}
        """
        cls._pre_get_sim_ids()
        if not sim_name:
            sim_name = f"{sim_name}#"
        short_first_name, short_last_name = sim_name.lower().split(SimCacheDefinition.SIM_NAMES_SEP, 1)
        equals_match: Dict[int, str] = {}
        starts_match: Dict[int, str] = {}
        ends_match: Dict[int, str] = {}
        contains_match: Dict[int, str] = {}
        for sim_id, sim_data in SimCache._sims.items():
            _sim_search_name = sim_data.get('search_name')  # name is in lower case
            _sim_name = sim_data.get('name')
            # log.debug(f"_sim_search_name{_sim_search_name} _sim_name{_sim_name}")
            _first_name, _last_name = _sim_search_name.split(SimCacheDefinition.SIM_NAMES_SEP, 1)
            if (_first_name == short_first_name) and (_last_name == short_last_name):
                equals_match.update({sim_id: _sim_name})
            elif _first_name.startswith(short_first_name) and _last_name.startswith(short_last_name):
                starts_match.update({sim_id: _sim_name})
            elif _first_name.endswith(short_first_name) and _last_name.endswith(short_last_name):
                ends_match.update({sim_id: _sim_name})
            elif short_first_name in _first_name and short_last_name in _last_name:
                contains_match.update({sim_id: _sim_name})

        cls._post_get_sim_ids()
        if equals_match:
            return equals_match
        elif starts_match:
            return starts_match
        elif ends_match:
            return ends_match
        else:
            return contains_match

    @classmethod
    def get_sim_ids_by_sim_name_advanced(cls, sim_name: str = SimCacheDefinition.SIM_NAMES_SEP) -> Tuple[Dict[int, str], Dict[int, str], Dict[int, str], Dict[int, str]]:
        """
        Return 0-n _sims matching the specified name.
        Equals, startswith, endswith and contains tests are performed.
        'bella#goth' will likely find one sim named 'Bella#Goth'.
        'be#g' may find a sim named 'Be#G' or 'Bella#Goth', 'Ben#Gur', ... as the fist char(s) match.
        'a#h' may fina a sim named 'A#H' or 'Ann#Hur', ... or 'Bella#Goth', ... as the last char(s) matches.
        'll#ot' may find 'Bella#Goth' as the chars are contained in the name.
        :param sim_name: Full or partial sim name with '#' to separate first and last name.
        :return: Tuple with 4 values exact, starts, ends, contains, each with: {sim_id: name, ...}
        """
        cls._pre_get_sim_ids()
        if not sim_name:
            sim_name = f"{sim_name}#"
        short_first_name, short_last_name = sim_name.lower().split(SimCacheDefinition.SIM_NAMES_SEP, 1)
        equals_match: Dict[int, str] = {}
        starts_match: Dict[int, str] = {}
        ends_match: Dict[int, str] = {}
        contains_match: Dict[int, str] = {}
        for sim_id, sim_data in SimCache._sims.items():
            _sim_search_name = sim_data.get('search_name')  # name is in lower case
            _sim_name = sim_data.get('name')
            _first_name, _last_name = _sim_search_name.split(SimCacheDefinition.SIM_NAMES_SEP, 1)
            if (_first_name == short_first_name) and (_last_name == short_last_name):
                equals_match.update({sim_id: _sim_name})
                # Skip the other tests in this case. They would all match.
                continue
            if _first_name.startswith(short_first_name) and _last_name.startswith(short_last_name):
                starts_match.update({sim_id: _sim_name})
            if _first_name.endswith(short_first_name) and _last_name.endswith(short_last_name):
                ends_match.update({sim_id: _sim_name})
            if short_first_name in _first_name and short_last_name in _last_name:
                contains_match.update({sim_id: _sim_name})

        cls._post_get_sim_ids()
        # More detailed results
        return equals_match, starts_match, ends_match, contains_match

    '''
    Deprecated, use get_sim_ids_by_occult_typeS and  get_sim_ids_by_ageS instead and supply one or more entries in a list()
    @classmethod
    def get_sim_ids_by_occult_type(cls, occult_type: str) -> Dict[int, str]:
        """
        Return 0-n _sims matching the specified IDs.
        :param occult_type: String with occult_type, eg ['HUMAN', ]
        :return: {sim_id: name, ...}
        """
        cls._pre_get_sim_ids()
        rv: Dict[int, str] = {}
        try:
            occult_dict_name = f"_occult_{occult_type.lower()}"
            occult_dict = getattr(SimCache, occult_dict_name)
            rv = {**rv, **occult_dict}
        except Exception as e:
            log.warn(f"Oops: {e}")
        cls._post_get_sim_ids()
        return rv

    @classmethod
    def get_sim_ids_by_age(cls, age: str) -> Dict[int, str]:
        """
        Return 0-n _sims matching the specified age.
        :param age: Age string like TEEN, ...
        :return: {sim_id: name, ...}
        """
        cls._pre_get_sim_ids()
        rv: Dict[int, str] = {}
        for sim_id, sim_data in SimCache._sims.items():
            if sim_data.get('age', None) == age:
                _sim_name = sim_data.get('name')
                rv.update({sim_id: _sim_name})
        cls._post_get_sim_ids()
        return rv
    '''


# noinspection PyUnusedLocal
@CommonEventRegistry.handle_events('o19.sim_selector')
def zone_loaded(event_data: S4CLZoneLateLoadEvent):
    try:
        log.debug(f"Updating cache")  # Should happen every time the users travels to a new lot or leaves CAS.
        sc = SimCache()
        sc.update_sim_ids()
        SimCache.is_ready = False
    except Exception as e:
        log.warn(f"Failed to cache _sims ({e}")


# noinspection PyUnusedLocal
@CommonEventRegistry.handle_events(ModInfo.get_identity().name)
def handle_event(event_data: S4CLZoneTeardownEvent):
    log.debug(f"Invalidating cache")
    # Set is_ready to force a refresh when entering a lot.
    SimCache.is_ready = False
