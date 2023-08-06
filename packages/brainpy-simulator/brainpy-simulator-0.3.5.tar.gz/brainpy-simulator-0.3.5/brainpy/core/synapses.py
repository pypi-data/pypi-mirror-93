# -*- coding: utf-8 -*-

import re

import numpy as np

from . import base
from . import constants
from . import neurons
from .. import connectivity
from .. import errors
from .. import profile
from .. import tools

__all__ = [
    'SynType',
    'SynConn',
    'delayed',
]

_SYN_CONN_NO = 0


class SynType(base.ObjType):
    """Abstract Synapse Type.

    It can be defined based on a collection of synapses or a single synapse model.
    """

    def __init__(self, name, ST, steps, mode='vector', requires=None, hand_overs=None, ):
        if mode not in [constants.SCALAR_MODE, constants.VECTOR_MODE, constants.MATRIX_MODE]:
            raise errors.ModelDefError('SynType only support "scalar", "vector" or "matrix".')

        super(SynType, self).__init__(
            ST=ST,
            requires=requires,
            steps=steps,
            name=name,
            mode=mode,
            hand_overs=hand_overs)

        # inspect delay keys
        # ------------------

        # delay function
        delay_funcs = []
        for func in self.steps:
            if func.__name__.startswith('_brainpy_delayed_'):
                delay_funcs.append(func)
        if len(delay_funcs):
            delay_func_code = '\n'.join([tools.deindent(tools.get_main_code(func)) for func in delay_funcs])
            delay_func_code_left = '\n'.join(tools.format_code(delay_func_code).lefts)

            # get delayed variables
            _delay_keys = set()
            delay_keys_in_left = set(re.findall(r'ST\[[\'"](\w+)[\'"]\]', delay_func_code_left))
            if len(delay_keys_in_left) > 0:
                raise errors.ModelDefError(f'Delayed function cannot assign value to "ST".')
            delay_keys = set(re.findall(r'ST\[[\'"](\w+)[\'"]\]', delay_func_code))
            if len(delay_keys) > 0:
                _delay_keys.update(delay_keys)
            self._delay_keys = list(_delay_keys)


class SynConn(base.Ensemble):
    """Synaptic connections.

    Parameters
    ----------
    model : SynType
        The instantiated neuron type model.
    pars_update : dict
        Parameters to update.
    pre_group : neurons.NeuGroup, neurons.NeuSubGroup
        Pre-synaptic neuron group.
    post_group : neurons.NeuGroup, neurons.NeuSubGroup
        Post-synaptic neuron group.
    conn : connectivity.Connector
        Connection method to create synaptic connectivity.
    num : int
        The number of the synapses.
    delay : float
        The time of the synaptic delay.
    monitors : list, tuple
        Variables to monitor.
    name : str
        The name of the neuron group.
    """

    def __init__(self, model, pre_group=None, post_group=None, conn=None, delay=0.,
                 name=None, monitors=None, satisfies=None, pars_update=None, ):
        # name
        # ----
        if name is None:
            global _SYN_CONN_NO
            name = f'SynConn{_SYN_CONN_NO}'
            _SYN_CONN_NO += 1
        else:
            name = name

        # model
        # ------
        if not isinstance(model, SynType):
            raise errors.ModelUseError(f'{type(self).__name__} receives an instance of {SynType.__name__}, '
                                       f'not {type(model).__name__}.')

        if model.mode == 'scalar':
            if pre_group is None or post_group is None:
                raise errors.ModelUseError('Using scalar-based synapse model must '
                                           'provide "pre_group" and "post_group".')

        # pre or post neuron group
        # ------------------------
        self.pre_group = pre_group
        self.post_group = post_group
        self.conn = None
        num = 1
        if pre_group is not None and post_group is not None:
            # check
            # ------
            if not isinstance(pre_group, (neurons.NeuGroup, neurons.NeuSubGroup)):
                raise errors.ModelUseError('"pre_group" must be an instance of NeuGroup/NeuSubGroup.')
            if not isinstance(post_group, (neurons.NeuGroup, neurons.NeuSubGroup)):
                raise errors.ModelUseError('"post_group" must be an instance of NeuGroup/NeuSubGroup.')

            # pre and post synaptic state
            self.pre = pre_group.ST
            self.post = post_group.ST

            if conn is not None:
                # connections
                # ------------
                if isinstance(conn, connectivity.Connector):
                    self.conn = conn
                    self.conn(pre_group.indices, post_group.indices)
                else:
                    if isinstance(conn, np.ndarray):
                        # check matrix dimension
                        if np.ndim(conn) != 2:
                            raise errors.ModelUseError(f'"conn" must be a 2D array, not {np.ndim(conn)}D.')
                        # check matrix shape
                        conn_shape = np.shape(conn)
                        if not (conn_shape[0] == pre_group.num and conn_shape[1] == post_group.num):
                            raise errors.ModelUseError(
                                f'The shape of "conn" must be ({pre_group.num}, {post_group.num})')
                        # get pre_ids and post_ids
                        pre_ids, post_ids = np.where(conn > 0)
                    else:
                        # check conn type
                        if not isinstance(conn, dict):
                            raise errors.ModelUseError(f'"conn" only support "dict", 2D ndarray, '
                                                       f'or instance of bp.connect.Connector.')
                        # check conn content
                        if not ('i' in conn and 'j' in conn):
                            raise errors.ModelUseError('When provided "conn" is a dict, "i" and "j" must in "conn".')
                        # get pre_ids and post_ids
                        pre_ids = np.asarray(conn['i'], dtype=np.int_)
                        post_ids = np.asarray(conn['j'], dtype=np.int_)
                    self.conn = connectivity.Connector()
                    self.conn.pre_ids = pre_group.indices.flatten()[pre_ids]
                    self.conn.post_ids = post_group.indices.flatten()[post_ids]

                # get synaptic structures
                self.conn.set_size(num_post=post_group.size, num_pre=pre_group.size)
                if model.mode == constants.SCALAR_MODE:
                    self.conn.set_requires(model.step_args + ['post2syn', 'pre2syn'])
                else:
                    self.conn.set_requires(model.step_args)
                for k in self.conn.requires:
                    setattr(self, k, getattr(self.conn, k))
                self.pre_ids = self.conn.pre_ids
                self.post_ids = self.conn.post_ids
                num = len(self.pre_ids)

        if satisfies is not None and 'num' in satisfies:
            num = satisfies['num']

        try:
            assert 0 < num < 2 ** 64
        except AssertionError:
            raise errors.ModelUseError('Total synapse number "num" must be a valid number in "uint64".')

        # initialize
        # ----------
        super(SynConn, self).__init__(model=model,
                                      pars_update=pars_update,
                                      name=name,
                                      num=num,
                                      monitors=monitors,
                                      cls_type=constants.SYN_CONN_TYPE,
                                      satisfies=satisfies)

        # delay
        # -------
        if delay is None:
            delay_len = 1
        elif isinstance(delay, (int, float)):
            dt = profile.get_dt()
            delay_len = int(np.ceil(delay / dt))
            if delay_len == 0:
                delay_len = 1
        else:
            raise ValueError("BrainPy currently doesn't support other kinds of delay.")
        self.delay_len = delay_len  # delay length

        # ST
        # --
        if self.model.mode == constants.MATRIX_MODE:
            if pre_group is None:
                if 'pre_size' not in satisfies:
                    raise errors.ModelUseError('"pre_size" must be provided in "satisfies" when "pre_group" is none.')
                pre_size = satisfies['pre_size']
            else:
                pre_size = pre_group.size

            if post_group is None:
                if 'post_size' not in satisfies:
                    raise errors.ModelUseError('"post_size" must be provided in "satisfies" when "post_group" is none.')
                post_size = satisfies['post_size']
            else:
                post_size = post_group.size
            size = (pre_size, post_size)
        else:
            size = (self.num,)
        self.ST = self.model.ST.make_copy(size=size,
                                          delay=delay_len,
                                          delay_vars=self.model._delay_keys)


def delayed(func):
    """Decorator for synapse delay.

    Parameters
    ----------
    func : callable
        The step function which use delayed synapse state.

    Returns
    -------
    func : callable
        The modified step function.
    """
    func.__name__ = f'_brainpy_delayed_{func.__name__}'
    return func
