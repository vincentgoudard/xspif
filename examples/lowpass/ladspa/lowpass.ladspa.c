/****************************************************************
XSPIF: cross(X) Standard PlugIn Framework: XSPIF to LADSPA
	examples/lowpass.ladspa.c

 A simple lowpass with saturation
 This is a comment to test the xml framework
 Some comments about Input
 Some comments about Ouput
 This file is generated automatically from the file: examples/lowpass.xml
	plugin ID: 'lowp'
	manufacturer ID: 'ReMu'
	maker: Remy Muller
	copyright: GPL
****************************************************************/



#include <stdlib.h>
#include <string.h>
#include "ladspa.h"




/****************************************************************/
// Macro for getting the sample rate
#undef XSPIF_GET_SAMPLE_RATE()
#define XSPIF_GET_SAMPLE_RATE() (plugin_data->sample_rate)
// Macro for getting the vector_size
#undef XSPIF_GET_VECTOR_SIZE()
#define XSPIF_GET_VECTOR_SIZE() (sample_count)



/****************************************************************/

#include <math.h>
/******************************************/
/* Put all independent code here */
float saturate(float x)
{
if(x>0.f)
    x = 2.f*x-x*x;
else
    x=  2.f*x + x*x;
return x;
}
/******************************************/
    



/****************************************************************/
// States declared in the <code> section can only be blobal
// Otherwise, they cannot be accessed in the process functon

      // could do some things here...
      



/****************************************************************/
/* Audio and parameters ports */
#define INPUT1		0
#define INPUT2		1
#define OUTPUT1		2
#define OUTPUT2		3
#define CUTOFF		4



/****************************************************************/
static LADSPA_Descriptor *lowpassDescriptor = NULL;



/****************************************************************/
// The plugin structure 
typedef struct {

	LADSPA_Data sample_rate;
	// Pointers to the ports:
	LADSPA_Data *m_pfinput1;
	LADSPA_Data *m_pfinput2;
	LADSPA_Data *m_pfoutput1;
	LADSPA_Data *m_pfoutput2;
	LADSPA_Data *m_pfcutoff;

	// Internal copy of the parameters:
	float cutoff;

	// Parameters last value:
	float last_cutoff;

	// Internal states:
	float lp2;
	float lp1;
	float lambda;
	LADSPA_Data run_adding_gain;
}LowPass;



/****************************************************************/
const LADSPA_Descriptor *ladspa_descriptor(unsigned long index) {

	switch (index) {
	case 0:
		return lowpassDescriptor;
	default:
		return NULL;
	}
}



/****************************************************************/
// Initialise and activate a plugin instance.
static void activateLowPass(LADSPA_Handle instance) {

	LowPass *plugin_data = (LowPass*)instance;
	// States:
	float lp2 = plugin_data->lp2;
	float lp1 = plugin_data->lp1;
	float lambda = plugin_data->lambda;
	{

    // nothing to do here... 
    	}
}



/****************************************************************/
/* Cleanup is the "de-instantiate" function.
Free the memory allocated in "instantiate" in this function */
static void cleanupLowPass(LADSPA_Handle instance) {

	LowPass* plugin_data = (LowPass*)instance;
	// States:
	float lp2 = plugin_data->lp2;
	float lp1 = plugin_data->lp1;
	float lambda = plugin_data->lambda;
	{

    
	}
	free(instance);
}



/****************************************************************/
static void connectPortLowPass( LADSPA_Handle instance,
                                unsigned long port,
                                LADSPA_Data *data) {

	LowPass *plugin;

	plugin = (LowPass *)instance;
	switch (port) {
	case INPUT1:
		plugin->m_pfinput1 = data;
		break;
	case INPUT2:
		plugin->m_pfinput2 = data;
		break;
	case OUTPUT1:
		plugin->m_pfoutput1 = data;
		break;
	case OUTPUT2:
		plugin->m_pfoutput2 = data;
		break;
	case CUTOFF:
		plugin->m_pfcutoff = data;
		break;
	}
}



/****************************************************************/
static LADSPA_Handle instantiateLowPass( const LADSPA_Descriptor *descriptor,
                                         unsigned long s_rate) {

	LowPass *plugin_data = (LowPass *)malloc(sizeof(LowPass));
	float lp2;
	float lp1;
	float lambda;
		plugin_data->sample_rate =(LADSPA_Data)s_rate;
	{
		
    lambda = lp1 = lp2 = 0.;
    
	}
	plugin_data->lp2 = lp2;
	plugin_data->lp1 = lp1;
	plugin_data->lambda = lambda;

	return (LADSPA_Handle)plugin_data;
}



/****************************************************************/
// Macro for run-adding processing
#undef XSPIF_WRITE_SAMPLE
#define XSPIF_WRITE_SAMPLE(dest, index, source) ((dest)[(index)] = (source))



/****************************************************************/
static void runLowPass(LADSPA_Handle instance,
                       unsigned long sample_count) {

	LowPass *plugin_data = (LowPass*)instance;

	/*cutoff (Hz)*/
	const LADSPA_Data cutoff = *(plugin_data->m_pfcutoff);
	/* Audio input: input1*/
	const LADSPA_Data * const input1 = plugin_data->m_pfinput1;

	/* Audio input: input2*/
	const LADSPA_Data * const input2 = plugin_data->m_pfinput2;

	/* Audio input: output1*/
	LADSPA_Data * const output1 = plugin_data->m_pfoutput1;

	/* Audio input: output2*/
	LADSPA_Data * const output2 = plugin_data->m_pfoutput2;

	// Parameters last value:
	float last_cutoff = plugin_data->last_cutoff;

	// States:
	float lp2 = plugin_data->lp2;
	float lp1 = plugin_data->lp1;
	float lambda = plugin_data->lambda;

	if (cutoff != last_cutoff) {

      // cutoff and samplerate are both in Hertz
      lambda = exp(- cutoff / XSPIF_GET_SAMPLE_RATE()); 
      
		plugin_data->last_cutoff = cutoff;
	}


// Here is the DSP algorithm:
	{

    for(int i=0;i < XSPIF_GET_VECTOR_SIZE();i++)
    {
         // in and out names are derived from the label in the pin declaration
         lp1 = (1.f-lambda)*input1[i] + lambda*lp1;
         lp2 = (1.f-lambda)*input2[i] + lambda*lp2;
	 XSPIF_WRITE_SAMPLE(output1, i, saturate(lp1));
	 XSPIF_WRITE_SAMPLE(output2, i, saturate(lp2));  
    }
    	
}
}



/****************************************************************/
// Macro for run-adding processing
#undef XSPIF_WRITE_SAMPLE
#define XSPIF_WRITE_SAMPLE(dest, index, source) ((dest)[(index)] += (source))



/****************************************************************/
static void setRunAddingGainLowPass(LADSPA_Handle instance,
			LADSPA_Data gain) {

	((LowPass*)instance)->run_adding_gain = gain;
}



/****************************************************************/
static void runAddingLowPass(LADSPA_Handle instance, unsigned long sample_count) {

	LowPass *plugin_data = (LowPass*)instance;
	LADSPA_Data run_adding_gain = plugin_data->run_adding_gain;

	/*cutoff (Hz)*/
	const LADSPA_Data cutoff = *(plugin_data->m_pfcutoff);
	/* Audio input: input1*/
	const LADSPA_Data * const input1 = plugin_data->m_pfinput1;

	/* Audio input: input2*/
	const LADSPA_Data * const input2 = plugin_data->m_pfinput2;

	/* Audio input: output1*/
	LADSPA_Data * const output1 = plugin_data->m_pfoutput1;

	/* Audio input: output2*/
	LADSPA_Data * const output2 = plugin_data->m_pfoutput2;

	// Parameters last value:
	float last_cutoff = plugin_data->last_cutoff;

	// States:
	float lp2 = plugin_data->lp2;
	float lp1 = plugin_data->lp1;
	float lambda = plugin_data->lambda;

	if (cutoff != last_cutoff) {

      // cutoff and samplerate are both in Hertz
      lambda = exp(- cutoff / XSPIF_GET_SAMPLE_RATE()); 
      
		plugin_data->last_cutoff = cutoff;
	}


// Here is the DSP algorithm:
	{

    for(int i=0;i < XSPIF_GET_VECTOR_SIZE();i++)
    {
         // in and out names are derived from the label in the pin declaration
         lp1 = (1.f-lambda)*input1[i] + lambda*lp1;
         lp2 = (1.f-lambda)*input2[i] + lambda*lp2;
	 XSPIF_WRITE_SAMPLE(output1, i, saturate(lp1));
	 XSPIF_WRITE_SAMPLE(output2, i, saturate(lp2));  
    }
    	
}
}



/****************************************************************/
/* _init() is called automatically when the plugin library is first loaded. */
void _init() {

	char **port_names;
	LADSPA_PortDescriptor *port_descriptors;
	LADSPA_PortRangeHint *port_range_hints;

	lowpassDescriptor = 
	  (LADSPA_Descriptor *)malloc(sizeof(LADSPA_Descriptor));

	if (lowpassDescriptor) {
		lowpassDescriptor->UniqueID = 'lowp';
		lowpassDescriptor->Label = strdup("LowPass");
		lowpassDescriptor->Name = strdup("LowPass");
		lowpassDescriptor->Maker = strdup("Remy Muller");
		lowpassDescriptor->Copyright = strdup("GPL");
		lowpassDescriptor->PortCount = 5;

		port_descriptors = (LADSPA_PortDescriptor *)calloc(5,
		 sizeof(LADSPA_PortDescriptor));
		lowpassDescriptor->PortDescriptors =
		(const LADSPA_PortDescriptor *)port_descriptors;

		port_range_hints = (LADSPA_PortRangeHint *)calloc(5,
		 sizeof(LADSPA_PortRangeHint));
		lowpassDescriptor->PortRangeHints =
		 (const LADSPA_PortRangeHint *)port_range_hints;

		port_names = (char **)calloc(5, sizeof(char*));
		lowpassDescriptor->PortNames =
		 (const char **)port_names;

		/* Parameters for cutoff (Hz) */
		port_descriptors[CUTOFF] =
		 LADSPA_PORT_INPUT | LADSPA_PORT_CONTROL;
		port_names[CUTOFF] =
		 strdup("cutoff (Hz)");
		port_range_hints[CUTOFF].HintDescriptor =
		 LADSPA_HINT_BOUNDED_BELOW | LADSPA_HINT_BOUNDED_ABOVE | LADSPA_HINT_DEFAULT_MIDDLE;
		port_range_hints[CUTOFF].LowerBound = 100.0;
		port_range_hints[CUTOFF].UpperBound = 10000.0;
;

		/* Parameters for Input */
		port_descriptors[INPUT1] =
		 LADSPA_PORT_INPUT | LADSPA_PORT_AUDIO;
		port_names[INPUT1] =
		 strdup("Input");
		port_range_hints[INPUT1].HintDescriptor = 0;

		/* Parameters for Input */
		port_descriptors[INPUT2] =
		 LADSPA_PORT_INPUT | LADSPA_PORT_AUDIO;
		port_names[INPUT2] =
		 strdup("Input");
		port_range_hints[INPUT2].HintDescriptor = 0;

		/* Parameters for Output */
		port_descriptors[OUTPUT1] =
		 LADSPA_PORT_OUTPUT | LADSPA_PORT_AUDIO;
		port_names[OUTPUT1] =
		 strdup("Output");
		port_range_hints[OUTPUT1].HintDescriptor = 0;

		/* Parameters for Output */
		port_descriptors[OUTPUT2] =
		 LADSPA_PORT_OUTPUT | LADSPA_PORT_AUDIO;
		port_names[OUTPUT2] =
		 strdup("Output");
		port_range_hints[OUTPUT2].HintDescriptor = 0;

		lowpassDescriptor->activate = activateLowPass;
		lowpassDescriptor->cleanup = cleanupLowPass;
		lowpassDescriptor->connect_port = connectPortLowPass;
		lowpassDescriptor->deactivate = NULL;
		lowpassDescriptor->instantiate = instantiateLowPass;
		lowpassDescriptor->run = runLowPass;
		lowpassDescriptor->run_adding = NULL;
		lowpassDescriptor->set_run_adding_gain = NULL;
	}
}



/****************************************************************/
/* _fini() is called automatically when the library is unloaded. */
void _fini() {

 	int i;
 	if (lowpassDescriptor) {
 	 	free((char *)lowpassDescriptor->Label);
 	 	free((char *)lowpassDescriptor->Name);
 	 	free((char *)lowpassDescriptor->Maker);
 	 	free((char *)lowpassDescriptor->Copyright);
 	 	free((LADSPA_PortDescriptor *)lowpassDescriptor->PortDescriptors);
 	 	for (i = 0; i < lowpassDescriptor->PortCount; i++)
 	 	 	free((char *)(lowpassDescriptor->PortNames[i]));
 	 	free((char **)lowpassDescriptor->PortNames);
 	 	free((LADSPA_PortRangeHint *)lowpassDescriptor->PortRangeHints);
 	 	free(lowpassDescriptor);
 	}
}
