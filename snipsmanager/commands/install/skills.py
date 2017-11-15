# -*-: coding utf-8 -*-

import os

from ..base import Base
from ...utils.pip_installer import PipInstaller
from ...utils.os_helpers import file_exists
from ...utils.snipsfile import Snipsfile
from .skill import SkillInstaller, SkillInstallerWarning

from ... import DEFAULT_SNIPSFILE_PATH

from snipsmanagercore import pretty_printer as pp

class SkillsInstallerException(Exception):
    pass

class SkillsInstallerWarning(Exception):
    pass


class SkillsInstaller(Base):
    
    def run(self):
        try:
            SkillsInstaller.install(snipsfile_path=self.options['--snipsfile'], silent=self.options['--silent'], force_download=self.options['--force-download'])
        except SkillsInstallerWarning as e:
            pp.pwarning(str(e))
        except Exception as e:
            pp.perror(str(e))


    @staticmethod
    def install(snipsfile_path=None, silent=False, force_download=False):
        SkillsInstaller.print_start(silent)
        if snipsfile_path is None:
            snipsfile_path = DEFAULT_SNIPSFILE_PATH
        if snipsfile_path is not None and not file_exists(snipsfile_path):
            raise SkillsInstallerException("Error installing skills: Snipsfile not found")
        snipsfile = Snipsfile(snipsfile_path)
        num_installed = SkillsInstaller.install_from_snipsfile(snipsfile, silent=True, force_download=force_download)
        SkillsInstaller.print_done(num_installed, silent)


    @staticmethod
    def install_from_snipsfile(snipsfile, silent=False, force_download=False):
        SkillsInstaller.print_start(silent)
        if snipsfile is None:
            raise SkillsInstallerException("Error installing skills: no Snipsfile provided")
        skill_urls = snipsfile.get_skill_urls()
        num_skills_without_url = snipsfile.get_num_skills_without_url()
        if len(skill_urls) + num_skills_without_url == 0:
            raise SkillsInstallerWarning("No skills found in Snipsfile. Skipping skill installation")
        num_installed = SkillsInstaller.install_from_urls(skill_urls, silent=True, force_download=force_download)
        SkillsInstaller.print_done(num_installed + num_skills_without_url, silent)
        return num_installed + num_skills_without_url


    @staticmethod
    def install_from_urls(skill_urls, silent=False, force_download=False):
        SkillsInstaller.print_start(silent)
        num_installed = 0
        for url in skill_urls:
            try:
                SkillInstaller.install(url, force_download=force_download)
                num_installed = num_installed + 1
            except SkillInstallerWarning as e:
                pp.pwarning(str(e))
            except Exception as e:
                pp.perror(str(e))
        SkillsInstaller.print_done(num_installed, silent)
        return num_installed


    @staticmethod
    def print_start(silent=False):
        if not silent:
            pp.pcommand("Installing skills")


    @staticmethod
    def print_done(num_installed, silent=False):
        if not silent:
            if num_installed == 1:
                pp.psuccess("Successfully installed 1 skill")
            else:
                pp.psuccess("Successfully installed {} skills".format(num_installed))
