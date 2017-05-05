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
# $Date: 2015-07-13 12:14:32 $

# Utilities to generate Latex code. These functions are used for reporting purposes.

import logging
import sys
import os
import re
import subprocess
from sbpipe.utils.re_utils import nat_sort_key
from sbpipe.sbpipe_config import which

logger = logging.getLogger('sbpipe')


def get_latex_header(pdftitle="SBpipe report", title="SBpipe report", abstract="Generic report."):
    """
    Initialize a Latex header with a title and an abstract.
    
    :param pdftitle: the pdftitle for the LaTeX header
    :param title: the title for the LaTeX header
    :param abstract: the abstract for the LaTeX header
    :return: the LaTeX header
    """
    return (
        "\\documentclass[10pt,a4paper]{article}\n"
        "\\usepackage[top=2.54cm,bottom=2.54cm,left=3.17cm,right=3.17cm]{geometry}\n"
        "\\usepackage{graphicx}\n"
        "\\usepackage[plainpages=false,pdfauthor={Generated with SBpipe},pdftitle={" + pdftitle + "},pdftex]"
                                                                                                   "{hyperref}\n"
                                                                                                   "\\author{Generated with SBpipe} \n"
                                                                                                   "\\title{" + title + "}\n"
                                                                                                                        "\\date{\\today}\n"
                                                                                                                        "\\begin{document}\n"
                                                                                                                        "\\maketitle\n"
                                                                                                                        "\\begin{abstract}\n" + abstract + " \n\\end{abstract}\n"
    )


def latex_report_ps1(outputdir, plots_folder, filename_prefix, model_noext, scanned_par):
    """
    Generate a report for a single parameter scan task.
    
    :param outputdir: the output directory
    :param plots_folder: the folder containing the simulated plots
    :param filename_prefix: the prefix for the LaTeX file
    :param model_noext: the model name
    :param scanned_par: the scanned parameter
    """
    with open(os.path.join(outputdir, filename_prefix + model_noext + ".tex"), "w") as file_out:
        model_name = model_noext[:].replace("_", " ")
        scanned_par_name = scanned_par[0:].replace("_", " ")
        logger.info("Model: " + model_name)
        logger.info("Scanning parameter: " + scanned_par)
        # writing on file
        # Get latex header
        header = get_latex_header("Report: " + model_name,
                                  "Report: " + model_name,
                                  "Report for {\\it " + model_name + "}, scanning {\\it " + scanned_par_name + "}.")
        file_out.write(header)
        logger.info("Files in " + os.path.join(outputdir, plots_folder) + ":")
        file_out.write("\\section*{Plots - Scanning parameter " + scanned_par_name + "}\n")
        files = [f for f in os.listdir(os.path.join(outputdir, plots_folder)) if f.endswith('.png')]
        files.sort()
        # we sort using the __eval_ pattern in files
        files.sort(key=lambda x: x.split("__eval_")[1])
        for infile in files:
            if infile.find(model_noext) != -1:
                logger.info(infile)
                file_out.write("\\includegraphics[width=2in]{" + plots_folder +
                               "/{" + infile.replace('.png', '') + "}.png}\n")
                file_out.write("\\hfill\n")
        file_out.write("\\end{document}\n")


def latex_report_ps2(outputdir, plots_folder, filename_prefix, model_noext,
                     scanned_par1, scanned_par2):
    """
    Generate a report for a double parameter scan task.
    
    :param outputdir: the output directory
    :param plots_folder: the folder containing the simulated plots
    :param filename_prefix: the prefix for the LaTeX file
    :param model_noext: the model name
    :param scanned_par1: the 1st scanned parameter
    :param scanned_par2: the 2nd scanned parameter
    """
    with open(os.path.join(outputdir, filename_prefix + model_noext + ".tex"), "w") as file_out:
        model_name = model_noext[:].replace("_", " ")
        scanned_par1_name = scanned_par1[0:].replace("_", " ")
        scanned_par2_name = scanned_par2[0:].replace("_", " ")
        logger.info("Model: " + model_name)
        logger.info("Scanning parameters: " + scanned_par1_name + " and " + scanned_par2_name)
        # writing on file
        # Get latex header
        header = get_latex_header("Report: " + model_name,
                                  "Report: " + model_name,
                                  "Report for {\\it " + model_name + "}, scanning {\\it " +
                                  scanned_par1_name + "} and {\\it " + scanned_par2_name + "}.")
        file_out.write(header)
        logger.info("Files in " + os.path.join(outputdir, plots_folder) + ":")
        file_out.write("\\section*{Plots - Scanning parameters " + scanned_par1_name + " and " +
                       scanned_par2_name + "}\n")
        folder = [f for f in os.listdir(os.path.join(outputdir, plots_folder)) if f.endswith('.png')]
        folder.sort(key=nat_sort_key)
        prev_readout = ''
        for infile in folder:
            if infile.find(model_noext) != -1:
                try:
                    curr_readout = re.search('__eval_(.+?)__tp_', infile).group(1)
                except AttributeError:
                    curr_readout = 'Unknown readout'
                if curr_readout != prev_readout:
                    logger.debug("Adding plots for: " + curr_readout)
                    file_out.write("\\subsection*{Readout: " + curr_readout.replace("_", " ") + "}\n")
                    prev_readout = curr_readout

                logger.info(infile)
                file_out.write("\\includegraphics[width=2in]{" + plots_folder +
                               "/{" + infile.replace('.png', '') + "}.png}\n")
                file_out.write("\\hfill\n")
        file_out.write("\\end{document}\n")


def latex_report_sim(outputdir, plots_folder, model_noext, filename_prefix):
    """
    Generate a report for a time course task.
    
    :param outputdir: the output directory
    :param plots_folder: the folder containing the simulated plots
    :param model_noext: the model name
    :param filename_prefix: the prefix for the LaTeX file
    """
    with open(os.path.join(outputdir, filename_prefix + model_noext + ".tex"), "w") as file_out:
        model_name = model_noext[:].replace("_", " ")
        logger.info(model_name)
        # writing on file
        # Get latex header
        header = get_latex_header("Report: " + model_name,
                                  "Report: " + model_name,
                                  "Report for {\\it " + model_name + "}.")
        file_out.write(header)
        logger.info("Files in " + os.path.join(outputdir, plots_folder) + ":")
        file_out.write("\\section*{Plots}\n")
        folder = [f for f in os.listdir(os.path.join(outputdir, plots_folder)) if f.endswith('.png')]
        folder.sort()
        for infile in folder:
            if infile.find(model_noext) != -1:
                # if infile.find('mean_sd_ci95') != -1:
                logger.info(infile)
                file_out.write("\\includegraphics[width=2in]{" + plots_folder +
                               "/{" + infile.replace('.png', '') + "}.png}\n")
        file_out.write("\\end{document}\n")


def latex_report_pe(outputdir, plots_folder, model_noext, filename_prefix):
    """
    Generate a report for a parameter estimation task.
    
    :param outputdir: the output directory
    :param plots_folder: the folder containing the simulated plots
    :param model_noext: the model name
    :param filename_prefix: the prefix for the LaTeX file
    """
    with open(os.path.join(outputdir, filename_prefix + model_noext + ".tex"), "w") as file_out:
        model_name = model_noext[:].replace("_", " ")
        logger.info(model_name)
        # writing on file
        # Get latex header
        header = get_latex_header("Report: " + model_name,
                                  "Report: " + model_name,
                                  "Parameter estimation report for {\\it " + model_name + "}.")
        file_out.write(header)
        logger.info("Files in " + os.path.join(outputdir, plots_folder) + ":")
        file_out.write("\\section*{Plots}\n")
        folder = [f for f in os.listdir(os.path.join(outputdir, plots_folder)) if f.endswith('.png')]
        folder.sort()
        begin_figure = False
        figure_num = 0
        figures_per_page = 12
        for infile in folder:
            logger.info(infile)
            figure_num += 1
            if not begin_figure:
                file_out.write("\\begin{figure}[!ht]\n")
                begin_figure = True
            file_out.write("\\begin{minipage}{0.31\\textwidth}\n")
            file_out.write("\\includegraphics[width=\\textwidth]{" + plots_folder +
                           "/{" + infile.replace('.png', '') + "}.png}\n")
            file_out.write("\\end{minipage}\n")
            file_out.write("\\hfill\n")
            if figure_num % figures_per_page == 0 and begin_figure:
                file_out.write("\\end{figure}\n")
                file_out.write("\\newpage\n")
                begin_figure = False
                figures_per_page = 18
                figure_num = 0
        if begin_figure:
            file_out.write("\\end{figure}\n")
        file_out.write("\\end{document}\n")


def latex_report(outputdir, plots_folder, model_noext, filename_prefix, caption=False):
    """
    Generate a generic report.
    
    :param outputdir: the output directory
    :param plots_folder: the folder containing the simulated plots
    :param model_noext: the model name
    :param filename_prefix: the prefix for the LaTeX file
    :param caption: True if figure captions (=figure file name) should be added
    """
    with open(os.path.join(outputdir, filename_prefix + model_noext + ".tex"), "w") as file_out:
        model_name = model_noext[:].replace("_", " ")
        logger.info(model_name)
        # writing on file
        # Get latex header
        header = get_latex_header("Report: " + model_name,
                                  "Report: " + model_name,
                                  "Generic report for {\\it " + model_name + "}.")
        file_out.write(header)
        logger.info("Files in " + os.path.join(outputdir, plots_folder) + ":")
        file_out.write("\\section*{Plots}\n")
        files = [f for f in os.listdir(os.path.join(outputdir, plots_folder)) if f.endswith('.png')]
        files.sort()
        begin_figure = False
        figure_num = 0
        figures_per_page = 9
        for infile in files:
            logger.info(infile)
            figure_num += 1
            if not begin_figure:
                file_out.write("\\begin{figure}[!ht]\n")
                begin_figure = True
            file_out.write("\\begin{minipage}{0.31\\textwidth}\n")
            file_out.write("\\includegraphics[width=\\textwidth]{" + plots_folder +
                           "/{" + infile.replace('.png', '') + "}.png}\n")
            if caption:
                file_out.write("\\caption{" + infile.replace(model_noext, "").replace("_", " ")[:-4] + "}\n")
            file_out.write("\\end{minipage}\n")
            file_out.write("\\hfill\n")
            if figure_num % figures_per_page == 0 and begin_figure:
                file_out.write("\\end{figure}\n")
                file_out.write("\\newpage\n")
                begin_figure = False
                figures_per_page = 15
                figure_num = 0
        if begin_figure:
            file_out.write("\\end{figure}\n")
        file_out.write("\\end{document}\n")


def pdf_report(outputdir, filename):
    """
    Generate a PDF report from LaTeX report using pdflatex.
    
    :param outputdir: the output directory
    :param filename: the LaTeX file name
    """
    pdflatex = which("pdflatex")
    if pdflatex is None:
        logger.error("pdflatex not found! pdflatex must be installed for pdf reports.")
        return
    currdir = os.getcwd()
    os.chdir(outputdir)
    logger.info(pdflatex + " -halt-on-error " + filename + " ... ")
    # We suppress the output of pdflatex completely
    try:
        from subprocess import DEVNULL  # python3
    except ImportError:
        DEVNULL = open(os.devnull, 'wb')

    if sys.version_info > (3,):
        with subprocess.Popen([pdflatex, "-halt-on-error", filename], stdout=DEVNULL, stderr=subprocess.STDOUT) as p:
            p.communicate()[0]
        with subprocess.Popen([pdflatex, "-halt-on-error", filename], stdout=DEVNULL, stderr=subprocess.STDOUT) as p:
            p.communicate()[0]
    else:
        p = subprocess.Popen([pdflatex, "-halt-on-error", filename], stdout=DEVNULL, stderr=subprocess.STDOUT)
        p = subprocess.Popen([pdflatex, "-halt-on-error", filename], stdout=DEVNULL, stderr=subprocess.STDOUT)
        p.communicate()[0]
    os.chdir(currdir)




