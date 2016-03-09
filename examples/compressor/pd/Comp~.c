/****************************************************************
XSPIF: cross(X) Standard PlugIn Framework: XSPIF to PD
  Comp~.c


 This file is generated automatically from the file: compressor.xspif
  plugin ID: 'MCMP'
  manufacturer ID: 'mdsp'
  maker: mdsp @ smartelectronix
  copyright: GPL
****************************************************************/



#include <stdlib.h>
#include <string.h>
#ifndef PD_VERSION
#include "m_pd.h"
#endif



/****************************************************************/

// Macro for getting the sample rate
#undef XSPIF_GET_SAMPLE_RATE
#define XSPIF_GET_SAMPLE_RATE()(sys_getsr())

// Macro for getting the vector_size
#undef XSPIF_GET_VECTOR_SIZE
#define XSPIF_GET_VECTOR_SIZE()(vector_size)

// Macro for control outputs
#undef XSPIF_CONTROLOUT
#define XSPIF_CONTROLOUT(dest, index, value)(outlet_float(dest, value))

// Macros for checking parameter fit in its range
#undef FIT_RANGE
#define FIT_RANGE(value, min, max)(((value) < min) ? min : (((value) > max) ? max : (value)))



/****************************************************************/
// add independant code here

#include <math.h>
    


/****************************************************************/
static t_class *Comp_tilde_class;

typedef struct _Comp_tilde {
  t_object  x_obj;
  t_float sample_rate;
  t_int active;

  // Internal copy of the parameters:
  t_float m_fattack;
  t_float m_frelease;
  t_float m_fthreshold;
  t_float m_fratio;
  t_float m_fpreamp;
  t_float m_fvolume;

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

  // Pointers to the outlets:

  //  Dummy variable needed for ~ objects:
  t_sample dummy_f;

} t_Comp_tilde;



/****************************************************************/
// Prototypes
void Comp_tilde_activate(t_Comp_tilde *x);
void Comp_tilde_deactivate(t_Comp_tilde *x);
static void Comp_tilde_print(t_Comp_tilde *x);



/****************************************************************/

// Output information about the plugin
static void Comp_tilde_print(t_Comp_tilde *x){

// General info about the plugin

post("
This file has been automatically generated  with XSPIF:
a (X)cross Standard PlugIn Framework
from the XML file : compressor.xspif
Plugin name : Compressor
Plugin label : Comp
Maker : mdsp @ smartelectronix
Copyright : GPL
Description :
");


post("Control input(s):");
post("(Index for controls with a dedicated inlet are hinted with a #)");
post(" #0 Attack = %f (ms)", x->m_fattack);
post("    attack, type: float, in range [10.0 ; 50.0]");
post("    with mapping (suggested): lin");
post("    Note:");
post(" #1 Release = %f (ms)", x->m_frelease);
post("    release, type: float, in range [10.0 ; 500.0]");
post("    with mapping (suggested): lin");
post("    Note:");
post(" #2 Threshold = %f (dB)", x->m_fthreshold);
post("    threshold, type: float, in range [-40.0 ; 0.0]");
post("    with mapping (suggested): lin");
post("    Note:");
post(" #3 Ratio = %f ( : 1)", x->m_fratio);
post("    ratio, type: float, in range [1.0 ; 40.0]");
post("    with mapping (suggested): lin");
post("    Note:");
post(" #4 Preamp = %f (dB)", x->m_fpreamp);
post("    preamp, type: float, in range [0.0 ; 40.0]");
post("    with mapping (suggested): lin");
post("    Note:");
post(" #5 Volume = %f (dB)", x->m_fvolume);
post("    volume, type: float, in range [-40.0 ; 0.0]");
post("    with mapping (suggested): lin");
post("    Note:");
post("Control output(s):");
post("Audio input(s):");
post(" #2 input1");
post(" #3 input2");
post("Audio output(s):");
post(" #5 output1");
post(" #4 output2");
if (x->active)
  post("Plugin ACTIVATED!");
else
  post("Plugin DEACTIVATED!");
}




/****************************************************************/
// Method responding to a change in parameter attack
static void Comp_tilde_attack(t_Comp_tilde *x, t_floatarg f){


  // Get the states from plugin's structure:
  float ga = x->ga;
  float gr = x->gr;
  float cThres = x->cThres;
  float cSlope = x->cSlope;
  float boost = x->boost;
  float makeup = x->makeup;
  float last_peak = x->last_peak;
  float last_gain = x->last_gain;
  float attenuation = x->attenuation;

  // Get the params from plugin's structure:
  float attack = x->m_fattack;
  float release = x->m_frelease;
  float threshold = x->m_fthreshold;
  float ratio = x->m_fratio;
  float preamp = x->m_fpreamp;
  float volume = x->m_fvolume;

   // Check the parameter fits its range and actualize it
  attack = FIT_RANGE(f, 10.0, 50.0);


  {

      // 2.2 is the compensation factor to define attack time as t90-t10
      ga = (float)exp(-2.2/(XSPIF_GET_SAMPLE_RATE()*(attack*0.001))); 
      
  }

  // Update attack and states in the plugin structure:
  x->m_fattack = attack;

  // Update the states in plugin's structure:
  x->ga = ga;
  x->gr = gr;
  x->cThres = cThres;
  x->cSlope = cSlope;
  x->boost = boost;
  x->makeup = makeup;
  x->last_peak = last_peak;
  x->last_gain = last_gain;
  x->attenuation = attenuation;
}



/****************************************************************/
// Method responding to a change in parameter release
static void Comp_tilde_release(t_Comp_tilde *x, t_floatarg f){


  // Get the states from plugin's structure:
  float ga = x->ga;
  float gr = x->gr;
  float cThres = x->cThres;
  float cSlope = x->cSlope;
  float boost = x->boost;
  float makeup = x->makeup;
  float last_peak = x->last_peak;
  float last_gain = x->last_gain;
  float attenuation = x->attenuation;

  // Get the params from plugin's structure:
  float attack = x->m_fattack;
  float release = x->m_frelease;
  float threshold = x->m_fthreshold;
  float ratio = x->m_fratio;
  float preamp = x->m_fpreamp;
  float volume = x->m_fvolume;

   // Check the parameter fits its range and actualize it
  release = FIT_RANGE(f, 10.0, 500.0);


  {

      // 2.2 is the compensation factor to define attack time as t90-t10
      gr = (float)exp(-2.2/(XSPIF_GET_SAMPLE_RATE()*(release*0.001)));
      
  }

  // Update release and states in the plugin structure:
  x->m_frelease = release;

  // Update the states in plugin's structure:
  x->ga = ga;
  x->gr = gr;
  x->cThres = cThres;
  x->cSlope = cSlope;
  x->boost = boost;
  x->makeup = makeup;
  x->last_peak = last_peak;
  x->last_gain = last_gain;
  x->attenuation = attenuation;
}



/****************************************************************/
// Method responding to a change in parameter threshold
static void Comp_tilde_threshold(t_Comp_tilde *x, t_floatarg f){


  // Get the states from plugin's structure:
  float ga = x->ga;
  float gr = x->gr;
  float cThres = x->cThres;
  float cSlope = x->cSlope;
  float boost = x->boost;
  float makeup = x->makeup;
  float last_peak = x->last_peak;
  float last_gain = x->last_gain;
  float attenuation = x->attenuation;

  // Get the params from plugin's structure:
  float attack = x->m_fattack;
  float release = x->m_frelease;
  float threshold = x->m_fthreshold;
  float ratio = x->m_fratio;
  float preamp = x->m_fpreamp;
  float volume = x->m_fvolume;

   // Check the parameter fits its range and actualize it
  threshold = FIT_RANGE(f, -40.0, 0.0);


  {

      cThres = pow(10.0,threshold/20);
      makeup = pow(10.0, -(threshold*cSlope)/20.0);
      
  }

  // Update threshold and states in the plugin structure:
  x->m_fthreshold = threshold;

  // Update the states in plugin's structure:
  x->ga = ga;
  x->gr = gr;
  x->cThres = cThres;
  x->cSlope = cSlope;
  x->boost = boost;
  x->makeup = makeup;
  x->last_peak = last_peak;
  x->last_gain = last_gain;
  x->attenuation = attenuation;
}



/****************************************************************/
// Method responding to a change in parameter ratio
static void Comp_tilde_ratio(t_Comp_tilde *x, t_floatarg f){


  // Get the states from plugin's structure:
  float ga = x->ga;
  float gr = x->gr;
  float cThres = x->cThres;
  float cSlope = x->cSlope;
  float boost = x->boost;
  float makeup = x->makeup;
  float last_peak = x->last_peak;
  float last_gain = x->last_gain;
  float attenuation = x->attenuation;

  // Get the params from plugin's structure:
  float attack = x->m_fattack;
  float release = x->m_frelease;
  float threshold = x->m_fthreshold;
  float ratio = x->m_fratio;
  float preamp = x->m_fpreamp;
  float volume = x->m_fvolume;

   // Check the parameter fits its range and actualize it
  ratio = FIT_RANGE(f, 1.0, 40.0);


  {

      cSlope = 1.0 - 1.0/ratio; // 2:1 <-> 40:1
      makeup = pow(10.0, -(threshold*cSlope)/20.0);
      
  }

  // Update ratio and states in the plugin structure:
  x->m_fratio = ratio;

  // Update the states in plugin's structure:
  x->ga = ga;
  x->gr = gr;
  x->cThres = cThres;
  x->cSlope = cSlope;
  x->boost = boost;
  x->makeup = makeup;
  x->last_peak = last_peak;
  x->last_gain = last_gain;
  x->attenuation = attenuation;
}



/****************************************************************/
// Method responding to a change in parameter preamp
static void Comp_tilde_preamp(t_Comp_tilde *x, t_floatarg f){


  // Get the states from plugin's structure:
  float ga = x->ga;
  float gr = x->gr;
  float cThres = x->cThres;
  float cSlope = x->cSlope;
  float boost = x->boost;
  float makeup = x->makeup;
  float last_peak = x->last_peak;
  float last_gain = x->last_gain;
  float attenuation = x->attenuation;

  // Get the params from plugin's structure:
  float attack = x->m_fattack;
  float release = x->m_frelease;
  float threshold = x->m_fthreshold;
  float ratio = x->m_fratio;
  float preamp = x->m_fpreamp;
  float volume = x->m_fvolume;

   // Check the parameter fits its range and actualize it
  preamp = FIT_RANGE(f, 0.0, 40.0);


  {

      boost = pow(10.,preamp/20.0);
      
  }

  // Update preamp and states in the plugin structure:
  x->m_fpreamp = preamp;

  // Update the states in plugin's structure:
  x->ga = ga;
  x->gr = gr;
  x->cThres = cThres;
  x->cSlope = cSlope;
  x->boost = boost;
  x->makeup = makeup;
  x->last_peak = last_peak;
  x->last_gain = last_gain;
  x->attenuation = attenuation;
}



/****************************************************************/
// Method responding to a change in parameter volume
static void Comp_tilde_volume(t_Comp_tilde *x, t_floatarg f){


  // Get the states from plugin's structure:
  float ga = x->ga;
  float gr = x->gr;
  float cThres = x->cThres;
  float cSlope = x->cSlope;
  float boost = x->boost;
  float makeup = x->makeup;
  float last_peak = x->last_peak;
  float last_gain = x->last_gain;
  float attenuation = x->attenuation;

  // Get the params from plugin's structure:
  float attack = x->m_fattack;
  float release = x->m_frelease;
  float threshold = x->m_fthreshold;
  float ratio = x->m_fratio;
  float preamp = x->m_fpreamp;
  float volume = x->m_fvolume;

   // Check the parameter fits its range and actualize it
  volume = FIT_RANGE(f, -40.0, 0.0);


  {

      attenuation = pow(10.,volume/20.0);
      
  }

  // Update volume and states in the plugin structure:
  x->m_fvolume = volume;

  // Update the states in plugin's structure:
  x->ga = ga;
  x->gr = gr;
  x->cThres = cThres;
  x->cSlope = cSlope;
  x->boost = boost;
  x->makeup = makeup;
  x->last_peak = last_peak;
  x->last_gain = last_gain;
  x->attenuation = attenuation;
}



/****************************************************************/
// Macro for process-replacing
#undef XSPIF_WRITE_SAMPLE
#define XSPIF_WRITE_SAMPLE(dest, index, value) ((dest)[(index)] = (value))



/****************************************************************/
// Macro for control outputs in the perform method : use clock
#undef XSPIF_CONTROLOUT
#define XSPIF_CONTROLOUT(dest, index, value)(Comp_tilde_controlouts(x, dest, index*1000/XSPIF_GET_SAMPLE_RATE(), value)) 



/****************************************************************/
t_int *Comp_tilde_perform(t_int *w)
{
  t_Comp_tilde *x = (t_Comp_tilde *)(w[1]);
  t_sample *input1 = (t_sample *)(w[2]);
  t_sample *input2 = (t_sample *)(w[3]);
  t_sample *output2 = (t_sample *)(w[4]);
  t_sample *output1 = (t_sample *)(w[5]);
  int vector_size = (int)(w[6]);
  if (x->active)
    {

  // Get the params from plugin's structure:
  float attack = x->m_fattack;
  float release = x->m_frelease;
  float threshold = x->m_fthreshold;
  float ratio = x->m_fratio;
  float preamp = x->m_fpreamp;
  float volume = x->m_fvolume;

  // Get the states from plugin's structure:
  float ga = x->ga;
  float gr = x->gr;
  float cThres = x->cThres;
  float cSlope = x->cSlope;
  float boost = x->boost;
  float makeup = x->makeup;
  float last_peak = x->last_peak;
  float last_gain = x->last_gain;
  float attenuation = x->attenuation;

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
  x->ga = ga;
  x->gr = gr;
  x->cThres = cThres;
  x->cSlope = cSlope;
  x->boost = boost;
  x->makeup = makeup;
  x->last_peak = last_peak;
  x->last_gain = last_gain;
  x->attenuation = attenuation;
    }
  return (w+7);
}



/****************************************************************/
// Plugin DSP method
void Comp_tilde_dsp(t_Comp_tilde *x, t_signal **sp)
{
  dsp_add(Comp_tilde_perform, 6, x,
     sp[0]->s_vec, sp[1]->s_vec, sp[2]->s_vec, sp[3]->s_vec,sp[0]->s_n);
}



/****************************************************************/
// Plugin new method
void *Comp_tilde_new(t_symbol *s, int argc, t_atom *argv)
{
  int i;
  t_float val;
  float ga;
  float gr;
  float cThres;
  float cSlope;
  float boost;
  float makeup;
  float last_peak;
  float last_gain;
  float attenuation;

  t_Comp_tilde *x = (t_Comp_tilde *)pd_new(Comp_tilde_class);
  x->sample_rate = XSPIF_GET_SAMPLE_RATE();

  // Declare the in/out-lets for the audio ports
  // Beware: 1 inlet already declared in the "CLASS_DEFAULT"
  inlet_new(&x->x_obj, &x->x_obj.ob_pd, &s_signal, &s_signal);
  outlet_new(&x->x_obj, &s_signal);
  outlet_new(&x->x_obj, &s_signal);

  // attack calls a dedicated method
  inlet_new(&x->x_obj, &x->x_obj.ob_pd, &s_float, gensym("attack"));
  // release calls a dedicated method
  inlet_new(&x->x_obj, &x->x_obj.ob_pd, &s_float, gensym("release"));
  // threshold calls a dedicated method
  inlet_new(&x->x_obj, &x->x_obj.ob_pd, &s_float, gensym("threshold"));
  // ratio calls a dedicated method
  inlet_new(&x->x_obj, &x->x_obj.ob_pd, &s_float, gensym("ratio"));
  // preamp calls a dedicated method
  inlet_new(&x->x_obj, &x->x_obj.ob_pd, &s_float, gensym("preamp"));
  // volume calls a dedicated method
  inlet_new(&x->x_obj, &x->x_obj.ob_pd, &s_float, gensym("volume"));


  // Code from callback <instantiate> of XSPIF meta-plugin
  {

    ga = gr = boost = attenuation = makeup = cSlope = cThres = 0;
    last_peak = last_gain = 0;
    
  }

  // Update the states in plugin's structure:
  x->ga = ga;
  x->gr = gr;
  x->cThres = cThres;
  x->cSlope = cSlope;
  x->boost = boost;
  x->makeup = makeup;
  x->last_peak = last_peak;
  x->last_gain = last_gain;
  x->attenuation = attenuation;

  // Get the parameters
  switch (argc)
    {
    case 0:
        Comp_tilde_attack(x, 10.0);
        Comp_tilde_release(x, 100.0);
        Comp_tilde_threshold(x, -10.0);
        Comp_tilde_ratio(x, 6.0);
        Comp_tilde_preamp(x, 0.0);
        Comp_tilde_volume(x, 0.0);
      break;
    case 6:
      {
        // Check all parameters are float
        for (i=0; i <= argc-1;i++)
          if (argv[i].a_type != A_FLOAT)
            {
              post("Comp_tilde : wrong arguments");
              return NULL;
            }
        val= atom_getfloatarg(0, argc, argv);
        Comp_tilde_attack(x, val);
        val= atom_getfloatarg(1, argc, argv);
        Comp_tilde_release(x, val);
        val= atom_getfloatarg(2, argc, argv);
        Comp_tilde_threshold(x, val);
        val= atom_getfloatarg(3, argc, argv);
        Comp_tilde_ratio(x, val);
        val= atom_getfloatarg(4, argc, argv);
        Comp_tilde_preamp(x, val);
        val= atom_getfloatarg(5, argc, argv);
        Comp_tilde_volume(x, val);
      }
      break;
    default:
      {
        post( "Comp : error in the number of arguments ( %d )", argc );
        return NULL;
      }
    }

  Comp_tilde_activate(x);
  return (void *)x;
}



/****************************************************************/
// Initialise and activate a plugin instance.
void Comp_tilde_activate(t_Comp_tilde *x) {


  // Get the states from plugin's structure:
  float ga = x->ga;
  float gr = x->gr;
  float cThres = x->cThres;
  float cSlope = x->cSlope;
  float boost = x->boost;
  float makeup = x->makeup;
  float last_peak = x->last_peak;
  float last_gain = x->last_gain;
  float attenuation = x->attenuation;

  // Get the params from plugin's structure:
  float attack = x->m_fattack;
  float release = x->m_frelease;
  float threshold = x->m_fthreshold;
  float ratio = x->m_fratio;
  float preamp = x->m_fpreamp;
  float volume = x->m_fvolume;

  // Update the states in plugin's structure:
  x->ga = ga;
  x->gr = gr;
  x->cThres = cThres;
  x->cSlope = cSlope;
  x->boost = boost;
  x->makeup = makeup;
  x->last_peak = last_peak;
  x->last_gain = last_gain;
  x->attenuation = attenuation;
  x->active = 1;
}



/****************************************************************/
// Deactivate a plugin instance (bypass).
void Comp_tilde_deactivate(t_Comp_tilde *x) {


  // Get the states from plugin's structure:
  float ga = x->ga;
  float gr = x->gr;
  float cThres = x->cThres;
  float cSlope = x->cSlope;
  float boost = x->boost;
  float makeup = x->makeup;
  float last_peak = x->last_peak;
  float last_gain = x->last_gain;
  float attenuation = x->attenuation;

  // Get the params from plugin's structure:
  float attack = x->m_fattack;
  float release = x->m_frelease;
  float threshold = x->m_fthreshold;
  float ratio = x->m_fratio;
  float preamp = x->m_fpreamp;
  float volume = x->m_fvolume;

  // Code from callback <deactivate> of XSPIF meta-plugin
  {

    last_peak = last_gain = 0;    
    
  }

  // Update the states in plugin's structure:
  x->ga = ga;
  x->gr = gr;
  x->cThres = cThres;
  x->cSlope = cSlope;
  x->boost = boost;
  x->makeup = makeup;
  x->last_peak = last_peak;
  x->last_gain = last_gain;
  x->attenuation = attenuation;
  x->active = 0;
}



/****************************************************************/
// Plugin setup method
void Comp_tilde_setup(void) {
  Comp_tilde_class = class_new(gensym("Comp~"),
    (t_newmethod)Comp_tilde_new,
    0,
    sizeof(t_Comp_tilde),
    CLASS_DEFAULT,
    A_GIMME, 0);

  class_addmethod(Comp_tilde_class,
    (t_method)Comp_tilde_dsp, gensym("dsp"), 0);
  class_addmethod(Comp_tilde_class,
    (t_method)Comp_tilde_print, gensym("print"), 0);
  class_addmethod(Comp_tilde_class,
    (t_method)Comp_tilde_activate, gensym("on"), 0);
  class_addmethod(Comp_tilde_class,
    (t_method)Comp_tilde_deactivate, gensym("off"), 0);

  // Declare a method for the parameter attack
  class_addmethod(Comp_tilde_class,
    (t_method)Comp_tilde_attack, gensym("attack"), A_FLOAT, 0);
  // Declare a method for the parameter release
  class_addmethod(Comp_tilde_class,
    (t_method)Comp_tilde_release, gensym("release"), A_FLOAT, 0);
  // Declare a method for the parameter threshold
  class_addmethod(Comp_tilde_class,
    (t_method)Comp_tilde_threshold, gensym("threshold"), A_FLOAT, 0);
  // Declare a method for the parameter ratio
  class_addmethod(Comp_tilde_class,
    (t_method)Comp_tilde_ratio, gensym("ratio"), A_FLOAT, 0);
  // Declare a method for the parameter preamp
  class_addmethod(Comp_tilde_class,
    (t_method)Comp_tilde_preamp, gensym("preamp"), A_FLOAT, 0);
  // Declare a method for the parameter volume
  class_addmethod(Comp_tilde_class,
    (t_method)Comp_tilde_volume, gensym("volume"), A_FLOAT, 0);
  
  CLASS_MAINSIGNALIN(Comp_tilde_class, t_Comp_tilde, dummy_f);
}
