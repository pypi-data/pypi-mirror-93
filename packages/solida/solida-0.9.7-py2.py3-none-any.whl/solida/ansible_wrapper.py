import os.path
from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager as Inventory
from ansible.executor.playbook_executor import PlaybookExecutor

from solida import cache_dir


class AnsibleWrapper(object):
    """

    """
    def __init__(self, host, remote_user, connection, pipeline, profile,
                 playbooks_path='playbooks'):
        def set_extra_vars(pipeline=None, profile=None):
            extra_vars = dict()
            if pipeline:
                extra_vars['pipeline_label'] = pipeline['label']
                extra_vars['pipeline_url'] = pipeline['url']
                extra_vars['pipeline_cache_path'] = os.path.join(cache_dir,
                                                                 pipeline['label'])
            if profile:
                for k, v in profile.items():
                    extra_vars[k] = v

            return extra_vars

        loader = DataLoader()

        Options = namedtuple('Options',
                             ['connection', 'forks', 'remote_user', 'become',
                              'become_method', 'become_user', 'diff', 'check',
                              'listhosts', 'listtasks', 'listtags', 'syntax',
                              'module_path'])
        options = Options(connection=connection, forks=100, remote_user=remote_user,
                          become=None, become_method=None, become_user=None,
                          diff=False, check=False, listhosts=False,
                          listtasks=False, listtags=False, syntax=False,
                          module_path="")

        passwords = dict()

        inventory = Inventory(loader=loader, sources="{},".format(host))
        variable_manager = VariableManager(loader=loader, inventory=inventory)

        here = os.path.abspath(os.path.dirname(__file__))
        playbook_list = [os.path.join(here, playbooks_path,
                                      pipeline['playbook'])]

        variable_manager.extra_vars = set_extra_vars(pipeline=pipeline,
                                                     profile=profile)

        self.pbex = PlaybookExecutor(playbooks=playbook_list,
                                     inventory=inventory,
                                     variable_manager=variable_manager,
                                     loader=loader,
                                     options=options,
                                     passwords=passwords)

    def run(self):
        return self.pbex.run()
