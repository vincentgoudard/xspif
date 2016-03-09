/****************************************************************
XSPIF: cross(X) Standard PlugIn Framework: XSPIF to LADSPA
  compressor.ladspa.c

 This file is generated automatically from the file: compressor.xspif
  plugin ID: 'MCMP'
  manufacturer ID: 'mdsp'
  maker: mdsp @ smartelectronix
  copyright: GPL
****************************************************************/



#include <stdlib.h>
#include <string.h>
#include "ladspa.h"




/****************************************************************/
// Macro for getting the sample rate
#undef XSPIF_GET_SAMPLE_RATE
#define XSPIF_GET_SAMPLE_RATE() (plugin_data->sample_rate)
// Macro for getting the vector_size
#undef XSPIF_GET_VECTOR_SIZE
#define XSPIF_GET_VECTOR_SIZE() (sample_count)



/****************************************************************/

#include <math.h>
    



/****************************************************************/
/* Audio and parameters ports */
#define PORT_INPUT1    0
#define PORT_INPUT2    1
#define PORT_OUTPUT1    2
#define PORT_OUTPUT2    3
#define PORT_ATTACK    4
#define PORT_RELEASE    5
#define PORT_THRESHOLD    6
#define PORT_RATIO    7
#define PORT_PREAMP    8
#define PORT_VOLUME    9



/****************************************************************/
static LADSPA_Descriptor *compDescriptor = NULL;



/****************************************************************/
// The plugin structure 
typedef struct {

  LADSPA_Data sample_rate;
  // Pointers to the ports:
  LADSPA_Data *m_pfinput1;
  LADSPA_Data *m_pfinput2;
  LADSPA_Data *m_pfoutput1;
  LADSPA_Data *m_pfoutput2;
  LADSPA_Data *m_pfattack;
  LADSPA_Data *m_pfrelease;
  LADSPA_Data *m_pfthreshold;
  LADSPA_Data *m_pfratio;
  LADSPA_Data *m_pfpreamp;
  LADSPA_Data *m_pfvolume;

  // Internal copy of the parameters and its last value:
  float attack;
  float _last_attack;
  float release;
  float _last_release;
  float threshold;
  float _last_threshold;
  float ratio;
  float _last_ratio;
  float preamp;
  float _last_preamp;
  float volume;
  float _last_volume;

  // Internal states:
  float ga;
  float gr;
  float cThres;
  float cSlope;
  float boost;
  float makeup;
  float last_peak;
  float last_gain;
  float attenuation;
  LADSPA_Data run_adding_gain;
}Comp;



/****************************************************************/
const LADSPA_Descriptor *ladspa_descriptor(unsigned long index) {

  switch (index) {
  case 0:
    return compDescriptor;
  default:
    return NULL;
  }
}



/****************************************************************/
// Deactivate a plugin instance.
static void deactivateComp(LADSPA_Handle instance) {

  Comp *plugin_data = (Comp*)instance;
  // Get the states from plugin's structure:
  float ga = plugin_data->ga;
  float gr = plugin_data->gr;
  float cThres = plugin_data->cThres;
  float cSlope = plugin_data->cSlope;
  float boost = plugin_data->boost;
  float makeup = plugin_data->makeup;
  float last_peak = plugin_data->last_peak;
  float last_gain = plugin_data->last_gain;
  float attenuation = plugin_data->attenuation;
  // Get the params from plugin's structure:
  const LADSPA_Data attack = *(plugin_data->m_pfattack);
  const LADSPA_Data release = *(plugin_data->m_pfrelease);
  const LADSPA_Data threshold = *(plugin_data->m_pfthreshold);
  const LADSPA_Data ratio = *(plugin_data->m_pfratio);
  const LADSPA_Data preamp = *(plugin_data->m_pfpreamp);
  const LADSPA_Data volume = *(plugin_data->m_pfvolume);

  // Code from callback <deactivate> of XSPIF meta-plugin
  {

    last_peak = last_gain = 0;    
    
  }
  // Update the states in plugin's structure:
  plugin_data->ga = ga;
  plugin_data->gr = gr;
  plugin_data->cThres = cThres;
  plugin_data->cSlope = cSlope;
  plugin_data->boost = boost;
  plugin_data->makeup = makeup;
  plugin_data->last_peak = last_peak;
  plugin_data->last_gain = last_gain;
  plugin_data->attenuation = attenuation;

}



/****************************************************************/
/* Cleanup is the "de-instantiate" function.
Free the memory allocated in "instantiate" in this function */
static void cleanupComp(LADSPA_Handle instance) {

  Comp* plugin_data = (Comp*)instance;
  free(instance);
}



/****************************************************************/
static void connectPortComp( LADSPA_Handle instance,
                             unsigned long port,
                             LADSPA_Data *data) {

  Comp *plugin;

  plugin = (Comp *)instance;
  switch (port) {
  case PORT_INPUT1:
    plugin->m_pfinput1 = data;
    break;
  case PORT_INPUT2:
    plugin->m_pfinput2 = data;
    break;
  case PORT_OUTPUT1:
    plugin->m_pfoutput1 = data;
    break;
  case PORT_OUTPUT2:
    plugin->m_pfoutput2 = data;
    break;
  case PORT_ATTACK:
    plugin->m_pfattack = data;
    break;
  case PORT_RELEASE:
    plugin->m_pfrelease = data;
    break;
  case PORT_THRESHOLD:
    plugin->m_pfthreshold = data;
    break;
  case PORT_RATIO:
    plugin->m_pfratio = data;
    break;
  case PORT_PREAMP:
    plugin->m_pfpreamp = data;
    break;
  case PORT_VOLUME:
    plugin->m_pfvolume = data;
    break;
  }
}



/****************************************************************/
static LADSPA_Handle instantiateComp( const LADSPA_Descriptor *descriptor,
                                      unsigned long s_rate) {

  Comp *plugin_data = (Comp *)malloc(sizeof(Comp));

  // States:
  float ga;
  float gr;
  float cThres;
  float cSlope;
  float boost;
  float makeup;
  float last_peak;
  float last_gain;
  float attenuation;
    plugin_data->sample_rate =(LADSPA_Data)s_rate;
  // Code from callback <instantiate> of XSPIF meta-plugin
  {

    ga = gr = boost = attenuation = makeup = cSlope = cThres = 0;
    last_peak = last_gain = 0;
    
  }
  // Update the states in plugin's structure:
  plugin_data->ga = ga;
  plugin_data->gr = gr;
  plugin_data->cThres = cThres;
  plugin_data->cSlope = cSlope;
  plugin_data->boost = boost;
  plugin_data->makeup = makeup;
  plugin_data->last_peak = last_peak;
  plugin_data->last_gain = last_gain;
  plugin_data->attenuation = attenuation;

  return (LADSPA_Handle)plugin_data;
}



/****************************************************************/
// Macro for run-replacing processing
#undef XSPIF_WRITE_SAMPLE
#define XSPIF_WRITE_SAMPLE(dest, index, source) ((dest)[(index)] = (source))



/****************************************************************/
static void runComp(LADSPA_Handle instance,
                    unsigned long sample_count) {

  Comp *plugin_data = (Comp*)instance;

  /*Attack*/
  const LADSPA_Data attack = *(plugin_data->m_pfattack);
  float _last_attack = plugin_data->_last_attack;
  /*Release*/
  const LADSPA_Data release = *(plugin_data->m_pfrelease);
  float _last_release = plugin_data->_last_release;
  /*Threshold*/
  const LADSPA_Data threshold = *(plugin_data->m_pfthreshold);
  float _last_threshold = plugin_data->_last_threshold;
  /*Ratio*/
  const LADSPA_Data ratio = *(plugin_data->m_pfratio);
  float _last_ratio = plugin_data->_last_ratio;
  /*Preamp*/
  const LADSPA_Data preamp = *(plugin_data->m_pfpreamp);
  float _last_preamp = plugin_data->_last_preamp;
  /*Volume*/
  const LADSPA_Data volume = *(plugin_data->m_pfvolume);
  float _last_volume = plugin_data->_last_volume;

  /* Audio input: input1*/
  const LADSPA_Data * const input1 = plugin_data->m_pfinput1;

  /* Audio input: input2*/
  const LADSPA_Data * const input2 = plugin_data->m_pfinput2;

  /* Audio output: output1*/
  LADSPA_Data * const output1 = plugin_data->m_pfoutput1;

  /* Audio output: output2*/
  LADSPA_Data * const output2 = plugin_data->m_pfoutput2;

  // Get the states from plugin's structure:
  float ga = plugin_data->ga;
  float gr = plugin_data->gr;
  float cThres = plugin_data->cThres;
  float cSlope = plugin_data->cSlope;
  float boost = plugin_data->boost;
  float makeup = plugin_data->makeup;
  float last_peak = plugin_data->last_peak;
  float last_gain = plugin_data->last_gain;
  float attenuation = plugin_data->attenuation;

  // Check if param changed and perform necessary conversions if any:
  if (attack != _last_attack) {

      // 2.2 is the compensation factor to define attack time as t90-t10
      ga = (float)exp(-2.2/(XSPIF_GET_SAMPLE_RATE()*(attack*0.001))); 
      
    plugin_data->_last_attack = attack;
  }
  if (release != _last_release) {

      // 2.2 is the compensation factor to define attack time as t90-t10
      gr = (float)exp(-2.2/(XSPIF_GET_SAMPLE_RATE()*(release*0.001)));
      
    plugin_data->_last_release = release;
  }
  if (threshold != _last_threshold) {

      cThres = pow(10.0,threshold/20);
      makeup = pow(10.0, -(threshold*cSlope)/20.0);
      
    plugin_data->_last_threshold = threshold;
  }
  if (ratio != _last_ratio) {

      cSlope = 1.0 - 1.0/ratio; // 2:1 <-> 40:1
      makeup = pow(10.0, -(threshold*cSlope)/20.0);
      
    plugin_data->_last_ratio = ratio;
  }
  if (preamp != _last_preamp) {

      boost = pow(10.,preamp/20.0);
      
    plugin_data->_last_preamp = preamp;
  }
  if (volume != _last_volume) {

      attenuation = pow(10.,volume/20.0);
      
    plugin_data->_last_volume = volume;
  }

  // Code from callback <process> of XSPIF meta-plugin
  {

    float gain, delta_peak, in1, in2;
    int i;
    for(i=0;i < XSPIF_GET_VECTOR_SIZE();i++)
    {
      in1 = boost * input1[i];
      in2 = boost * input2[i];
      
      // get peak data: 
      // if greater than last peak, add difference filtered with attack time
      // else let decay with release time
      delta_peak = 0.5*(fabs(in1) + fabs(in2)) - last_peak;
      if (delta_peak<0) delta_peak = 0;
      last_peak *= gr;
      last_peak += (1.0-ga)*delta_peak;

      if(last_peak>cThres)
	gain = pow(last_peak/cThres, - cSlope); //compression
      else 
	gain = 1.f; // no compression

      //filter w/ attack and release
      if(last_gain < gain)
	{
	  last_gain *= 1.0-ga;
	  last_gain += ga*gain;
	}
      else
	{
	  last_gain *= 1.0-gr;
	  last_gain += gr*gain;
	}
      
      // write y(n) = postamp * g(n) * makeup * x(n)
      XSPIF_WRITE_SAMPLE( output1, i, attenuation * last_gain * makeup * in1);
      XSPIF_WRITE_SAMPLE( output2, i, attenuation * last_gain * makeup * in2);
    } 
    
  }
  // Update the states in plugin's structure:
  plugin_data->ga = ga;
  plugin_data->gr = gr;
  plugin_data->cThres = cThres;
  plugin_data->cSlope = cSlope;
  plugin_data->boost = boost;
  plugin_data->makeup = makeup;
  plugin_data->last_peak = last_peak;
  plugin_data->last_gain = last_gain;
  plugin_data->attenuation = attenuation;
}



/****************************************************************/
// Macro for run-adding processing
#undef XSPIF_WRITE_SAMPLE
#define XSPIF_WRITE_SAMPLE(dest, index, source) ((dest)[(index)] += (source))



/****************************************************************/
static void setRunAddingGainComp(LADSPA_Handle instance,
      LADSPA_Data gain) {

  ((Comp*)instance)->run_adding_gain = gain;
}



/****************************************************************/
static void runAddingComp(LADSPA_Handle instance, unsigned long sample_count) {

  Comp *plugin_data = (Comp*)instance;
  LADSPA_Data run_adding_gain = plugin_data->run_adding_gain;

  /*Attack*/
  const LADSPA_Data attack = *(plugin_data->m_pfattack);
  float _last_attack = plugin_data->_last_attack;
  /*Release*/
  const LADSPA_Data release = *(plugin_data->m_pfrelease);
  float _last_release = plugin_data->_last_release;
  /*Threshold*/
  const LADSPA_Data threshold = *(plugin_data->m_pfthreshold);
  float _last_threshold = plugin_data->_last_threshold;
  /*Ratio*/
  const LADSPA_Data ratio = *(plugin_data->m_pfratio);
  float _last_ratio = plugin_data->_last_ratio;
  /*Preamp*/
  const LADSPA_Data preamp = *(plugin_data->m_pfpreamp);
  float _last_preamp = plugin_data->_last_preamp;
  /*Volume*/
  const LADSPA_Data volume = *(plugin_data->m_pfvolume);
  float _last_volume = plugin_data->_last_volume;

  /* Audio input: input1*/
  const LADSPA_Data * const input1 = plugin_data->m_pfinput1;

  /* Audio input: input2*/
  const LADSPA_Data * const input2 = plugin_data->m_pfinput2;

  /* Audio input: output1*/
  LADSPA_Data * const output1 = plugin_data->m_pfoutput1;

  /* Audio input: output2*/
  LADSPA_Data * const output2 = plugin_data->m_pfoutput2;

  // Get the states from plugin's structure:
  float ga = plugin_data->ga;
  float gr = plugin_data->gr;
  float cThres = plugin_data->cThres;
  float cSlope = plugin_data->cSlope;
  float boost = plugin_data->boost;
  float makeup = plugin_data->makeup;
  float last_peak = plugin_data->last_peak;
  float last_gain = plugin_data->last_gain;
  float attenuation = plugin_data->attenuation;

  // Check if param changed and perform necessary conversions if any:
  if (attack != _last_attack) {

      // 2.2 is the compensation factor to define attack time as t90-t10
      ga = (float)exp(-2.2/(XSPIF_GET_SAMPLE_RATE()*(attack*0.001))); 
      
    plugin_data->_last_attack = attack;
  }
  if (release != _last_release) {

      // 2.2 is the compensation factor to define attack time as t90-t10
      gr = (float)exp(-2.2/(XSPIF_GET_SAMPLE_RATE()*(release*0.001)));
      
    plugin_data->_last_release = release;
  }
  if (threshold != _last_threshold) {

      cThres = pow(10.0,threshold/20);
      makeup = pow(10.0, -(threshold*cSlope)/20.0);
      
    plugin_data->_last_threshold = threshold;
  }
  if (ratio != _last_ratio) {

      cSlope = 1.0 - 1.0/ratio; // 2:1 <-> 40:1
      makeup = pow(10.0, -(threshold*cSlope)/20.0);
      
    plugin_data->_last_ratio = ratio;
  }
  if (preamp != _last_preamp) {

      boost = pow(10.,preamp/20.0);
      
    plugin_data->_last_preamp = preamp;
  }
  if (volume != _last_volume) {

      attenuation = pow(10.,volume/20.0);
      
    plugin_data->_last_volume = volume;
  }

  // Code from callback <process> of XSPIF meta-plugin
  {

    float gain, delta_peak, in1, in2;
    int i;
    for(i=0;i < XSPIF_GET_VECTOR_SIZE();i++)
    {
      in1 = boost * input1[i];
      in2 = boost * input2[i];
      
      // get peak data: 
      // if greater than last peak, add difference filtered with attack time
      // else let decay with release time
      delta_peak = 0.5*(fabs(in1) + fabs(in2)) - last_peak;
      if (delta_peak<0) delta_peak = 0;
      last_peak *= gr;
      last_peak += (1.0-ga)*delta_peak;

      if(last_peak>cThres)
	gain = pow(last_peak/cThres, - cSlope); //compression
      else 
	gain = 1.f; // no compression

      //filter w/ attack and release
      if(last_gain < gain)
	{
	  last_gain *= 1.0-ga;
	  last_gain += ga*gain;
	}
      else
	{
	  last_gain *= 1.0-gr;
	  last_gain += gr*gain;
	}
      
      // write y(n) = postamp * g(n) * makeup * x(n)
      XSPIF_WRITE_SAMPLE( output1, i, attenuation * last_gain * makeup * in1);
      XSPIF_WRITE_SAMPLE( output2, i, attenuation * last_gain * makeup * in2);
    } 
    
  }
  // Update the states in plugin's structure:
  plugin_data->ga = ga;
  plugin_data->gr = gr;
  plugin_data->cThres = cThres;
  plugin_data->cSlope = cSlope;
  plugin_data->boost = boost;
  plugin_data->makeup = makeup;
  plugin_data->last_peak = last_peak;
  plugin_data->last_gain = last_gain;
  plugin_data->attenuation = attenuation;
}



/****************************************************************/
/* _init() is called automatically when the plugin library is first loaded. */
void _init() {

  char **port_names;
  LADSPA_PortDescriptor *port_descriptors;
  LADSPA_PortRangeHint *port_range_hints;

  compDescriptor = 
    (LADSPA_Descriptor *)malloc(sizeof(LADSPA_Descriptor));

  if (compDescriptor) {
    compDescriptor->UniqueID = 'MCMP';
    compDescriptor->Label = strdup("Comp");
    compDescriptor->Name = strdup("Compressor");
    compDescriptor->Maker = strdup("mdsp @ smartelectronix");
    compDescriptor->Copyright = strdup("GPL");
    compDescriptor->PortCount = 10;

    port_descriptors = (LADSPA_PortDescriptor *)calloc(10,
     sizeof(LADSPA_PortDescriptor));
    compDescriptor->PortDescriptors =
    (const LADSPA_PortDescriptor *)port_descriptors;

    port_range_hints = (LADSPA_PortRangeHint *)calloc(10,
     sizeof(LADSPA_PortRangeHint));
    compDescriptor->PortRangeHints =
     (const LADSPA_PortRangeHint *)port_range_hints;

    port_names = (char **)calloc(10, sizeof(char*));
    compDescriptor->PortNames =
     (const char **)port_names;

    /* Parameters for Attack */
    port_descriptors[PORT_ATTACK] =
     LADSPA_PORT_INPUT | LADSPA_PORT_CONTROL;
    port_names[PORT_ATTACK] =
     strdup("Attack");
    port_range_hints[PORT_ATTACK].HintDescriptor =
     LADSPA_HINT_BOUNDED_BELOW | LADSPA_HINT_BOUNDED_ABOVE | LADSPA_HINT_DEFAULT_MINIMUM;
    port_range_hints[PORT_ATTACK].LowerBound = 10.0;
    port_range_hints[PORT_ATTACK].UpperBound = 50.0;


    /* Parameters for Release */
    port_descriptors[PORT_RELEASE] =
     LADSPA_PORT_INPUT | LADSPA_PORT_CONTROL;
    port_names[PORT_RELEASE] =
     strdup("Release");
    port_range_hints[PORT_RELEASE].HintDescriptor =
     LADSPA_HINT_BOUNDED_BELOW | LADSPA_HINT_BOUNDED_ABOVE | LADSPA_HINT_DEFAULT_MIDDLE;
    port_range_hints[PORT_RELEASE].LowerBound = 10.0;
    port_range_hints[PORT_RELEASE].UpperBound = 500.0;


    /* Parameters for Threshold */
    port_descriptors[PORT_THRESHOLD] =
     LADSPA_PORT_INPUT | LADSPA_PORT_CONTROL;
    port_names[PORT_THRESHOLD] =
     strdup("Threshold");
    port_range_hints[PORT_THRESHOLD].HintDescriptor =
     LADSPA_HINT_BOUNDED_BELOW | LADSPA_HINT_BOUNDED_ABOVE | LADSPA_HINT_DEFAULT_MIDDLE;
    port_range_hints[PORT_THRESHOLD].LowerBound = -40.0;
    port_range_hints[PORT_THRESHOLD].UpperBound = 0.0;


    /* Parameters for Ratio */
    port_descriptors[PORT_RATIO] =
     LADSPA_PORT_INPUT | LADSPA_PORT_CONTROL;
    port_names[PORT_RATIO] =
     strdup("Ratio");
    port_range_hints[PORT_RATIO].HintDescriptor =
     LADSPA_HINT_BOUNDED_BELOW | LADSPA_HINT_BOUNDED_ABOVE | LADSPA_HINT_DEFAULT_MIDDLE;
    port_range_hints[PORT_RATIO].LowerBound = 1.0;
    port_range_hints[PORT_RATIO].UpperBound = 40.0;


    /* Parameters for Preamp */
    port_descriptors[PORT_PREAMP] =
     LADSPA_PORT_INPUT | LADSPA_PORT_CONTROL;
    port_names[PORT_PREAMP] =
     strdup("Preamp");
    port_range_hints[PORT_PREAMP].HintDescriptor =
     LADSPA_HINT_BOUNDED_BELOW | LADSPA_HINT_BOUNDED_ABOVE | LADSPA_HINT_DEFAULT_MINIMUM;
    port_range_hints[PORT_PREAMP].LowerBound = 0.0;
    port_range_hints[PORT_PREAMP].UpperBound = 40.0;


    /* Parameters for Volume */
    port_descriptors[PORT_VOLUME] =
     LADSPA_PORT_INPUT | LADSPA_PORT_CONTROL;
    port_names[PORT_VOLUME] =
     strdup("Volume");
    port_range_hints[PORT_VOLUME].HintDescriptor =
     LADSPA_HINT_BOUNDED_BELOW | LADSPA_HINT_BOUNDED_ABOVE | LADSPA_HINT_DEFAULT_MAXIMUM;
    port_range_hints[PORT_VOLUME].LowerBound = -40.0;
    port_range_hints[PORT_VOLUME].UpperBound = 0.0;


    /* Parameters for PORT_input1 */
    port_descriptors[PORT_INPUT1] =
     LADSPA_PORT_INPUT | LADSPA_PORT_AUDIO;
    port_names[PORT_INPUT1] =
     strdup("Input");
    port_range_hints[PORT_INPUT1].HintDescriptor = 0;

    /* Parameters for PORT_input2 */
    port_descriptors[PORT_INPUT2] =
     LADSPA_PORT_INPUT | LADSPA_PORT_AUDIO;
    port_names[PORT_INPUT2] =
     strdup("Input");
    port_range_hints[PORT_INPUT2].HintDescriptor = 0;

    /* Parameters for PORT_output1 */
    port_descriptors[PORT_OUTPUT1] =
     LADSPA_PORT_OUTPUT | LADSPA_PORT_AUDIO;
    port_names[PORT_OUTPUT1] =
     strdup("Output");
    port_range_hints[PORT_OUTPUT1].HintDescriptor = 0;

    /* Parameters for PORT_output2 */
    port_descriptors[PORT_OUTPUT2] =
     LADSPA_PORT_OUTPUT | LADSPA_PORT_AUDIO;
    port_names[PORT_OUTPUT2] =
     strdup("Output");
    port_range_hints[PORT_OUTPUT2].HintDescriptor = 0;

    compDescriptor->instantiate = instantiateComp;
    compDescriptor->cleanup = NULL;
    compDescriptor->activate = NULL;
    compDescriptor->deactivate = deactivateComp;
    compDescriptor->connect_port = connectPortComp;
    compDescriptor->run = runComp;
    compDescriptor->run_adding = runAddingComp;
    compDescriptor->set_run_adding_gain = setRunAddingGainComp;
  }
}



/****************************************************************/
/* _fini() is called automatically when the library is unloaded. */
void _fini() {

 	int i;
 	if (compDescriptor) {
 	 	free((char *)compDescriptor->Label);
 	 	free((char *)compDescriptor->Name);
 	 	free((char *)compDescriptor->Maker);
 	 	free((char *)compDescriptor->Copyright);
 	 	free((LADSPA_PortDescriptor *)compDescriptor->PortDescriptors);
 	 	for (i = 0; i < compDescriptor->PortCount; i++)
 	 	 	free((char *)(compDescriptor->PortNames[i]));
 	 	free((char **)compDescriptor->PortNames);
 	 	free((LADSPA_PortRangeHint *)compDescriptor->PortRangeHints);
 	 	free(compDescriptor);
 	}
}
