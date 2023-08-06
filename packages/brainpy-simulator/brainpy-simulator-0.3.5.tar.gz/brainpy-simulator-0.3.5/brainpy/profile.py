# -*- coding: utf-8 -*-

"""
The setting of the overall framework by ``profile.py`` API.
"""

from numba import cuda

__all__ = [
    'set',

    'run_on_cpu',
    'run_on_gpu',

    'set_backend',
    'get_backend',

    'set_device',
    'get_device',

    'set_dt',
    'get_dt',

    'set_numerical_method',
    'get_numerical_method',

    'set_numba_profile',
    'get_numba_profile',

    'get_num_thread_gpu',

    'is_jit',
    'is_merge_integrators',
    'is_merge_steps',
    'is_substitute_equation',
    'show_code_scope',
    'show_format_code',
]

_jit = False
_backend = 'numpy'
_device = 'cpu'
_dt = 0.1
_method = 'euler'
_numba_setting = {
    'nopython': True,
    'fastmath': True,
    'nogil': True,
    'parallel': False
}
_show_format_code = False
_show_code_scope = False
_substitute_equation = False
_merge_integrators = True
_merge_steps = False
_num_thread_gpu = None


def set(
        jit=None,
        device=None,
        numerical_method=None,
        dt=None,
        float_type=None,
        int_type=None,
        merge_integrators=None,
        merge_steps=None,
        substitute=None,
        show_code=None,
        show_code_scope=None
):
    # JIT and device
    if device is not None and jit is None:
        assert isinstance(device, str), "'device' must a string."
        set_device(_jit, device=device)
    if jit is not None:
        assert isinstance(jit, bool), "'jit' must be True or False."
        if device is not None:
            assert isinstance(device, str), "'device' must a string."
        set_device(jit, device=device)

    # numerical integration method
    if numerical_method is not None:
        assert isinstance(numerical_method, str), '"numerical_method" must be a string.'
        set_numerical_method(numerical_method)

    # numerical integration precision
    if dt is not None:
        assert isinstance(dt, (float, int)), '"dt" must be float or int.'
        set_dt(dt)

    # default float type
    if float_type is not None:
        from .backend import _set_default_float
        _set_default_float(float_type)

    # default int type
    if int_type is not None:
        from .backend import _set_default_int
        _set_default_int(int_type)

    # option to merge integral functions
    if merge_integrators is not None:
        assert isinstance(merge_integrators, bool), '"merge_integrators" must be True or False.'
        if run_on_gpu() and not merge_integrators:
            raise ValueError('GPU mode do not support "merge_integrators = False".')
        global _merge_integrators
        _merge_integrators = merge_integrators

    # option to merge step functions
    if merge_steps is not None:
        assert isinstance(merge_steps, bool), '"merge_steps" must be True or False.'
        global _merge_steps
        _merge_steps = merge_steps

    # option of the equation substitution
    if substitute is not None:
        assert isinstance(substitute, bool), '"substitute" must be True or False.'
        global _substitute_equation
        _substitute_equation = substitute

    # option of the formatted code output
    if show_code is not None:
        assert isinstance(show_code, bool), '"show_code" must be True or False.'
        global _show_format_code
        _show_format_code = show_code

    # option of the formatted code scope
    if show_code_scope is not None:
        assert isinstance(show_code_scope, bool), '"show_code_scope" must be True or False.'
        global _show_code_scope
        _show_code_scope = show_code_scope


def set_device(jit, device=None):
    """Set the backend and the device to deploy the models.

    Parameters
    ----------
    jit : bool
        Whether use the jit acceleration.
    device : str, optional
        The device name.
    """

    # jit
    # ---

    global _jit

    if _jit != jit:
        _jit = jit

    # device
    # ------

    global _device
    global _num_thread_gpu

    if device is None:
        return

    device = device.lower()
    if _device != device:
        if not jit:
            if device != 'cpu':
                print(f'Non-JIT mode now only supports "cpu" device, not "{device}".')
            else:
                _device = device
        else:
            if device == 'cpu':
                set_numba_profile(parallel=False)
            elif device == 'multi-cpu':
                set_numba_profile(parallel=True)
            else:
                if device.startswith('gpu'):
                    # get cuda id
                    cuda_id = device.replace('gpu', '')
                    if cuda_id == '':
                        cuda_id = 0
                        device = f'{device}0'
                    else:
                        cuda_id = float(cuda_id)

                    # set cuda
                    if cuda.is_available():
                        cuda.select_device(cuda_id)
                    else:
                        raise ValueError('Cuda is not available. Cannot set gpu backend.')

                    gpu = cuda.get_current_device()
                    _num_thread_gpu = gpu.MAX_THREADS_PER_BLOCK

                else:
                    raise ValueError(f'Unknown device in Numba mode: {device}.')
            _device = device


def get_device():
    """Get the device name.

    Returns
    -------
    device: str
        Device name.

    """
    return _device


def is_jit():
    """Check whether the backend is ``numba``.

    Returns
    -------
    jit : bool
        True or False.
    """
    return _jit


def run_on_cpu():
    """Check whether the device is "CPU".

    Returns
    -------
    device : bool
        True or False.
    """
    return _device.endswith('cpu')


def run_on_gpu():
    """Check whether the device is "GPU".

    Returns
    -------
    device : bool
        True or False.
    """
    return _device.startswith('gpu')


def set_backend(backend):
    """Set the running backend.

    Parameters
    ----------
    backend : str
        The backend name.
    """
    if backend not in ['numpy', 'pytorch']:
        raise ValueError(f'BrainPy now supports "numpy" or "pytorch" backend, not "{backend}".')

    global _backend
    _backend = backend


def get_backend():
    """Get the used backend of BrainPy.

    Returns
    -------
    backend : str
        The backend name.
    """
    return _backend


def set_numba_profile(**kwargs):
    """Set the compilation options of Numba JIT function.

    Parameters
    ----------
    kwargs : Any
        The arguments, including ``cache``, ``fastmath``,
        ``parallel``, ``nopython``.
    """
    global _numba_setting

    if 'fastmath' in kwargs:
        _numba_setting['fastmath'] = kwargs.pop('fastmath')
    if 'nopython' in kwargs:
        _numba_setting['nopython'] = kwargs.pop('nopython')
    if 'nogil' in kwargs:
        _numba_setting['nogil'] = kwargs.pop('nogil')
    if 'parallel' in kwargs:
        _numba_setting['parallel'] = kwargs.pop('parallel')


def get_numba_profile():
    """Get the compilation setting of numba JIT function.

    Returns
    -------
    numba_setting : dict
        Numba setting.
    """
    return _numba_setting


def set_dt(dt):
    """Set the numerical integrator precision.

    Parameters
    ----------
    dt : float
        Numerical integration precision.
    """
    assert isinstance(dt, float)
    global _dt
    _dt = dt


def get_dt():
    """Get the numerical integrator precision.

    Returns
    -------
    dt : float
        Numerical integration precision.
    """
    return _dt


def set_numerical_method(method):
    """Set the default numerical integrator method for differential equations.

    Parameters
    ----------
    method : str, callable
        Numerical integrator method.
    """
    from brainpy.integration import _SUPPORT_METHODS

    if not isinstance(method, str):
        raise ValueError(f'Only support string, not {type(method)}.')
    if method not in _SUPPORT_METHODS:
        raise ValueError(f'Unsupported numerical method: {method}.')

    global _method
    _method = method


def get_numerical_method():
    """Get the default numerical integrator method.

    Returns
    -------
    method : str
        The default numerical integrator method.
    """
    return _method


def is_merge_integrators():
    return _merge_integrators


def is_merge_steps():
    return _merge_steps


def is_substitute_equation():
    return _substitute_equation


def show_code_scope():
    return _show_code_scope


def show_format_code():
    return _show_format_code


def get_num_thread_gpu():
    return _num_thread_gpu
