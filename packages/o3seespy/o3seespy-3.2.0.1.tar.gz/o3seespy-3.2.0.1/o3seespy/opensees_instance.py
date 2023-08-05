try:
    from custom_openseespy import custom_opensees as opy
except ModuleNotFoundError:
    import openseespy.opensees as opy
from collections import OrderedDict
from . import exceptions, extensions


class OpenSeesInstance(object):

    def __init__(self, ndm: int, ndf=None, state=0, mp=False, nnpp=10000):
        init_tag = 0
        if mp:
            pid = opy.getPID()
            init_tag = pid * nnpp
        self.mp = mp
        self.n_node = init_tag
        self.n_con = init_tag
        self.n_ele = init_tag
        self.n_mat = init_tag
        self.n_sect = init_tag
        self.n_tseries = init_tag
        self.n_pat = init_tag
        self.n_fix = init_tag
        self.n_integ = init_tag
        self.n_transformation = init_tag
        self.n_region = init_tag
        self.n_params = init_tag
        self.n_mesh = init_tag
        self.ndm = ndm
        self._state = state  # 0=execute line by line, 1=export to raw openseespy, 2=export reloadable json
        parameters = ['BasicBuilder', '-ndm', ndm]
        if ndf is not None:
            if ndf not in [1, 2, 3, 4, 6]:
                raise ValueError('ndm must be: 1, 2, 3, 4, 6')
            self.ndf = int(ndf)
            parameters += ['-ndf', self.ndf]
        else:
            if ndm == 1:
                self.ndf = 1
            elif ndm == 2:
                self.ndf = 3
            else:
                self.ndf = 6
        opy.wipe()
        opy.model(*parameters)
        self.commands = []
        self.dict = OrderedDict()

        if state == 1:
            self.commands.append('opy.wipe()')
            self.commands.append(f"opy.model('basic', '-ndm', {ndm}, '-ndf', {self.ndf})")
        if state == 2:
            self.dict['ndm'] = ndm
            self.dict['ndf'] = ndf
            # base_types = ['node', 'element', 'section', 'uniaxial_material']
        elif state == 3:
            self.commands.append('opy.wipe()')
            self.commands.append(f"opy.model('basic', '-ndm', {ndm}, '-ndf', {self.ndf})")

    def reset_model_params(self, ndm, ndf):
        opy.model('BasicBuilder', '-ndm', ndm, '-ndf', ndf)
        self.ndm = ndm
        self.ndf = ndf
        if self._state == 1:
            self.commands.append(f"opy.model('basic', '-ndm', {ndm}, '-ndf', {ndf})")
        if self._state == 2:
            self.dict['ndm'] = ndm
            self.dict['ndf'] = ndf
            # base_types = ['node', 'element', 'section', 'uniaxial_material']
        elif self._state == 3:
            self.commands.append(f"opy.model('basic', '-ndm', {ndm}, '-ndf', {ndf})")

    def to_commands(self, os_command):
        self.commands.append(os_command)

    def to_dict(self, os_model, export_none=False):
        if os_model.op_type not in self.dict:
            self.dict[os_model.op_type] = OrderedDict()
        self.dict[os_model.op_type][os_model.tag] = os_model.to_dict(export_none=export_none)

    def to_process(self, op_base_type, parameters):
        if self.state == 0:
            return self.to_opensees(op_base_type, parameters)
        # if self.state == 1:
        #     self.to_commands(extensions.to_commands(op_base_type, parameters))
        # elif self.state == 2:
        #     self.to_dict(self)
        #     return self.to_opensees(op_base_type, parameters)
        elif self.state == 3:
            self.to_commands(extensions.to_commands(op_base_type, parameters))
            return self.to_opensees(op_base_type, parameters)

    def to_opensees(self, op_base_type, parameters):
        try:
            try:
                return getattr(opy, op_base_type)(*parameters)
            except opy.OpenSeesError as e:
                raise ValueError('opensees.{0}({1}) caused error "{2}"'.format(op_base_type,
                                                                               ','.join(str(x) for x in parameters), e))

        except SystemError as e:
            if None in parameters:
                print(parameters)
                raise exceptions.ModelError("%s of type: %s contains 'None'" % (op_base_type))
            else:
                raise SystemError(e)
        except AttributeError as e:
            print(e)
            print('opensees.{0}({1}) caused error "{2}"'.format(op_base_type,
                                                                               ','.join(str(x) for x in parameters),
                                                                                        e))
            raise exceptions.ModelError("op_base_type: '%s' does not exist in opensees module" % op_base_type)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value


class OpenseesInstance(OpenSeesInstance):
    def __init__(self, ndm: int, ndf=None, state=0):
        print('Please use OpenSeesInstance instead of OpenseesInstance')
        super(OpenseesInstance, self).__init__(ndm, ndf, state)


class _OpenSeesInstanceTestMP(OpenSeesInstance):
    def __init__(self, ndm: int, ndf=None, state=0, mp=False, nnpp=10000, pid=None):
        init_tag = 0
        if mp:
            if pid is None:
                pid = opy.getPID()
            init_tag = pid * nnpp
        self.mp = mp
        self.n_node = init_tag
        self.n_con = init_tag
        self.n_ele = init_tag
        self.n_mat = init_tag
        self.n_sect = init_tag
        self.n_tseries = init_tag
        self.n_pat = init_tag
        self.n_fix = init_tag
        self.n_integ = init_tag
        self.n_transformation = init_tag
        self.n_region = init_tag
        self.n_params = init_tag
        self.n_mesh = init_tag
        self.ndm = ndm
        self._state = state  # 0=execute line by line, 1=export to raw openseespy, 2=export reloadable json
        parameters = ['BasicBuilder', '-ndm', ndm]
        if ndf is not None:
            if ndf not in [1, 2, 3, 6]:
                raise ValueError('ndm must be: 1, 2, 3, 6')
            self.ndf = int(ndf)
            parameters += ['-ndf', self.ndf]
        else:
            if ndm == 1:
                self.ndf = 1
            elif ndm == 2:
                self.ndf = 3
            else:
                self.ndf = 6
        opy.wipe()
        opy.model(*parameters)
        self.commands = []
        self.dict = OrderedDict()

        if state == 1:
            self.commands.append('opy.wipe()')
            self.commands.append(f"opy.model('basic', '-ndm', {ndm}, '-ndf', {self.ndf})")
        if state == 2:
            self.dict['ndm'] = ndm
            self.dict['ndf'] = ndf
            # base_types = ['node', 'element', 'section', 'uniaxial_material']
        elif state == 3:
            self.commands.append('opy.wipe()')
            self.commands.append(f"opy.model('basic', '-ndm', {ndm}, '-ndf', {self.ndf})")
