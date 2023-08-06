# -*- coding: utf-8 -*-

import brainpy as bp
import numpy as np
import matplotlib.pyplot as plt
import sys

def get_BCM(learning_rate=0.005, w_max=2., w_min = 0., r_0 = 0., mode='matrix'):
    """
    Bienenstock-Cooper-Munro (BCM) rule.

    .. math::

        r_i = \\sum_j w_{ij} r_j 

        \\frac d{dt} w_{ij} = \\eta \\cdot r_i (r_i - r_{\\theta}) r_j

    where :math:`\\eta` is some learning rate, and :math:`r_{\\theta}` is the 
    plasticity threshold,
    which is a function of the averaged postsynaptic rate, we take:

    .. math::

        r_{\\theta} = < r_i >

    **Learning Rule Parameters**
    
    ============= ============== ======== ================================
    **Parameter** **Init Value** **Unit** **Explanation**
    ------------- -------------- -------- --------------------------------
    learning_rate 0.005          \        Learning rate.

    w_max         2.             \        Maximal possible synapse weight.

    w_min         0.             \        Minimal possible synapse weight.

    mode          'matrix'       \        Data structure of ST members.
    ============= ============== ======== ================================

    Returns:
        bp.Syntype: return description of the BCM rule.
        
    
    **Learning Rule State**

    ST refers to synapse state (note that BCM learning rule can be implemented as synapses),
    members of ST are listed below:

    ================ ================= =========================================================
    **Member name**  **Initial Value** **Explanation**
    ---------------- ----------------- ---------------------------------------------------------                                  
    w                1.                Synapse weights.
    ================ ================= =========================================================

    Note that all ST members are saved as floating point type in BrainPy, 
    though some of them represent other data types (such as boolean).

    References:
        .. [1] Gerstner, Wulfram, et al. Neuronal dynamics: From single 
               neurons to networks and models of cognition. Cambridge 
               University Press, 2014.
    """
    ST=bp.types.SynState(
            {'w': 1.}, 
            help='BCM synapse state.')

    requires = dict(
        pre=bp.types.NeuState(
            ['r'], help='Pre-synaptic neuron state must have "spike" item.'),
        post=bp.types.NeuState(
            ['r'], help='Post-synaptic neuron state must have "spike" item.'),
        sum_post_r = bp.types.Array(dim=1)        
    )

    dt = bp.profile._dt

    @bp.integrate
    def int_w(w, t, r_pre, r_post, r_th):
        dwdt = learning_rate * r_post * (r_post - r_th) * r_pre
        return dwdt

    if mode == 'scalar':
        raise ValueError("mode of function '%s' can not be '%s'." % (sys._getframe().f_code.co_name, mode))

    elif mode == 'vector':
        requires['post2syn']=bp.types.ListConn()
        requires['post2pre']=bp.types.ListConn()

        def learn(ST, _t, pre, post, post2syn, post2pre, sum_post_r):
            for post_id , post_r_i in enumerate(post['r']):
                if post_r_i < r_0:
                    post['r'][post_id] = post_r_i
                elif post2syn[post_id].size > 0:
                    # mapping
                    syn_ids = post2syn[post_id]
                    pre_ids = post2pre[post_id]
                    pre_r = pre['r'][pre_ids]
                    w = ST['w'][syn_ids]

                    # threshold
                    sum_post_r[post_id] += post_r_i
                    r_threshold = sum_post_r[post_id] / (_t / dt + 1)
                    
                    # BCM rule
                    w = int_w(w, _t, pre_r, post_r_i, r_threshold)
                    w = np.clip(w, w_min, w_max)
                    ST['w'][syn_ids] = w

                    # output
                    post['r'][post_id] = np.dot(w, pre_r)


    elif mode == 'matrix':
        requires['conn_mat']=bp.types.MatConn()

        def learn(ST, _t, pre, post, conn_mat, sum_post_r):
            post_r_i = post['r']
            w = ST['w'] * conn_mat
            pre_r = pre['r']

            # threshold
            sum_post_r += post_r_i
            r_th = sum_post_r / (_t / dt + 1) 

            # BCM rule
            dim = np.shape(w)
            reshape_th = np.vstack((r_th,)*dim[0])
            reshape_post = np.vstack((post_r_i,)*dim[0])
            reshape_pre = np.vstack((pre_r,)*dim[1]).T
            w = int_w(w, _t, reshape_pre, reshape_post, reshape_th)
            w = np.clip(w, w_min, w_max)
            ST['w'] = w

            # output
            post['r'] = np.dot(w.T, pre_r)

    else:
        raise ValueError("BrainPy does not support mode '%s'." % (mode))

    return bp.SynType(name='BCM_synapse',
                      ST=ST,
                      requires=requires,
                      steps=learn,
                      mode=mode)