# GNU MakeFile 
# Karaparambil Rajan Rebin                  # Date: 23 Jun 2023
#library files : "-lMinuit" for Tminuit and "-lgsl -lgslcblas" for gsl

APP      = Run_Getfigure

SRCEXT   = cpp
SRCDIR   = ./
OBJDIR   = ./
BINDIR   = ./

SRCS    := $(shell find $(SRCDIR) -name '*.$(SRCEXT)' )
SRCDIRS := $(shell find . -name '*.$(SRCEXT)' -exec dirname {} \; | uniq)
OBJS    := $(patsubst %.$(SRCEXT),$(OBJDIR)/%.o,$(SRCS))


EXTRALIBS += `root-config --glibs` 

DEBUG    = 
INCLUDES = -I./include -I `root-config --incdir`  
CFLAGS   = -c $(DEBUG) $(INCLUDES) -O3
LDFLAGS  = `root-config --libs`  -lGeom -lMinuit -lgsl -lgslcblas


CC = g++
ifeq ($(CC),)
CC = g++
endif

.PHONY: all clean distclean

all: $(BINDIR)/$(APP)

$(BINDIR)/$(APP): buildrepo $(OBJS)
	@mkdir -p `dirname $@`
	@echo "Linking $@..."
	@$(CC) $(OBJS) $(LDFLAGS) -o $@

$(OBJDIR)/%.o: %.$(SRCEXT)
	@echo "Compiling $<..."
	@$(CC) $(CFLAGS) $< -o $@

clean:
	$(RM) -r  $(APP) $(OBJS)

distclean: clean
	$(RM) -r 

buildrepo:
	@$(call make-repo)

define make-repo
   for dir in $(SRCDIRS); \
   do \
	mkdir -p $(OBJDIR)/$$dir; \
   done
endef

# usage: $(call make-depend,source-file,object-file,depend-file)
define make-depend
  $(CC) -MM       \
        -MF $3    \
        -MP       \
        -MT $2    \
        $(CFLAGS) \
        $1
endef
