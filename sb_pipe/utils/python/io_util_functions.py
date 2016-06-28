#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of sb_pipe.
#
# sb_pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sb_pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2010-07-13 12:14:32 $
# $Id: latex_report.py,v 1.0 2010-07-13 12:45:32 Piero Dalle Pezze Exp $



# Personal I/O utilities


import sys
import os, glob
from numpy import *
import scipy.stats



reload(sys)  
sys.setdefaultencoding('utf8')

# Return the line number (as string) of the first occurrence of pattern in filename
def get_pattern_position(pattern, filename):
  with open(filename) as myFile:
    for num, line in enumerate(myFile, 1):
      if pattern in line:
	#print(str(num) + " : " + pattern)
	return str(num)
  #print(str(-1) + " : " + pattern)
  return str(-1)



# Return all files with a certain pattern in folder+subdirectories
def files_with_pattern_recur(folder, pattern):
   for dirname, subdirs, files in os.walk(folder):
      for f in files:
         if f.endswith(pattern):
            yield os.path.join(dirname, f)



# Print the matrix results stored in data in an output file
def write_matrix_on_file(path, filename_out, data):
  # Open output file
  file_out = open(path + "/" + filename_out, "w")
  for row in data:
    for item in row:
      file_out.write(str(item) + "\t")
    file_out.write("\n")
  file_out.close()
  
  
  # replace a string with another in file_out  
def replace_string_in_file(file_out, old_string, new_string):
  # Read in the file
  filedata = None
  with open(file_out, 'r') as file :
    filedata = file.read()
  # Replace the target string
  filedata = filedata.replace(old_string, new_string)
  # Write the file out again
  with open(file_out, 'w') as file:
    file.write(filedata)

