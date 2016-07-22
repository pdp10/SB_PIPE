#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sb_pipe.
#
# sb_pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sb_pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Object: Execute the model several times for deterministic or stochastical analysis
#
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-23 13:45:32 $




import os
import sys
import glob
import shutil
from subprocess import Popen,PIPE
# for generating a timestamp
import datetime
import logging
logger = logging.getLogger('sbpipe')

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(SB_PIPE)
from sb_config import get_copasi

sys.path.append(os.path.join(SB_PIPE,'sb_pipe','utils','python'))
from RandomiseParameters import *
from parallel_computation import parallel_computation



# Input parameters
# model: read the model
# models_dir: read the models dir
# output_dir: The output dir
# tmp_dir: read the temp dir
# sim_number: the number of simulations to perform
def main(model, models_dir, data_dir, data_folder, cluster_type, pp_cpus, nfits, results_dir, output_folder, tmp_dir):
  
  if int(nfits) < 1: 
    logger.error("variable " + nfits + " must be greater than 0. Please, check your configuration file.");
    return

  if not os.path.exists(data_dir):
    logger.error(data_dir + " does not exist.") 
    return  

  if not os.path.isfile(os.path.join(models_dir,model)):
    logger.error(os.path.join(models_dir, model) + " does not exist.") 
    return  
  
  if not os.path.exists(os.path.join(results_dir, output_folder)):
    os.mkdir(os.path.join(results_dir, output_folder)) 


  logger.info("Configure Copasi:")
  logger.info("Replicate a Copasi file configured for parameter estimation and randomise the initial parameter values") 
  pre_param_estim = RandomiseParameters(models_dir, model)
  pre_param_estim.print_parameters_to_estimate()
  pre_param_estim.generate_instances_from_template(nfits)
  

  logger.info("\n")
  logger.info("Parallel parameter estimation:")
  # for some reason, CopasiSE ignores the "../" for the data file and assumes that the Data folder is inside the Models folder..
  # Let's temporarily copy this folder and then delete it.
  if os.path.exists(os.path.join(models_dir, data_folder)):
    os.rename(os.path.join(models_dir, data_folder), os.path.join(models_dir, data_folder+"_{:%Y%m%d%H%M%S}".format(datetime.datetime.now())))
  shutil.copytree(data_dir, os.path.join(models_dir, data_folder))

  copasi = get_copasi()
  if copasi == None:
    logger.error("CopasiSE not found! Please check that CopasiSE is installed and in the PATH environmental variable.")
    return
  
  timestamp = "{:%Y%m%d%H%M%S}".format(datetime.datetime.now())
  command = copasi + " -s "+os.path.join(models_dir, model[:-4]+timestamp+".cps")+" "+os.path.join(models_dir, model[:-4]+timestamp+".cps")
  parallel_computation(command, timestamp, cluster_type, nfits, results_dir, pp_cpus)

  # remove the previously copied Data folder
  shutil.rmtree(os.path.join(models_dir, data_folder), ignore_errors=True) 

  # Move the files to the results_dir
  tmpFiles = os.listdir(tmp_dir)
  for file in tmpFiles:
    shutil.move(os.path.join(tmp_dir, file), os.path.join(results_dir, output_folder, file))

