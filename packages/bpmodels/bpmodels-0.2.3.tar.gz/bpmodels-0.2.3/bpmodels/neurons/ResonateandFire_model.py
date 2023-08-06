# -*- coding: utf-8 -*-

import sys
import brainpy as bp


def get_ResonateandFire(b=-1., omega=10., V_th=1., V_reset=1., x_reset=0., noise=0., mode='scalar'):
    """Resonate-and-fire neuron model.

    .. math::

        \\frac{d x}{d t} = b x - \\omega y

        \\frac{d y}{d t} = \\omega x + b y

    When spike,

    .. math::

        x \\leftarrow 0

        y \\leftarrow 1

    Or we can write the equations in equivalent complex form:    

    .. math::

        \\frac{d z}{d t} = (b + i \\omega) z

        z = x + i y \\in \\mathbb{C}


    When spike,

    .. math::

        z \\leftarrow i

    **Neuron Parameters**

    ============= ============== ======== ========================================================
    **Parameter** **Init Value** **Unit** **Explanation**
    ------------- -------------- -------- --------------------------------------------------------
    b             -1.            \        Parameter, refers to the rate of attrsction to the rest.

    omega         10.            \        Parameter. refers to the frequency of the oscillations.

    V_th          1.             \        Threshold potential of spike.

    V_reset       1.             \        Reset value for voltage-like variable after spike.

    x_reset       0.             \        Reset value for current-like variable after spike.

    mode          'scalar'       \        Data structure of ST members.
    ============= ============== ======== ========================================================

    Returns:
        bp.Neutype: return description of RF model.


    **Neuron State**

    ST refers to neuron state, members of ST are listed below:

    =============== ================= ==============================================
    **Member name** **Initial Value** **Explanation**
    --------------- ----------------- ----------------------------------------------
    V               0.                Voltage-like variable.

    x               0.                Current-like variable.

    input           0.                External and synaptic input current.

    spike           0.                Flag to mark whether the neuron is spiking. 

                                      Can be seen as bool.

    t_last_spike    -1e7              Last spike time stamp.
    =============== ================= ==============================================

    Note that all ST members are saved as floating point type in BrainPy, 
    though some of them represent other data types (such as boolean).

    References:
        .. [1] Izhikevich, Eugene M. "Resonate-and-fire neurons." 
               Neural networks 14.6-7 (2001): 883-894.

    """

    ST = bp.types.NeuState(
        {'V': 0., 'x': 0., 'input': 0., 'spike': 0., 't_last_spike': -1e7}
    )

    @bp.integrate
    def int_x(x, t, V):  # input--internal
        return b * x - omega * V

    @bp.integrate
    def int_V(V, t, x):  # V
        return omega * x + b * V

    if mode == 'scalar':

        def update(ST, _t):
            # update variables
            ST['spike'] = 0.
            x = ST['x']
            x += ST['input']
            V = ST['V']
            x = int_x(x, _t, V)
            V = int_V(V, _t, x)
            if V > V_th:
                V = V_reset
                x = x_reset
                ST['spike'] = 1.
            ST['x'] = x
            ST['V'] = V
            ST['input'] = 0.  # reset input here or it will be brought to next step

    elif mode == 'vector':

        def update(ST, _t):
            x = ST['x'] + ST['input']
            x = int_x(x, _t, ST['V'])
            V = int_V(ST['V'], _t, x)

            is_spike = V > V_th
            V[is_spike] = V_reset
            x[is_spike] = x_reset

            ST['spike'] = is_spike
            ST['x'] = x
            ST['V'] = V
            ST['input'] = 0.  # reset input here or it will be brought to next step

    else:
        raise ValueError("BrainPy does not support mode '%s'." % (mode))

    return bp.NeuType(name='RF_neuron',
                      ST=ST,
                      steps=update,
                      mode=mode)
