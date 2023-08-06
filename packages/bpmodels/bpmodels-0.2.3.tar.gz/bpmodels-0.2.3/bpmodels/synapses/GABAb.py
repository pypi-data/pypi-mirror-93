# -*- coding: utf-8 -*-

import brainpy as bp
import numpy as np
import sys


def get_GABAb1(g_max=0.02, E=-95., k1=0.18, k2=0.034, k3=0.09, k4=0.0012,
               kd=100., T=0.5, T_duration=0.3, mode='vector'):
    """GABAb conductance-based synapse model(type 1).

    .. math::

        &\\frac{d[R]}{dt} = k_3 [T](1-[R])- k_4 [R]

        &\\frac{d[G]}{dt} = k_1 [R]- k_2 [G]

        I_{GABA_{B}} &=\\overline{g}_{GABA_{B}} (\\frac{[G]^{4}} {[G]^{4}+K_{d}}) (V-E_{GABA_{B}})


    - [G] is the concentration of activated G protein.
    - [R] is the fraction of activated receptor.
    - [T] is the transmitter concentration.

    **Synapse Parameters**

    ============= ============== ======== ============================================================================
    **Parameter** **Init Value** **Unit** **Explanation**
    ------------- -------------- -------- ----------------------------------------------------------------------------
    g_max         0.02           \        Maximum synapse conductance.

    E             -95.           mV       Reversal potential of synapse.

    k1            0.18           \        Activating rate constant of G protein catalyzed 

                                          by activated GABAb receptor.

    k2            0.034          \        De-activating rate constant of G protein.

    k3            0.09           \        Activating rate constant of GABAb receptor.

    k4            0.0012         \        De-activating rate constant of GABAb receptor.

    kd            100.           \        Dissociation rate constant of the binding of 

                                          G protein on K+ channels.

    T             0.5            \        Transmitter concentration when synapse is 

                                          triggered by a pre-synaptic spike.

    T_duration    0.3            \        Transmitter concentration duration time 

                                          after being triggered.

    mode          'vector'       \        Data structure of ST members.
    ============= ============== ======== ============================================================================

    Returns:
        bp.SynType: return description of GABAb synapse model.


    **Synapse State**

    ST refers to synapse state, members of ST are listed below:

    ================ ================= =========================================================
    **Member name**  **Initial Value** **Explanation**
    ---------------- ----------------- ---------------------------------------------------------
    R                0.                The fraction of activated receptor.

    G                0.                The concentration of activated G protein.

    g                0.                Synapse conductance on post-synaptic neuron.

    t_last_pre_spike -1e7              Last spike time stamp of pre-synaptic neuron.
    ================ ================= =========================================================

    Note that all ST members are saved as floating point type in BrainPy, 
    though some of them represent other data types (such as boolean).

    References:
        .. [1] Gerstner, Wulfram, et al. Neuronal dynamics: From single 
               neurons to networks and models of cognition. Cambridge 
               University Press, 2014.
    """

    ST = bp.types.SynState('R', 'G', 'g', t_last_pre_spike=-1e7)

    requires = {
        'pre': bp.types.NeuState(['spike'], help="Pre-synaptic neuron state must have 'spike' item"),
        'post': bp.types.NeuState(['V', 'input'], help="Post-synaptic neuron state must have 'V' and 'input' item"),
    }

    @bp.integrate
    def int_R(R, t, TT):
        return k3 * TT * (1 - R) - k4 * R

    @bp.integrate
    def int_G(G, t, R):
        return k1 * R - k2 * G

    if mode == 'scalar':
        def update(ST, _t, pre):
            if pre['spike'] > 0.:
                ST['t_last_pre_spike'] = _t
            TT = ((_t - ST['t_last_pre_spike']) < T_duration) * T
            R = int_R(ST['R'], _t, TT)
            G = int_G(ST['G'], _t, R)
            ST['R'] = R
            ST['G'] = G
            ST['g'] = g_max * G ** 4 / (G ** 4 + kd)

        @bp.delayed
        def output(ST, _t, post):
            I_syn = ST['g'] * (post['V'] - E)
            post['input'] -= I_syn

        return bp.SynType(name='GABAb1_synapse',
                          ST=ST,
                          requires=requires,
                          steps=(update, output),
                          mode=mode)

    elif mode == 'vector':

        requires['pre2syn'] = bp.types.ListConn()
        requires['post_slice_syn'] = bp.types.Array(dim=2)

        def update(ST, _t, pre, pre2syn):
            for pre_id in np.where(pre['spike'] > 0.)[0]:
                syn_ids = pre2syn[pre_id]
                ST['t_last_pre_spike'][syn_ids] = _t
            TT = ((_t - ST['t_last_pre_spike']) < T_duration) * T
            R = int_R(ST['R'], _t, TT)
            G = int_G(ST['G'], _t, R)
            ST['R'] = R
            ST['G'] = G
            ST['g'] = g_max * G ** 4 / (G ** 4 + kd)

        @bp.delayed
        def output(ST, post, post_slice_syn):
            post_num = len(post_slice_syn)
            post_cond = np.zeros(post_num, dtype=np.float_)
            for i, [s, e] in enumerate(post_slice_syn):
                post_cond[i] = np.sum(ST['g'][s:e])
            post['input'] -= post_cond * (post['V'] - E)

    elif mode == 'matrix':

        def update(ST, _t, pre):
            spike_idxs = np.where(pre['spike'] > 0.)[0]
            ST['t_last_pre_spike'][spike_idxs] = _t
            TT = ((_t - ST['t_last_pre_spike']) < T_duration) * T
            R = int_R(ST['R'], _t, TT)
            G = int_G(ST['G'], _t, R)
            ST['R'] = R
            ST['G'] = G
            ST['g'] = g_max * G ** 4 / (G ** 4 + kd)

        @bp.delayed
        def output(ST, post):
            g = np.sum(ST['g'], axis=0)
            post['input'] -= g * (post['V'] - E)

    else:
        raise ValueError("BrainPy does not support mode '%s'." % (mode))

    return bp.SynType(name='GABAb1_synapse',
                      ST=ST,
                      requires=requires,
                      steps=(update, output),
                      mode=mode)


def get_GABAb2(g_max=0.02, E=-95., k1=0.66, k2=0.02, k3=0.0053, k4=0.017,
               k5=8.3e-5, k6=7.9e-3, kd=100., T=0.5, T_duration=0.5, mode='vector'):
    """
    GABAb conductance-based synapse model (markov form).

    G-protein cascade occurs in the following steps: 
    (i) the transmitter binds to the receptor, leading to its activated form; 
    (ii) the activated receptor catalyzes the activation of G proteins; 
    (iii) G proteins bind to open K+ channel, with n(=4) independent binding sites.

    .. math::

        &\\frac{d[D]}{dt}=K_{4}[R]-K_{3}[D]

        &\\frac{d[R]}{dt}=K_{1}[T](1-[R]-[D])-K_{2}[R]+K_{3}[D]

        &\\frac{d[G]}{dt}=K_{5}[R]-K_{6}[G]

        I_{GABA_{B}}&=\\bar{g}_{GABA_{B}} \\frac{[G]^{n}}{[G]^{n}+K_{d}}(V-E_{GABA_{B}})

    - [R] is the fraction of activated receptor.
    - [D] is the fraction of desensitized receptor.
    - [G] is the concentration of activated G-protein (μM).
    - [T] is the transmitter concentration.

    **Synapse Parameters**

    ============= ============== ======== ============================================================================
    **Parameter** **Init Value** **Unit** **Explanation**
    ------------- -------------- -------- ----------------------------------------------------------------------------
    g_max         0.02           \        Maximum synapse conductance.

    E             -95.           mV       Reversal potential of synapse.

    k1            0.66           \        Activating rate constant of G protein 

                                          catalyzed by activated GABAb receptor.

    k2            0.02           \        De-activating rate constant of G protein.

    k3            0.0053         \        Activating rate constant of GABAb receptor.

    k4            0.017          \        De-activating rate constant of GABAb receptor.

    k5            8.3e-5         \        Activating rate constant of G protein 

                                          catalyzed by activated GABAb receptor.

    k6            7.9e-3         \        De-activating rate constant of activated G protein.

    kd            100.           \        Dissociation rate constant of the binding of 

                                          G protein on K+ channels.

    T             0.5            \        Transmitter concentration when synapse 

                                          is triggered by a pre-synaptic spike.

    T_duration    0.5            \        Transmitter concentration duration time 

                                          after being triggered.

    mode          'vector'       \        Data structure of ST members.
    ============= ============== ======== ============================================================================

    Returns:
        bp.SynType: return decription of GABAb synapse model.


    **Synapse State**

    ST refers to synapse state, members of ST are listed below:

    ================ ================= =========================================================
    **Member name**  **Initial Value** **Explanation**
    ---------------- ----------------- ---------------------------------------------------------
    D                0.                The fraction of desensitized receptor.

    R                0.                The fraction of activated receptor.

    G                0.                The concentration of activated G protein.

    g                0.                Synapse conductance on post-synaptic neuron.

    t_last_pre_spike -1e7              Last spike time stamp of pre-synaptic neuron.
    ================ ================= =========================================================

    Note that all ST members are saved as floating point type in BrainPy, 
    though some of them represent other data types (such as boolean).

    References:
        .. [1] Destexhe, Alain, et al. "G-protein activation kinetics and 
               spillover of GABA may account for differences between 
               inhibitory responses in the hippocampus and thalamus." 
               Proc. Natl. Acad. Sci. USA v92 (1995): 9515-9519.

    """
    ST = bp.types.SynState('D', 'R', 'G', 'g', t_last_pre_spike=-1e7)

    requires = dict(
        pre=bp.types.NeuState(
            ['spike'], help="Pre-synaptic neuron state must have 'spike' item"),
        post=bp.types.NeuState(
            ['V', 'input'], help="Post-synaptic neuron state must have 'V' and 'input' item"),
    )

    @bp.integrate
    def int_D(D, t, R):
        return k4 * R - k3 * D

    @bp.integrate
    def int_R(R, t, TT, D):
        return k1 * TT * (1 - R - D) - k2 * R + k3 * D

    @bp.integrate
    def int_G(G, t, R):
        return k5 * R - k6 * G

    if mode == 'scalar':

        def update(ST, _t, pre):
            if pre['spike'] > 0.:
                ST['t_last_pre_spike'] = _t
            TT = ((_t - ST['t_last_pre_spike']) < T_duration) * T
            D = int_D(ST['D'], _t, ST['R'])
            R = int_R(ST['R'], _t, TT, D)
            G = int_G(ST['G'], _t, R)
            ST['D'] = D
            ST['R'] = R
            ST['G'] = G
            ST['g'] = g_max * (G ** 4 / (G ** 4 + kd))

        @bp.delayed
        def output(ST, post):
            post['input'] -= ST['g'] * (post['V'] - E)

    elif mode == 'vector':

        requires['pre2syn'] = bp.types.ListConn(
            help="Pre-synaptic neuron index -> synapse index")
        requires['post_slice_syn'] = bp.types.Array(dim=2)

        def update(ST, _t, pre, pre2syn):
            # calculate synaptic state
            for pre_id in np.where(pre['spike'] > 0.)[0]:
                syn_ids = pre2syn[pre_id]
                ST['t_last_pre_spike'][syn_ids] = _t
            TT = ((_t - ST['t_last_pre_spike']) < T_duration) * T
            D = int_D(ST['D'], _t, ST['R'])
            R = int_R(ST['R'], _t, TT, D)
            G = int_G(ST['G'], _t, R)
            ST['D'] = D
            ST['R'] = R
            ST['G'] = G
            ST['g'] = g_max * (G ** 4 / (G ** 4 + kd))

        @bp.delayed
        def output(ST, post, post_slice_syn):
            post_num = len(post_slice_syn)
            post_cond = np.zeros(post_num, dtype=np.float_)
            for i, [s, e] in enumerate(post_slice_syn):
                post_cond[i] = np.sum(ST['g'][s:e])
            post['input'] -= post_cond * (post['V'] - E)

    elif mode == 'matrix':

        def update(ST, _t, pre):
            spike_idxs = np.where(pre['spike'] > 0.)[0]
            ST['t_last_pre_spike'][spike_idxs] = _t
            TT = ((_t - ST['t_last_pre_spike']) < T_duration) * T
            D = int_D(ST['D'], _t, ST['R'])
            R = int_R(ST['R'], _t, TT, D)
            G = int_G(ST['G'], _t, R)
            ST['D'] = D
            ST['R'] = R
            ST['G'] = G
            ST['g'] = g_max * (G ** 4 / (G ** 4 + kd))

        @bp.delayed
        def output(ST, post):
            g = np.sum(ST['g'], axis=0)
            post['input'] -= g * (post['V'] - E)

    else:
        raise ValueError("BrainPy does not support mode '%s'." % (mode))

    return bp.SynType(name='GABAb2_synapse',
                      ST=ST,
                      requires=requires,
                      steps=(update, output),
                      mode=mode)
