# # # # # # #
# Weighting #
# # # # # # #
#
# Correct weighting of events from different
# MC sources.
#
# 2016 T. Hoinka (tobias.hoinka@udo.edu)

import numpy as np

from icecube.weighting.fluxes import GaisserH3a, Hoerandel5, GaisserH4a, Honda2004
from icecube.weighting import weighting

import joblib
import os

class compoundWeightGenerator:
	def __init__(self):
		self.g_list = []
		self.n_list = []
		self.id_list = []
		self.flux1 = GaisserH3a()
		self.flux2 = GaisserH4a()
		self.flux3 = Honda2004()

	def get_weight(self, energy, ptype):
		weight_vector = [self.n_list[i] * self.g_list[i](energy, ptype) for i in range(len(self.g_list))]
		return {'G3' : self.flux1(energy, ptype) / np.sum(weight_vector, axis=0),
				'G4' : self.flux2(energy, ptype) / np.sum(weight_vector, axis=0),
				'H' : self.flux3(energy, ptype) / np.sum(weight_vector, axis=0)}

	def add_generator(self, path, sim_id, n_files):
		if os.path.exists(path):
			generator = joblib.load(path)
			self.g_list += [generator]
		else:
			generator = weighting.from_simprod(sim_id)
			joblib.dump(generator, path)
			print("Written to new file %s." % path)
			self.g_list += [generator]
		self.n_list += [n_files]
		self.id_list += [sim_id]

