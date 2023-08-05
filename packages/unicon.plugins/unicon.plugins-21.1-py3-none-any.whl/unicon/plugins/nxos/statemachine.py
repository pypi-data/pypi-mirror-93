from unicon.plugins.generic.statements import default_statement_list
from unicon.plugins.generic.statemachine import GenericSingleRpStateMachine
from unicon.plugins.generic.statemachine import GenericDualRpStateMachine
from unicon.plugins.nxos.patterns import NxosPatterns
from unicon.statemachine import State, Path


patterns = NxosPatterns()


def attach_module(state_machine, spawn, context):
    spawn.sendline('attach module %s' % context.get('_module_num', '1'))

def send_config_cmd(state_machine, spawn, context):
    cmd = 'config dual-stage' if context.get('config_dual') else 'config term'
    spawn.sendline(cmd)

class NxosSingleRpStateMachine(GenericSingleRpStateMachine):

    def create(self):
        enable = State('enable', patterns.enable_prompt)
        config = State('config', patterns.config_prompt)
        shell = State('shell', patterns.shell_prompt)
        loader = State('loader', patterns.loader_prompt)
        guestshell = State('guestshell', patterns.guestshell_prompt)
        module = State('module', patterns.module_prompt)
        module_elam = State('module_elam', patterns.module_elam_prompt)
        module_elam_insel = State('module_elam_insel', patterns.module_elam_insel_prompt)

        enable_to_config = Path(enable, config, send_config_cmd, None)
        config_to_enable = Path(config, enable, 'end', None)

        enable_to_shell = Path(enable, shell, 'run bash', None)
        shell_to_enable = Path(shell, enable, 'exit', None)

        enable_to_guestshell = Path(enable, guestshell, 'guestshell', None)
        guestshell_to_enable = Path(guestshell, enable, 'exit', None)

        enable_to_module = Path(enable, module, attach_module, None)
        module_to_enable = Path(module, enable, 'exit', None)
        module_elam_to_module = Path(module_elam, module, 'exit', None)
        module_elam_insel_to_module = Path(module_elam_insel, module_elam, 'exit', None)

        # Add State and Path to State Machine
        self.add_state(enable)
        self.add_state(config)
        self.add_state(shell)
        self.add_state(loader)
        self.add_state(guestshell)
        self.add_state(module)
        self.add_state(module_elam)
        self.add_state(module_elam_insel)

        self.add_path(enable_to_config)
        self.add_path(config_to_enable)
        self.add_path(enable_to_shell)
        self.add_path(shell_to_enable)
        self.add_path(enable_to_guestshell)
        self.add_path(guestshell_to_enable)
        self.add_path(enable_to_module)
        self.add_path(module_to_enable)
        self.add_path(module_elam_to_module)
        self.add_path(module_elam_insel_to_module)

        self.add_default_statements(default_statement_list)


class NxosDualRpStateMachine(NxosSingleRpStateMachine):
    def create(self):
        super().create()
