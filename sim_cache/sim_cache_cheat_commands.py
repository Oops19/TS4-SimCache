#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2023 https://github.com/Oops19
#


from sim_cache.const.sim_cache_definition import SimCacheDefinition
from sim_cache.modinfo import ModInfo
from sim_cache.sim_cache import SimCache

from sims4communitylib.services.commands.common_console_command import CommonConsoleCommandArgument, CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_log_registry import CommonLogRegistry, CommonLog


mod_name = ModInfo.get_identity().name
log: CommonLog = CommonLogRegistry.get().register_log(f"{ModInfo.get_identity().name}", ModInfo.get_identity().name)
log.enable()


class SimCacheCheatCommands:

    @staticmethod
    @CommonConsoleCommand(ModInfo.get_identity(), 'o19.sc.init', 'Refresh the cache.', )
    def o19_sc_refresh(output: CommonConsoleCommandOutput):
        try:
            sc = SimCache()
            output(f"Purging cache ...")
            sc.update_sim_ids(force_refresh=True)
            output(f"Cache has been rebuilt.")
        except Exception as e:
            output(f"Oops: {e}")
            log.error(f"Oops: {e}", throw=True)

    @staticmethod
    @CommonConsoleCommand(ModInfo.get_identity(), 'o19.sc.dump', 'Dump all data to the log file.', )
    def o19_sc_refresh(output: CommonConsoleCommandOutput):
        try:
            output(f"Dumping cache ...")
            sc = SimCache()
            log.debug(f"{sc.sims}")
            log.debug(f"age_teen {sc.age_teen}")
            output(f"OK")
        except Exception as e:
            output(f"Oops: {e}")
            log.error(f"Oops: {e}", throw=True)


    @staticmethod
    @CommonConsoleCommand(ModInfo.get_identity(), 'o19.sc.search', 'Search sims.',
                          command_arguments=(
                                  CommonConsoleCommandArgument('sim_name', 'Sim Id or Name', 'The name, search string or decimal identifier of the Sim.', is_optional=False),
                          )
                          )
    def o19_sc_search_sim(output: CommonConsoleCommandOutput, sim_name: str):
        try:
            output(f"Searching '{sim_name}'")
            sc = SimCache()

            if SimCacheDefinition.SIM_NAMES_SEP not in sim_name:
                # it could be a sim_id
                if sim_name.startswith('0x'):
                    sim_id = int(sim_name, 16)
                elif isinstance(sim_name, int):
                    sim_id = int(sim_name)
                else:
                    output(f"Can't convert '{sim_name}' to a number. To search for a name use '{SimCacheDefinition.SIM_NAMES_SEP}' to separate first and last name parts.")
                    return
                sims = sc.get_sim_ids_by_ids([sim_id, ])
                output(f"Found: '{sims}'")
                return

            equals, starts, ends, contains = sc.get_sim_ids_by_sim_name_advanced(sim_name)
            output(f"Found {len(contains)} contains: '{contains}'")
            output(f"Found {len(ends)} ends: '{ends}'")
            output(f"Found {len(starts)} starts: '{starts}'")
            output(f"Found {len(equals)} equals: '{equals}'")
        except Exception as e:
            output(f"Oops: {e}")
            log.error(f"Oops: {e}", throw=True)





