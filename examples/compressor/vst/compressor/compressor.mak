# Microsoft Developer Studio Generated NMAKE File, Based on compressor.dsp
!IF "$(CFG)" == ""
CFG=compressor - Win32 Debug
!MESSAGE No configuration specified. Defaulting to compressor - Win32 Debug.
!ENDIF 

!IF "$(CFG)" != "compressor - Win32 Release" && "$(CFG)" != "compressor - Win32 Debug"
!MESSAGE Invalid configuration "$(CFG)" specified.
!MESSAGE You can specify a configuration when running NMAKE
!MESSAGE by defining the macro CFG on the command line. For example:
!MESSAGE 
!MESSAGE NMAKE /f "compressor.mak" CFG="compressor - Win32 Debug"
!MESSAGE 
!MESSAGE Possible choices for configuration are:
!MESSAGE 
!MESSAGE "compressor - Win32 Release" (based on "Win32 (x86) Dynamic-Link Library")
!MESSAGE "compressor - Win32 Debug" (based on "Win32 (x86) Dynamic-Link Library")
!MESSAGE 
!ERROR An invalid configuration is specified.
!ENDIF 

!IF "$(OS)" == "Windows_NT"
NULL=
!ELSE 
NULL=nul
!ENDIF 

CPP=cl.exe
MTL=midl.exe
RSC=rc.exe

!IF  "$(CFG)" == "compressor - Win32 Release"

OUTDIR=.\Release
INTDIR=.\Release

ALL : "d:\Program Files\Steinberg\Cubase SX\Vstplugins\mdsp\compressor.dll"


CLEAN :
	-@erase "$(INTDIR)\aeffguieditor.obj"
	-@erase "$(INTDIR)\AudioEffect.obj"
	-@erase "$(INTDIR)\audioeffectx.obj"
	-@erase "$(INTDIR)\compEditor.obj"
	-@erase "$(INTDIR)\compressor.vst.obj"
	-@erase "$(INTDIR)\dfxguimulticontrols.obj"
	-@erase "$(INTDIR)\vc60.idb"
	-@erase "$(INTDIR)\vstcontrols.obj"
	-@erase "$(INTDIR)\vstgui.obj"
	-@erase "$(OUTDIR)\compressor.exp"
	-@erase "$(OUTDIR)\compressor.lib"
	-@erase "d:\Program Files\Steinberg\Cubase SX\Vstplugins\mdsp\compressor.dll"

"$(OUTDIR)" :
    if not exist "$(OUTDIR)/$(NULL)" mkdir "$(OUTDIR)"

CPP_PROJ=/nologo /MT /W3 /GX /Ox /Ot /Oa /Og /Op /D "WIN32" /D "NDEBUG" /D "_WINDOWS" /D "_MBCS" /D "_USRDLL" /D "COMPRESSOR_EXPORTS" /Fp"$(INTDIR)\compressor.pch" /YX /Fo"$(INTDIR)\\" /Fd"$(INTDIR)\\" /FD /c 
MTL_PROJ=/nologo /D "NDEBUG" /mktyplib203 /win32 
BSC32=bscmake.exe
BSC32_FLAGS=/nologo /o"$(OUTDIR)\compressor.bsc" 
BSC32_SBRS= \
	
LINK32=link.exe
LINK32_FLAGS=kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib /nologo /dll /incremental:no /pdb:"$(OUTDIR)\compressor.pdb" /machine:I386 /def:"..\compressor.vst.def" /out:"d:\Program Files\Steinberg\Cubase SX\Vstplugins\mdsp\compressor.dll" /implib:"$(OUTDIR)\compressor.lib" 
DEF_FILE= \
	"..\compressor.vst.def"
LINK32_OBJS= \
	"$(INTDIR)\AudioEffect.obj" \
	"$(INTDIR)\audioeffectx.obj" \
	"$(INTDIR)\compressor.vst.obj" \
	"$(INTDIR)\compEditor.obj" \
	"$(INTDIR)\vstcontrols.obj" \
	"$(INTDIR)\aeffguieditor.obj" \
	"$(INTDIR)\vstgui.obj" \
	"$(INTDIR)\dfxguimulticontrols.obj"

"d:\Program Files\Steinberg\Cubase SX\Vstplugins\mdsp\compressor.dll" : "$(OUTDIR)" $(DEF_FILE) $(LINK32_OBJS)
    $(LINK32) @<<
  $(LINK32_FLAGS) $(LINK32_OBJS)
<<

!ELSEIF  "$(CFG)" == "compressor - Win32 Debug"

OUTDIR=.\Debug
INTDIR=.\Debug
# Begin Custom Macros
OutDir=.\Debug
# End Custom Macros

ALL : "d:\Program Files\Steinberg\Cubase SX\Vstplugins\mdsp\compressor.dll" "$(OUTDIR)\compressor.bsc"


CLEAN :
	-@erase "$(INTDIR)\aeffguieditor.obj"
	-@erase "$(INTDIR)\aeffguieditor.sbr"
	-@erase "$(INTDIR)\AudioEffect.obj"
	-@erase "$(INTDIR)\AudioEffect.sbr"
	-@erase "$(INTDIR)\audioeffectx.obj"
	-@erase "$(INTDIR)\audioeffectx.sbr"
	-@erase "$(INTDIR)\compEditor.obj"
	-@erase "$(INTDIR)\compEditor.sbr"
	-@erase "$(INTDIR)\compressor.vst.obj"
	-@erase "$(INTDIR)\compressor.vst.sbr"
	-@erase "$(INTDIR)\dfxguimulticontrols.obj"
	-@erase "$(INTDIR)\dfxguimulticontrols.sbr"
	-@erase "$(INTDIR)\vc60.idb"
	-@erase "$(INTDIR)\vc60.pdb"
	-@erase "$(INTDIR)\vstcontrols.obj"
	-@erase "$(INTDIR)\vstcontrols.sbr"
	-@erase "$(INTDIR)\vstgui.obj"
	-@erase "$(INTDIR)\vstgui.sbr"
	-@erase "$(OUTDIR)\compressor.bsc"
	-@erase "$(OUTDIR)\compressor.exp"
	-@erase "$(OUTDIR)\compressor.lib"
	-@erase "$(OUTDIR)\compressor.pdb"
	-@erase "d:\Program Files\Steinberg\Cubase SX\Vstplugins\mdsp\compressor.dll"
	-@erase "d:\Program Files\Steinberg\Cubase SX\Vstplugins\mdsp\compressor.ilk"

"$(OUTDIR)" :
    if not exist "$(OUTDIR)/$(NULL)" mkdir "$(OUTDIR)"

CPP_PROJ=/nologo /MTd /W3 /Gm /GX /ZI /Od /D "WIN32" /D "_DEBUG" /D "_WINDOWS" /D "_MBCS" /D "_USRDLL" /D "COMPRESSOR_EXPORTS" /FR"$(INTDIR)\\" /Fp"$(INTDIR)\compressor.pch" /YX /Fo"$(INTDIR)\\" /Fd"$(INTDIR)\\" /FD /GZ /c 
MTL_PROJ=/nologo /D "_DEBUG" /mktyplib203 /win32 
BSC32=bscmake.exe
BSC32_FLAGS=/nologo /o"$(OUTDIR)\compressor.bsc" 
BSC32_SBRS= \
	"$(INTDIR)\AudioEffect.sbr" \
	"$(INTDIR)\audioeffectx.sbr" \
	"$(INTDIR)\compressor.vst.sbr" \
	"$(INTDIR)\compEditor.sbr" \
	"$(INTDIR)\vstcontrols.sbr" \
	"$(INTDIR)\aeffguieditor.sbr" \
	"$(INTDIR)\vstgui.sbr" \
	"$(INTDIR)\dfxguimulticontrols.sbr"

"$(OUTDIR)\compressor.bsc" : "$(OUTDIR)" $(BSC32_SBRS)
    $(BSC32) @<<
  $(BSC32_FLAGS) $(BSC32_SBRS)
<<

LINK32=link.exe
LINK32_FLAGS=kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib /nologo /dll /incremental:yes /pdb:"$(OUTDIR)\compressor.pdb" /debug /machine:I386 /def:"..\compressor.vst.def" /out:"d:\Program Files\Steinberg\Cubase SX\Vstplugins\mdsp\compressor.dll" /implib:"$(OUTDIR)\compressor.lib" /pdbtype:sept 
DEF_FILE= \
	"..\compressor.vst.def"
LINK32_OBJS= \
	"$(INTDIR)\AudioEffect.obj" \
	"$(INTDIR)\audioeffectx.obj" \
	"$(INTDIR)\compressor.vst.obj" \
	"$(INTDIR)\compEditor.obj" \
	"$(INTDIR)\vstcontrols.obj" \
	"$(INTDIR)\aeffguieditor.obj" \
	"$(INTDIR)\vstgui.obj" \
	"$(INTDIR)\dfxguimulticontrols.obj"

"d:\Program Files\Steinberg\Cubase SX\Vstplugins\mdsp\compressor.dll" : "$(OUTDIR)" $(DEF_FILE) $(LINK32_OBJS)
    $(LINK32) @<<
  $(LINK32_FLAGS) $(LINK32_OBJS)
<<

!ENDIF 

.c{$(INTDIR)}.obj::
   $(CPP) @<<
   $(CPP_PROJ) $< 
<<

.cpp{$(INTDIR)}.obj::
   $(CPP) @<<
   $(CPP_PROJ) $< 
<<

.cxx{$(INTDIR)}.obj::
   $(CPP) @<<
   $(CPP_PROJ) $< 
<<

.c{$(INTDIR)}.sbr::
   $(CPP) @<<
   $(CPP_PROJ) $< 
<<

.cpp{$(INTDIR)}.sbr::
   $(CPP) @<<
   $(CPP_PROJ) $< 
<<

.cxx{$(INTDIR)}.sbr::
   $(CPP) @<<
   $(CPP_PROJ) $< 
<<


!IF "$(NO_EXTERNAL_DEPS)" != "1"
!IF EXISTS("compressor.dep")
!INCLUDE "compressor.dep"
!ELSE 
!MESSAGE Warning: cannot find "compressor.dep"
!ENDIF 
!ENDIF 


!IF "$(CFG)" == "compressor - Win32 Release" || "$(CFG)" == "compressor - Win32 Debug"
SOURCE="..\..\..\..\..\..\..\Mes VST PLUGS\vstsdk2\source\common\aeffguieditor.cpp"

!IF  "$(CFG)" == "compressor - Win32 Release"


"$(INTDIR)\aeffguieditor.obj" : $(SOURCE) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ELSEIF  "$(CFG)" == "compressor - Win32 Debug"


"$(INTDIR)\aeffguieditor.obj"	"$(INTDIR)\aeffguieditor.sbr" : $(SOURCE) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ENDIF 

SOURCE="..\..\..\..\..\..\..\Mes VST PLUGS\vstsdk2\source\common\AudioEffect.cpp"

!IF  "$(CFG)" == "compressor - Win32 Release"


"$(INTDIR)\AudioEffect.obj" : $(SOURCE) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ELSEIF  "$(CFG)" == "compressor - Win32 Debug"


"$(INTDIR)\AudioEffect.obj"	"$(INTDIR)\AudioEffect.sbr" : $(SOURCE) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ENDIF 

SOURCE="..\..\..\..\..\..\..\Mes VST PLUGS\vstsdk2\source\common\audioeffectx.cpp"

!IF  "$(CFG)" == "compressor - Win32 Release"


"$(INTDIR)\audioeffectx.obj" : $(SOURCE) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ELSEIF  "$(CFG)" == "compressor - Win32 Debug"


"$(INTDIR)\audioeffectx.obj"	"$(INTDIR)\audioeffectx.sbr" : $(SOURCE) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ENDIF 

SOURCE=..\gui\compEditor.cpp

!IF  "$(CFG)" == "compressor - Win32 Release"


"$(INTDIR)\compEditor.obj" : $(SOURCE) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ELSEIF  "$(CFG)" == "compressor - Win32 Debug"


"$(INTDIR)\compEditor.obj"	"$(INTDIR)\compEditor.sbr" : $(SOURCE) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ENDIF 

SOURCE=..\compressor.vst.cpp

!IF  "$(CFG)" == "compressor - Win32 Release"


"$(INTDIR)\compressor.vst.obj" : $(SOURCE) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ELSEIF  "$(CFG)" == "compressor - Win32 Debug"


"$(INTDIR)\compressor.vst.obj"	"$(INTDIR)\compressor.vst.sbr" : $(SOURCE) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ENDIF 

SOURCE="..\..\..\..\..\..\..\smartelectronix\usr\dfx\dfx\vstplugins\dfx-library\obsolete\dfxguimulticontrols.cpp"

!IF  "$(CFG)" == "compressor - Win32 Release"


"$(INTDIR)\dfxguimulticontrols.obj" : $(SOURCE) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ELSEIF  "$(CFG)" == "compressor - Win32 Debug"


"$(INTDIR)\dfxguimulticontrols.obj"	"$(INTDIR)\dfxguimulticontrols.sbr" : $(SOURCE) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ENDIF 

SOURCE="..\..\..\..\..\..\..\Mes VST PLUGS\vstsdk2\source\common\vstcontrols.cpp"

!IF  "$(CFG)" == "compressor - Win32 Release"


"$(INTDIR)\vstcontrols.obj" : $(SOURCE) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ELSEIF  "$(CFG)" == "compressor - Win32 Debug"


"$(INTDIR)\vstcontrols.obj"	"$(INTDIR)\vstcontrols.sbr" : $(SOURCE) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ENDIF 

SOURCE="..\..\..\..\..\..\..\Mes VST PLUGS\vstsdk2\source\common\vstgui.cpp"

!IF  "$(CFG)" == "compressor - Win32 Release"


"$(INTDIR)\vstgui.obj" : $(SOURCE) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ELSEIF  "$(CFG)" == "compressor - Win32 Debug"


"$(INTDIR)\vstgui.obj"	"$(INTDIR)\vstgui.sbr" : $(SOURCE) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ENDIF 


!ENDIF 

