

def to_commands(op_base_type, parameters):
    para = []
    for i, e in enumerate(parameters):
        if isinstance(e, str):
            e = "'%s'" % e
        elif isinstance(e, float):
            e = '%.6g' % e
            if '.' not in e and 'e' not in e:
                e += '.0'
        para.append(str(e))
        if i > 40:  # avoid verbose print output
            break
    p_str = ', '.join(para)
    return 'opy.%s(%s)' % (op_base_type, p_str)


def _get_fn_name_and_args(line):
    import re
    fn_name = line.split('(')[0]
    args = re.search(r'\((.*?)\)', line).group(1)
    args = args.replace(' ', '')
    args = args.split(',')
    for i in range(len(args)):

        if "'" in args[i] or '"' in args[i]:
            pass
        #     args[i] = args[i][1:-1]
        elif '.' in args[i]:
            args[i] = float(args[i])
        else:
            try:
                args[i] = int(args[i])
            except ValueError:
                pass

    return fn_name, args


def check_if_opy_lines_consistent(line1, line2, line3=None):
    if line3 is None:
        if line1 == line2:
            return True
        fn1, args1 = _get_fn_name_and_args(line1)
        fn2, args2 = _get_fn_name_and_args(line2)
        if fn1 == fn2 and len(args1) == len(args2):
            for i in range(len(args1)):
                if args1[i] == args2[i]:
                    continue
                elif isinstance(args1[i], str) or isinstance(args2, str):
                    # consistent = 0  # since strings must be identical
                    return False
            return True
        else:
            return False
    else:
        if line1 == line2 and line1 == line3:
            return True
        fn1, args1 = _get_fn_name_and_args(line1)
        fn2, args2 = _get_fn_name_and_args(line2)
        fn3, args3 = _get_fn_name_and_args(line3)
        if fn1 == fn2 and fn1 == fn3 and len(args1) == len(args2) and len(args1) == len(args3):
            for i in range(len(args1)):
                if args1[i] == args2[i] and args1[i] == args3[i]:
                    continue
                elif isinstance(args1[i], str) or isinstance(args2[i], str) or isinstance(args3[i], str):
                    # consistent = 0  # since strings must be identical
                    return False
                else:
                    val1 = float(args1[i])
                    val2 = float(args2[i])
                    val3 = float(args3[i])
                    if val2 - val1 == val3 - val2:
                        continue
                    else:
                        return False
            return True
        else:
            return False


def _build_logic_formula(line1, line2):
    if line1 == line2:
        return line1
    fn1, args1 = _get_fn_name_and_args(line1)
    fn2, args2 = _get_fn_name_and_args(line2)
    new_args = list(args1)
    for i in range(len(args1)):
        if args1[i] == args2[i]:
            new_args[i] = str(args1[i])
        else:
            diff = args2[i] - args1[i]
            if diff < 0:
                new_args[i] = f'{args1[i]} {diff} * i'
            else:
                new_args[i] = f'{args1[i]} + {diff} * i'
    return f'{fn1}({", ".join(new_args)})'


def compress_opy_lines(commands):
    slines = 10  # search lines
    latest_rep = -1
    new_commands = []
    for i, com in enumerate(commands):
        if i < latest_rep:
            continue
        new_commands.append(com)
        dup_detected = 0
        for j in range(1, slines):
            if dup_detected or i + j >= len(commands) - 1:
                break
            if check_if_opy_lines_consistent(com, commands[i + j]):
                # check all lines in between are repeated
                consistent = 1
                for k in range(1, j):
                    if i + j + k >= len(commands):
                        consistent = 0
                        break
                    if not check_if_opy_lines_consistent(commands[i + k], commands[i + j + k]):
                        consistent = 0
                if consistent:
                    nr = 0
                    new_rep = i + nr * j
                    while consistent:
                        nr += 1
                        new_rep = i + nr * j
                        for k in range(j):
                            if new_rep + k >= len(commands):
                                consistent = 0
                            elif nr == 1:
                                if not check_if_opy_lines_consistent(commands[i + k], commands[new_rep + k]):
                                    consistent = 0
                                    break
                            else:
                                if not check_if_opy_lines_consistent(commands[i + (nr - 2) * j + k],
                                                                     commands[i + (nr - 1) * j + k],
                                                                     commands[i + nr * j + k]
                                                                     ):
                                    consistent = 0
                    if nr > 3:
                        dup_detected = 1
                        latest_rep = new_rep
                        new_commands[-1] = f'for i in range({nr}):'  # replace
                        for k in range(j):
                            new_command = _build_logic_formula(commands[i + k], commands[i + k + j])
                            new_commands.append('    ' + new_command)

    return new_commands


def to_py_file(osi, ofile='ofile.py', compress=True, w_analyze=False):
    if compress:
        commands = compress_opy_lines(osi.commands)
    else:
        commands = osi.commands
    pstr = 'import openseespy.opensees as opy\n' + '\n'.join(commands)
    if w_analyze:
        pstr += '\nopy.analyze(1, 0.1)\n'
    ofile = open(ofile, 'w')
    ofile.write(pstr)
    ofile.close()


def to_tcl_file(osi, ofile='ofile.tcl', w_analyze=False):
    # if compress:
    #     commands = compress_opy_lines(osi.commands)
    # else:
    commands = osi.commands
    pstr = '\n'.join(commands)
    if w_analyze:
        pstr += '\nopy.analyze(1, 0.1)\n'
    tcl_str = py2tcl(pstr)
    ofile = open(ofile, 'w')
    ofile.write(tcl_str)
    ofile.close()


def get_o3_kwargs_from_obj(obj, o3_obj, custom=None, overrides=None):
    from inspect import signature
    from collections import OrderedDict
    if custom is None:
        custom = {}
    if overrides is None:
        overrides = {}
    sig = signature(o3_obj)
    kwargs = OrderedDict()
    args = []
    sig_vals = sig.parameters.values()
    for p in sig_vals:
        if p.name in custom:
            pname = custom[p.name]
        else:
            pname = p.name
        if pname == 'osi':
            continue
        if pname in overrides:
            val = overrides[pname]
        else:
            try:
                val = getattr(obj, pname)
            except AttributeError as e:
                if p.default == p.empty:
                    raise AttributeError(e)
                else:
                    val = p.default
        if p.default == p.empty:
            args.append(val)
        else:
            if val is not None:
                kwargs[p.name] = val
    return args, kwargs


def has_o3_model_changed(cur_type, prev_type, cur_args, prev_args, cur_kwargs, prev_kwargs):
    import numpy as np
    changed = 0
    if cur_type != prev_type or len(cur_args) != len(prev_args) or len(cur_kwargs) != len(prev_kwargs):
        changed = 1
    else:
        for j, arg in enumerate(cur_args):
            if hasattr(arg, '__len__'):
                if len(arg) != len(prev_args[j]):
                    changed = 1
                    break
                for k, subarg in enumerate(arg):
                    if not np.isclose(subarg, prev_args[j][k]):
                        changed = 1
            elif not np.isclose(arg, prev_args[j]):
                changed = 1
                break
        for pm in cur_kwargs:
            if pm not in prev_kwargs:
                changed = 1
                break
            if hasattr(cur_kwargs[pm], '__len__'):
                if len(cur_kwargs[pm]) != len(prev_kwargs[pm]):
                    changed = 1
                    break
                for k, subarg in enumerate(cur_kwargs[pm]):
                    if not np.isclose(subarg, cur_kwargs[pm][k]):
                        changed = 1
                        break
            elif not np.isclose(cur_kwargs[pm], prev_kwargs[pm]):
                changed = 1
                break
    return changed


def py2tcl(pystr):
    """
    Converts openseespy script to tcl

    Returns
    -------

    """
    # new = '\n'.join(pystr.split()[1:])  # removes the import line
    new = pystr.replace('(', ' ')
    new = new.replace(')', ' ')
    new = new.replace('opy.', '')
    new = new.replace(',', '')
    new = new.replace("'", '')
    new = new.replace('"', '')
    # lines = new.splitlines()
    # for i in range(len(lines)):
    #     if 'for i in range(' in lines[i]:
    #         line = lines.replace('for i in range(', 'for {set i 1} {$i <= num} {incr i 1} {')
    return new


def gen_free_field_2d_bc(osi, eles, left_bc, bl_node=0, width=1, connection=None, base_fix_x=False, base_fix_y=True):
    import numpy as np
    from o3seespy import element
    from o3seespy import EqualDOF, Fix2DOFMulti
    from o3seespy import node
    # eles array_like of vertical quad like elements
    # bl_node is index of bottom-left node
    if left_bc:
        top_ind = 3
        bot_ind = 0
        sgn = -1
    else:
        top_ind = 2
        bot_ind = 1
        sgn = 1
    top_inds = np.array([3, 2])
    bot_inds = np.array([0, 1])  # TODO: depends on node order
    new_eles = []
    new_nodes = []
    for i, ele in enumerate(eles):
        if i == 0:
            top_line_nodes = np.array(ele.ele_nodes)[top_inds]
            new_nodes_line = []
            for nod in top_line_nodes:
                new_nodes_line.append(node.Node(osi, nod.x + sgn * width, nod.y))
            new_nodes.append(new_nodes_line)
            EqualDOF(osi, new_nodes[i][0], new_nodes[i][1], [1, 2])
            if connection is None:  # use rigid
                EqualDOF(osi, ele.ele_nodes[top_ind], new_nodes[i][0], [1, 2])
            # TODO: support uniaxial material based connections
        line_nodes = np.array(ele.ele_nodes)[bot_inds]

        new_nodes_line = []
        for nod in line_nodes:
            new_nodes_line.append(node.Node(osi, nod.x + sgn * width, nod.y))
        new_nodes.append(new_nodes_line)
        EqualDOF(osi, new_nodes[i][0], new_nodes[i][1], [1, 2])
        if connection is None:  # use rigid
            EqualDOF(osi, ele.ele_nodes[bot_ind], new_nodes[i][0], [1, 2])
        if isinstance(ele, element.SSPquad):
            ele_nodes = [new_nodes[i+1][0], new_nodes[i+1][1], new_nodes[i][1], new_nodes[i][0]]
            new_eles.append(element.SSPquad(osi, ele_nodes, ele.mat, ele.otype, ele.thick * 1e4,
                                            ele.b1, ele.b2))
        # TODO: support Quad
    if base_fix_x and base_fix_y:
        Fix2DOFMulti(osi, new_nodes[-1], [1, 2])
    elif base_fix_x:
        Fix2DOFMulti(osi, new_nodes[-1], x=1, y=0)
    else:
        Fix2DOFMulti(osi, new_nodes[-1], x=0, y=1)

