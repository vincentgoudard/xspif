#include <AudioUnit/AudioUnit.r>

// Note that resource IDs must be spaced 2 apart for the 'STR' name and description
#define kAudioUnitResID_Comp				10000

// So you need to define these appropriately for your audio unit.
// For the name the convention is to provide your company name and end it with a ':',
// then provide the name of the AudioUnit.
// The Description can be whatever you want.
// For an effect unit the Type and SubType should be left the way they are defined here...
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// SampleEffectUnit
#define RES_ID			kAudioUnitResID_Comp
#define COMP_TYPE		'aufx'
#define COMP_SUBTYPE		'MCMP'
#define COMP_MANUF		'mdsp'
#define VERSION			0x00010000
#define NAME			"mdsp @ smartelectronix: Compressor"
#define DESCRIPTION		"Compressor"
#define ENTRY_POINT		"CompEntry"

#include "AUResources.r"
