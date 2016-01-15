import mdtraj as md
import os
import operator
import numpy as np

class TrajReader:
    def walk_dir(self,input_traj_dir, input_traj_ext,topdown=True):
        frame_list = []
        for root, dirs, files in os.walk(input_traj_dir, topdown):
            for name in files:
                if os.path.splitext(name)[1] == input_traj_ext:
                    frame_list.append( os.path.join( root, name ))
        return frame_list

    def get_trajlist(self,trajlist_filename, trajlist_dir):
        trajlist_file = open( trajlist_filename )
        trajlist_list = []
        for line in trajlist_file:
            list = trajlist_dir + '/' + line.rstrip("\n")
            list = list.strip() # remove the spaces in the end line, thanks to Yang Xi for reporting this bug, Stephen 20141208
            trajlist_list.append( list )
        trajlist_file.close()
        return trajlist_list

    def get_homedir(self):
        return os.getcwd()

    def get_atom_indices(self, indices_filename, indices_dir):
        if indices_filename != None:
            indices_file = open( indices_filename )
            atom_indices = map(int, indices_file.read().split(' '))
            indices_file.close()
            del atom_indices[ 0 ]
            return atom_indices
        else:
            return None

    def get_framefile_list(self, trajlist_list):
        framefile_list = []
        Ext = '.' + self.trajExt
        for trajlist in trajlist_list:
            framefile_list.extend( self.walk_dir(trajlist, Ext))
        return framefile_list

class XTCReader(TrajReader):
    def __init__(self, trajlistName=None, atomlistName=None, homedir=None, trajExt=None, File_TOP=None, nSubSample=None):
        self.trajlistName = trajlistName
        self.atomlistName = atomlistName
        self.trajDir = homedir
        self.trajExt = trajExt
        self.File_TOP = File_TOP
        self.homedir = homedir
        self.nSubSample = nSubSample
        self.trajlist_list = self.get_trajlist(trajlistName, self.homedir)
        if atomlistName is not None:
            self.atom_indices = self.get_atom_indices( atomlistName, self.homedir)
        else:
            self.atom_indices = None
        self.framefile_list = self.get_framefile_list(self.trajlist_list)
        self.trajs = self.read_trajs(self.framefile_list)


    def read_trajs(self, framelist):
        trajs = []
        print "Reading trajs..."
        for frame in framelist:
            print 'Reading: ', frame
            traj = md.load(frame, discard_overlapping_frames=True, top=self.File_TOP, atom_indices=self.atom_indices,
                           stride=self.nSubSample)
            #traj = traj[:-1] #remove last one
            trajs.append(traj)

        len_trajs = len(trajs)
        #whole_trajs= reduce(operator.add, (trajs[i] for i in xrange(len_trajs)))
        print "Done."
        print len_trajs, "trajs,"

        return trajs

    def get_phipsi(self, trajs, phi, psi):
        len_trajs = len(trajs)
        whole_trajs= reduce(operator.add, (trajs[i] for i in xrange(len_trajs)))
        PHI_INDICES = []
        PSI_INDICES = []
        for i in xrange(len(phi)):
            PHI_INDICES.append(self.atom_indices.index(phi[i]))
            PSI_INDICES.append(self.atom_indices.index(psi[i]))
        print "PSI:", PSI_INDICES
        print "PHI:", PHI_INDICES
        phi_angles = md.compute_dihedrals(whole_trajs, [PHI_INDICES]) * 180.0 / np.pi
        psi_angles = md.compute_dihedrals(whole_trajs, [PSI_INDICES]) * 180.0 / np.pi
        return phi_angles, psi_angles

class VectorReader(TrajReader):
    def __init__(self, trajlistName, atomlistName=None, homedir='.', trajExt='txt', File_TOP=None, nSubSample=1):
        self.trajlistName = trajlistName
        self.trajDir = homedir
        self.trajExt = trajExt
        self.homedir = homedir
        self.nSubSample = nSubSample
        self.trajlist_list = self.get_trajlist(trajlistName, self.homedir)
        self.framefile_list = self.get_framefile_list(self.trajlist_list)
        self.trajs, self.traj_len = self.read_trajs(self.framefile_list)


    def read_trajs(self, framelist):
        trajs = []
        traj_len = []
        for frame in framelist:
            print 'Reading: ', frame
            traj = np.loadtxt(frame, usecols=(0, 1), dtype='float32')
            traj = traj[:-1] #remove last one
            len_traj = len(traj)
            traj = traj[0:len_traj:self.nSubSample]
            #trajs.extend(traj)
            trajs.append(traj)
            traj_len.append(len(traj))
        print "Total Trajs:", len(trajs)
        return np.asarray(trajs), traj_len
