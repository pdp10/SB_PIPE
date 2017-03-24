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
# Object: install required dependencies automatically
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-07-27 11:48:32 $



# retrieve SBpipe package path
args <- commandArgs(trailingOnly = FALSE)
SBPIPE <- normalizePath(dirname(sub("^--file=", "", args[grep("^--file=", args)])))



    
install_r_deps <- function(x) {
    # no need to be noisy here.
    if (!suppressMessages(suppressWarnings(require(x, character.only=TRUE)))) {
        install.packages(x, dep=TRUE, repos='http://cran.r-project.org')
        if(!suppressMessages(suppressWarnings(require(x,character.only = TRUE)))) {
            print(paste("R Package", x, "not found.", sep=" "))
            FALSE
        }
    }
    TRUE
}


main <- function(args) {
   
   print("Installing R dependencies...")  

   rdeps_file <- file.path(SBPIPE, "rdeps.txt")
   if(!file.exists(rdeps_file)) {
      print(paste("Installation failed as", rdeps_file, "does not exist"))
      return(1)
   }
   rpkgs <- read.table(rdeps_file, stringsAsFactors=FALSE, encoding="utf-8")[,1]
   print(rpkgs)
   
   status <- TRUE
   for(i in 1:length(rpkgs)) {
      if(!install_r_deps(rpkgs[i])) {
	  status <- FALSE
      }
   }
   
  if(!status) {
      print("Some package was not found.")  
  } else {
      print("All packages were found. Please see the output for detail.")   
  }
  
}


main(commandArgs(TRUE))
# Clean the environment
rm ( list=ls ( ) )
