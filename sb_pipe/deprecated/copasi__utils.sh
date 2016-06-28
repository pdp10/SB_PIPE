#!/bin/bash
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
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2013-04-20 12:14:32 $
#
#
# Utilities for changing column names generated by copasi time course reports






# Replaces a group of annotation strings from a generated copasi report file
# Input parameters
# path:		The path of the copasi report
# report_name:	The name of the report
function replace_str_copasi_sim_report()
{
  local path=$1
  local report=$2

  local str_time1="\[Time\]"
  local str_time2="# Time"
  local str_time0="Time"
  local str_pn="\[ParticleNumber\]"
  local str_conc="\[Concentration\]"
  local str_initpn="\[InitialParticleNumber\]"
  local str_initconc="\[InitialConcentration\]"  
  local str_value="\[Value\]"

  local str_values="Values\["
  local str_initvalue="].InitialValue"   
  
  local str_flux1=".Flux"
  local str_flux0="_Flux"  
  local str_rate1=".Rate"
  local str_rate0="_Rate"  
  
  
  
  local str_open_square_bracket="\["
  local str_close_square_bracket="\]"    
  local str_open_parenthesis="("
  local str_close_parenthesis=")"    

  local str_null=""

  
  
  
  

  # Replace the previous strings in the following file:
  local report_with_path="${path}/${report%.*}.csv"


  # "s/.*${str_time1} means "every thing before ${str_time1}
  #sed -i "s/.*${str_time1}/${str_time0}/g" ${report_with_path}
  # This variant keeps the string in \(.*\t\) and put in \1 . Therefore, it removes every character 
  # before [Time] and after the \t.
  # 1,2 means only to the first two lines. Leave it in case a newline was wrongly inserted in the header
  # 1,2 is a great optimisation in this context.
  sed -i "1,2s/\(.*\t\).*${str_time1}/\1${str_time0}/g" ${report_with_path}  
  sed -i "1,2s/${str_time2}/${str_time0}/" ${report_with_path}
  sed -i "1,2s/${str_pn}/${str_null}/g" ${report_with_path}
  sed -i "1,2s/${str_conc}/${str_null}/g" ${report_with_path}
  sed -i "1,2s/${str_initpn}/${str_null}/g" ${report_with_path}
  sed -i "1,2s/${str_initconc}/${str_null}/g" ${report_with_path}  
  sed -i "1,2s/${str_value}/${str_null}/g" ${report_with_path}

  
  sed -i "1,2s/${str_values}/${str_null}/g" ${report_with_path}
  sed -i "1,2s/${str_initvalue}/${str_null}/g" ${report_with_path}  
  sed -i "1,2s/${str_flux1}/${str_flux0}/g" ${report_with_path}
  sed -i "1,2s/${str_rate1}/${str_rate0}/g" ${report_with_path}

  
  
  
  # leave this in the end as it plays on [] and ()
  sed -i "1,2s/${str_open_square_bracket}/${str_null}/g" ${report_with_path}
  sed -i "1,2s/${str_close_square_bracket}/${str_null}/g" ${report_with_path}
  sed -i "1,2s/${str_open_parenthesis}/${str_null}/g" ${report_with_path}
  sed -i "1,2s/${str_close_parenthesis}/${str_null}/g" ${report_with_path}  
  
}