# -*- coding: utf-8 -*-

import brainpy as bp
import numpy as np

def get_AMPA1(g_max=0.10, E=0., tau_decay=2.0, mode = 'scalar'):
    """AMPA conductance-based synapse (type 1).

    .. math::

        I(t)&=\\bar{g} s(t) (V-E_{syn})

        \\frac{d s}{d t}&=-\\frac{s}{\\tau_{decay}}+\\sum_{k} \\delta(t-t_{j}^{k})


    **Synapse Parameters**
    
    ============= ============== ======== ===================================================================================
    **Parameter** **Init Value** **Unit** **Explanation**
    ------------- -------------- -------- -----------------------------------------------------------------------------------
    tau_decay     2.             ms       The time constant of decay.

    g_max         .1             µmho(µS) Maximum conductance.

    E             0.             mV       The reversal potential for the synaptic current. (only for conductance-based model)

    mode          'scalar'       \        Data structure of ST members.
    ============= ============== ======== ===================================================================================  
    
    Returns:
        bp.Syntype: return description of the AMPA synapse model.

    **Synapse State**

    ST refers to the synapse state, items in ST are listed below:
    
    =============== ================== =========================================================
    **Member name** **Initial values** **Explanation**
    --------------- ------------------ ---------------------------------------------------------
    s                   0               Gating variable.
    
    g                   0               Synapse conductance.
    =============== ================== =========================================================

    Note that all ST members are saved as floating point type in BrainPy, 
    though some of them represent other data types (such as boolean).

    References:
        .. [1] Brunel N, Wang X J. Effects of neuromodulation in a cortical network 
                model of object working memory dominated by recurrent inhibition[J]. 
                Journal of computational neuroscience, 2001, 11(1): 63-85.
    """

    @bp.integrate
    def ints(s, t):
        return - s / tau_decay

    ST=bp.types.SynState(['s', 'g'], help='AMPA synapse state.')

    requires = {
        'pre': bp.types.NeuState(['spike'], help='Pre-synaptic neuron state must have "spike" item.'),
        'post': bp.types.NeuState(['V', 'input'], help='Post-synaptic neuron state must have "V" and "input" item.')
    }

    if mode == 'scalar':
        def update(ST, _t, pre):
            s = ints(ST['s'], _t)
            s += pre['spike']
            ST['s'] = s
            ST['g'] = g_max * s

        @bp.delayed
        def output(ST, post):
            post_val = - ST['g'] * (post['V'] - E)
            post['input'] += post_val

    elif mode == 'vector':
        requires['pre2syn']=bp.types.ListConn(help='Pre-synaptic neuron index -> synapse index')
        requires['post_slice_syn']=bp.types.Array(dim=2)

        def update(ST, _t, pre, pre2syn):
            s = ints(ST['s'], _t)
            spike_idx = np.where(pre['spike'] > 0.)[0]
            for i in spike_idx:
                syn_idx = pre2syn[i]
                s[syn_idx] += 1.
            ST['s'] = s
            ST['g'] = g_max * s

        @bp.delayed
        def output(ST, post, post_slice_syn):
            num_post = post_slice_syn.shape[0]
            g = np.zeros(num_post, dtype=np.float_)
            for post_id in range(num_post):
                pos = post_slice_syn[post_id]
                g[post_id] = np.sum(ST['g'][pos[0]: pos[1]])
            post['input'] -= g * (post['V'] - E)

    elif mode == 'matrix':
        requires['conn_mat']=bp.types.MatConn()

        def update(ST, _t, pre, conn_mat):
            s = ints(ST['s'], _t)
            s += pre['spike'].reshape((-1, 1)) * conn_mat
            ST['s'] = s
            ST['g'] = g_max * s

        @bp.delayed
        def output(ST, post):
            g = np.sum(ST['g'], axis=0)
            post['input'] -= g * (post['V'] - E)

    else:
        raise ValueError("BrainPy does not support mode '%s'." % (mode))


    return bp.SynType(name='AMPA_synapse',
                      ST=ST, requires=requires,
                      steps=(update, output),
                      mode = mode)



def get_AMPA2(g_max=0.42, E=0., alpha=0.98, beta=0.18, T=0.5, T_duration=0.5, mode = 'scalar'):
    """AMPA conductance-based synapse (type 2).

    .. math::

        I_{syn}&=\\bar{g}_{syn} s (V-E_{syn})

        \\frac{ds}{dt} &=\\alpha[T](1-s)-\\beta s

    **Synapse Parameters**
    
    ============= ============== ======== ================================================
    **Parameter** **Init Value** **Unit** **Explanation**
    ------------- -------------- -------- ------------------------------------------------
    g_max         .42            µmho(µS) Maximum conductance.

    E             0.             mV       The reversal potential for the synaptic current.

    alpha         .98            \        Binding constant.

    beta          .18            \        Unbinding constant.

    T             .5             mM       Neurotransmitter concentration.

    T_duration    .5             ms       Duration of the neurotransmitter concentration.

    mode          'scalar'       \        Data structure of ST members.
    ============= ============== ======== ================================================    
    
    Returns:
        bp.Syntype: return description of the AMPA synapse model.

    **Synapse State**

    ST refers to the synapse state, items in ST are listed below:
    
    ================ ================== =========================================================
    **Member name**  **Initial values** **Explanation**
    ---------------- ------------------ ---------------------------------------------------------
    s                 0                 Gating variable.
    
    g                 0                 Synapse conductance.

    t_last_pre_spike  -1e7              Last spike time stamp of the pre-synaptic neuron.
    ================ ================== =========================================================
    
    Note that all ST members are saved as floating point type in BrainPy, 
    though some of them represent other data types (such as boolean).

    References:
        .. [1] Vijayan S, Kopell N J. Thalamic model of awake alpha oscillations 
                and implications for stimulus processing[J]. Proceedings of the 
                National Academy of Sciences, 2012, 109(45): 18553-18558.
    """

    @bp.integrate
    def int_s(s, t, TT):
        return alpha * TT * (1 - s) - beta * s

    ST=bp.types.SynState({'s': 0., 't_last_pre_spike': -1e7, 'g': 0.},
                             help='AMPA synapse state.\n'
                                  '"s": Synaptic state.\n'
                                  '"t_last_pre_spike": Pre-synaptic neuron spike time.')

    requires = dict(
        pre=bp.types.NeuState(['spike'], help='Pre-synaptic neuron state must have "spike" item.'),
        post=bp.types.NeuState(['V', 'input'], help='Post-synaptic neuron state must have "V" and "input" item.')
    )

    if mode == 'scalar':
        def update(ST, _t, pre):
            if pre['spike'] > 0.:
                ST['t_last_pre_spike'] = _t
            TT = ((_t - ST['t_last_pre_spike']) < T_duration) * T
            s = np.clip(int_s(ST['s'], _t, TT), 0., 1.)
            ST['s'] = s
            ST['g'] = g_max * s

        @bp.delayed
        def output(ST, post):
            post_val = - ST['g'] * (post['V'] - E)
            post['input'] += post_val

    elif mode == 'vector':
        requires['pre2syn']=bp.types.ListConn(help='Pre-synaptic neuron index -> synapse index')
        requires['post_slice_syn']=bp.types.Array(dim=2)

        def update(ST, _t, pre, pre2syn):
            for i in np.where(pre['spike'] > 0.)[0]:
                syn_idx = pre2syn[i]
                ST['t_last_pre_spike'][syn_idx] = _t
            TT = ((_t - ST['t_last_pre_spike']) < T_duration) * T
            s = np.clip(int_s(ST['s'], _t, TT), 0., 1.)
            ST['s'] = s
            ST['g'] = g_max * s

        @bp.delayed
        def output(ST, post, post_slice_syn):
            num_post = post_slice_syn.shape[0]
            g = np.zeros(num_post, dtype=np.float_)
            for post_id in range(num_post):
                pos = post_slice_syn[post_id]
                g[post_id] = np.sum(ST['g'][pos[0]: pos[1]])
            post['input'] -= g * (post['V'] - E)


    elif mode == 'matrix':
        requires['conn_mat']=bp.types.MatConn()

        def update(ST, _t, pre, conn_mat):
            spike_idxs = np.where(pre['spike'] > 0.)[0]
            ST['t_last_pre_spike'][spike_idxs] = _t
            TT = ((_t - ST['t_last_pre_spike']) < T_duration) * T
            s = np.clip(int_s(ST['s'], _t, TT), 0., 1.)
            ST['s'] = s
            ST['g'] = g_max * s

        @bp.delayed
        def output(ST, post):
            g = np.sum(ST['g'], axis=0)
            post['input'] -= g * (post['V'] - E)

    else:
        raise ValueError("BrainPy does not support mode '%s'." % (mode))

    return bp.SynType(name='AMPA_synapse',
                      ST=ST, requires=requires,
                      steps=(update, output),
                      mode = mode)
