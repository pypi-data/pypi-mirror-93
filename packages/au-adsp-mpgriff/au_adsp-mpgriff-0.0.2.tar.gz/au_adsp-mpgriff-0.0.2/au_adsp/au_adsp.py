

def zplane(b,a, *args, colour='C0'):
    """
        function to replicate the functionality of Matlab's zplane
    """

    import numpy as np
    import matplotlib.pyplot as plt
    zeros = np.roots(b)
    poles = np.roots(a)


    # make a matplotlib subplot if it wasnt given (optional parameter)
    if len(args)==0:
        fig,axs = plt.subplots(1,1, figsize=(6,6))
    else:
        axs = args[0]


    # plot the unit circle
    theta = np.linspace(0., 2.*np.pi, 1000)
    axs.plot(np.cos(theta), np.sin(theta), 'k--')

    for i,rt in enumerate(zeros):
        if i==0:
            axs.plot(rt.real, rt.imag, '{}o'.format(colour), label='zero', markerfacecolor="white")
        else:
            axs.plot(rt.real, rt.imag, '{}o'.format(colour), markerfacecolor="white")
    for i,rt in enumerate(poles):
        if i==0:
            axs.plot(rt.real, rt.imag, '{}x'.format(colour), label='poles')
        else:
            axs.plot(rt.real, rt.imag, '{}x'.format(colour))

    axs.set_aspect('equal')
    axs.set_ylabel('imag(z)', fontsize=10)
    axs.set_xlabel('real(z)', fontsize=10)
    axs.set_yticks([-1, -0.5, 0, 0.5, 1.])
    axs.set_xticks([-1, -0.5, 0, 0.5, 1.])
    axs.legend()
    plt.show()
    return zeros, poles
