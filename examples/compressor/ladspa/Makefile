
###############################################################################
# XSPIF: cross(X) Standard PlugIn Framework:
# This makefile is generated automatically by the module "ladspa.py"
# and from the file: compressor.xspif
#

###############################################################################
# INSTALLATION DIRECTORIES
#
# Change these if you want to install somewhere else. In particularly
# you may wish to remove the middle "local/" part of each entry.


INSTALL_PLUGINS_DIR	=	/usr/local/lib/ladspa/
INSTALL_INCLUDE_DIR	=	/usr/include/
#INSTALL_BINARY_DIR	=	/usr/local/bin/

###############################################################################
#
# GENERAL
#

NAME		=       compressor
INCLUDES	=	-I$(LADSPA_PATH) -I. -I..
LIBRARIES	=	-ldl -lm
CFLAGS		=	$(INCLUDES) -DPD -O3 -Wall -funroll-loops -fPIC -Wno-unused -Wno-parentheses -Wno-switch
CXXFLAGS	=	$(CFLAGS)
SRC		=	$(NAME).ladspa.c
OBJ		=	$(NAME).ladspa.o
PLUGIN		=	$(NAME).ladspa.so
CC		=	cc
CPP		=	c++

###############################################################################
#
# RULES TO BUILD PLUGINS FROM C OR C++ CODE
#
$(PLUGIN):	$(OBJ)
	$(LD) -o $(PLUGIN) $(OBJ) -shared

$(OBJ):	$(SRC)
	$(CC) $(CFLAGS) -o $(OBJ) -c $(SRC)


# For now, all LADSPA plugins generated with XSPIF are in C
# $(PLUGIN):	$(SRC) $(OBJ) ladspa.h
# 	$(CPP) $(CXXFLAGS) -o $*.o -c $*.cpp
# 	$(CPP) -o $*.ladspa.so $*.ladspa.o -shared

###############################################################################
#
# TARGETS
#

install:	$(PLUGIN)
	cp      $(PLUGIN) $(LADSPA_PATH)

targets:	$(PLUGIN)

###############################################################################
#
# UTILITIES
#

clean:
	-rm -f `find . -name "*.o"`
	-rm -f `find .. -name "*~"`
	-rm -f `find .. -name "core*"`

###############################################################################

