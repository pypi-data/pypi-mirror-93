# vhlsrs

It means Vivado HLS run synthesis.

This package contains a script that runs vivado synthesis in a (somewhat)
reproducible way.

It also allow to search for the minimum pipeline depth design for a given clock
period constrain.

## Usage

### Experience description

The experience to run should be described in a .ini.

A complete experiment description looks like : 
```
[EXP_NAME]
comp_path=path/to/component/file.cpp
top_level_comp= Name of top level function
period= clock period in ns (float)
part= part code name (default is xc7k160tfbg484)
standard= c++ standard to use. (default is c++11)
includes=comma separated list of directories containing includes to use during the synthesis. optionnal.
defines=Key=comma separated list of key=value preprocessor macro that will be defined during synthesis
keep_env=True/False Should the synthesis environment be kept after the synthesis is performed. Default is False.
ip_lib= Name of the ip library to use when exporting the ip (optionnal)
ip_version= Version to use when exporting the ip (optionnal)
ip_descr= description that will be exported along the vivado ip (optionnal)
ip_vendor= vendor name for the exported vivado ip (optionnal)
latency= ltency constraint for the initial design (optionnal)
hdl= verilog|VHDL
no_pipeline=True|False if true the design will not be pipelined (default false)
no_inline=True|False if true the function call will not be inlined (default false)
ctrl_hs=True|False Block protocol will be ap_ctrl_hs if true, ap_ctrl_none else. Default false.
exp_type=hls|syn|impl until which phase is the experiment to be performed
```

### Running a one shot synthesis 

`python -m vhlsrs impl [expdescr.ini]`

will implement the experiments described in expdescr.ini either with a latency constraint if given or with the minimal latency estimated by the tool.


### Minimizing the latency

As vivado HLS is sometimes not very good at timing estimation, it can lead to overpessimistic latency.

the 
`python -m vhlsrs minimize [expdescr.ini]`

will attempt to find the lowest pipeline depth that still respect the clock constraints by dichotomy.
If a latency constraint is provided, it will start the exploration with a designed with this constraint. Otherwise, it will start the exploration with the latency estimated by the tool.

