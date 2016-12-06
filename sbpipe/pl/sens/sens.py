#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sbpipe.
#
# sbpipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sbpipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with sbpipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2015-05-30 16:14:32 $


# for computing the pipeline elapsed time 
import datetime
import glob
import logging
import os
import subprocess
from ..pipeline import Pipeline
from sbpipe.utils.io import refresh
from sbpipe.report.latex_reports import latex_report_sim, pdf_report

logger = logging.getLogger('sbpipe')


class Sens(Pipeline):
    """
    This module provides the user with a complete pipeline of scripts for computing 
    model sensitivity analysis.
    """

    def __init__(self, data_folder='Data', models_folder='Models', working_folder='Working_Folder',
                 sim_data_folder='sensitivity_data', sim_plots_folder='sensitivity_plots'):
        __doc__ = Pipeline.__init__.__doc__

        Pipeline.__init__(self, data_folder, models_folder, working_folder, sim_data_folder, sim_plots_folder)
        self.__sensitivities_dir = "sensitivities"

    def run(self, config_file):
        __doc__ = Pipeline.run.__doc__

        logger.info("Reading file " + config_file + " : \n")

        # variable initialisation
        try:
            (generate_data, analyse_data, generate_report,
             project_dir, simulator, model) = self.config_parser(config_file, "sensitivity")
        except Exception as e:
            logger.error(e.message)
            import traceback
            logger.debug(traceback.format_exc())
            return False

        models_dir = os.path.join(project_dir, self.get_models_folder())
        outputdir = os.path.join(project_dir, self.get_working_folder(), os.path.splitext(model)[0], self.__sensitivities_dir)

        # Get the pipeline start time
        start = datetime.datetime.now().replace(microsecond=0)

        logger.info("\n")
        logger.info("Processing model " + model)
        logger.info("#############################################################")
        logger.info("")

        # preprocessing
        # remove the folder the previous results if any
        # filesToDelete = glob.glob(os.path.join(sensitivities_dir, "*.png"))
        # for f in filesToDelete:
        #     os.remove(f)
        if not os.path.exists(outputdir):
            os.mkdir(outputdir)

        if generate_data:
            logger.info("\n")
            logger.info("Data generation:")
            logger.info("################")
            status = Sens.generate_data(simulator,
                                        model,
                                        self.get_models_dir(),
                                        outputdir)
            if not status:
                return False

        if analyse_data:
            logger.info("\n")
            logger.info("Data analysis:")
            logger.info("##############")
            status = Sens.analyse_data(outputdir)
            if not status:
                return False

        if generate_report:
            logger.info("\n")
            logger.info("Report generation:")
            logger.info("##################")
            status = Sens.generate_report(model, outputdir, self.get_sim_plots_folder())
            if not status:
                return False

        # Print the pipeline elapsed time
        end = datetime.datetime.now().replace(microsecond=0)
        logger.info("\n\nPipeline elapsed time (using Python datetime): " + str(end - start))

        if len(glob.glob(os.path.join(outputdir, '*.csv'))) > 0:
            return True
        return False

    @classmethod
    def generate_data(cls, simulator, model, inputdir, outputdir):
        """
        The first pipeline step: data generation.

        :param simulator: the name of the simulator (e.g. Copasi)
        :param model: the model to process
        :param inputdir: the directory containing the model
        :param outputdir: the directory to store the results
        :return: True if the task was completed successfully, False otherwise.
        """
        if not os.path.isfile(os.path.join(inputdir, model)):
            logger.error(os.path.join(inputdir, model) + " does not exist.")
            return False

        # folder preparation
        refresh(outputdir, os.path.splitext(model)[0])

        # execute runs simulations.
        logger.info("Sensitivity analysis for " + model)
        try:
            sim = cls.get_simul_obj(simulator)
            sim.sensitivity_analysis(model, inputdir, outputdir)
        except Exception as e:
            logger.error("simulator: " + simulator + " not found.")
            import traceback
            logger.debug(traceback.format_exc())
            return False
        return True

    # Input parameters
    # outputdir
    @classmethod
    def analyse_data(cls, outputdir):
        """
        The second pipeline step: data analysis.

        :param outputdir: the directory to store the performed analysis.
        :return: True if the task was completed successfully, False otherwise.
        """
        p = subprocess.Popen(['Rscript', os.path.join(os.path.dirname(__file__), 'sens_plot.r'),
                              outputdir])
        p.wait()
        return True

    @classmethod
    def generate_report(cls, model, outputdir, sim_plots_folder):
        """
        The third pipeline step: report generation.

        :param model: the model name
        :param outputdir: the directory to store the report
        :param sim_plots_folder: the directory containing the time courses results combined with experimental data
        :return: True if the task was completed successfully, False otherwise.
        """
        if not os.path.exists(os.path.join(outputdir, sim_plots_folder)):
            logger.error("input_dir " + os.path.join(outputdir, sim_plots_folder) +
                         " does not exist. Analyse the data first.")
            return False

        logger.info("Generating LaTeX report")
        filename_prefix = "report__sensitivity_"
        latex_report_sim(outputdir, sim_plots_folder, model, filename_prefix)

        logger.info("Generating PDF report")
        pdf_report(outputdir, filename_prefix + model + ".tex")
        return True

    def read_config(self, lines):
        __doc__ = Pipeline.read_config.__doc__

        # parse common options
        (generate_data, analyse_data, generate_report,
         project_dir, model) = self.read_common_config(lines)

        # default values
        simulator = 'Copasi'

        # Initialises the variables
        for line in lines:
            logger.info(line)
            if line[0] == "simulator":
                simulator = line[1]
            break

        return (generate_data, analyse_data, generate_report,
                project_dir, simulator, model)
