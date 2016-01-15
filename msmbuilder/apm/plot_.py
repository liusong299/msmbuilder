__author__ = 'stephen'
import numpy as np
import matplotlib.pyplot as plt
def plot_cluster(labels, phi_angles, psi_angles, name, outliers=-1, step=1, potential=False):
    '''
    :param labels: the assignments after clustering or lumping
    :param phi_angles: the phi angles
    :param psi_angles: the psi angles
    :param name: the name of the result pictures
    :param outliers: outliers default is -1
    :param potential: True is for 2D potential test, Flase is for Alanine Dipeptide test
    :return: None
    '''

    clusters = np.unique(labels)
    plt.rc("font", size=30)
    if step > 1:
        clusters = clusters[0:len(clusters):step]
    if potential is False: #plot Alanine Dipeptide
        for i in clusters:
            if i != outliers:
            #if i == 1:
                plt.plot(phi_angles[np.where(labels == i)],
                        psi_angles[np.where(labels == i)], '.',  alpha=0.1)

        plt.xlim([-180, 180])
        plt.ylim([-180, 180])
        plt.xticks([-120, -60, 0, 60, 120])
        plt.yticks([-120, -60, 0, 60, 120])
    else:  # if plot 2D potential
        plt.figure(figsize=(10, 10))
        for i in clusters:
            if i != outliers:
                plt.plot(phi_angles[np.where(labels == i)],
                        psi_angles[np.where(labels == i)], '.', markersize=1.0, alpha=0.7)
        plt.xlim([-75, 75])
        plt.ylim([-75, 75])
        plt.xticks([-50, 0, 50])
        plt.yticks([-50, 0, 50])


    plt.xlabel(r"$\phi$", fontsize=25)
    plt.ylabel(r"$\psi$", fontsize=25)
    # Save the result figure
    plt.savefig('./'+name+'.png', dpi=400)
    plt.close()
    #plt.show()
