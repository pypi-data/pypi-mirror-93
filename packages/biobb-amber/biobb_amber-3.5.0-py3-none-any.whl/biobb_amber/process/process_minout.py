#!/usr/bin/env python3

"""Module containing the ProcessMinOut class and the command line interface."""
import argparse
import shutil
from pathlib import Path, PurePath
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_amber.process.common import *

class ProcessMinOut():
    """
    | biobb_amber.process.process_minout ProcessMinOut
    | Wrapper of the `AmberTools (AMBER MD Package) process_minout tool <https://ambermd.org/AmberTools.php>`_ module.
    | Parses the AMBER (sander) minimization output file (log) and dumps statistics that can then be plotted. Using the process_minout.pl tool from the AmberTools MD package.

    Args:
        input_log_path (str): AMBER (sander) Minimization output (log) file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/process/sander.min.log>`_. Accepted formats: log (edam:format_2330), out (edam:format_2330), txt (edam:format_2330), o (edam:format_2330).
        output_dat_path (str): Dat output file containing data from the specified terms along the minimization process. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/process/sander.min.energy.dat>`_. Accepted formats: dat (edam:format_1637), txt (edam:format_2330), csv (edam:format_3752).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **terms** (*list*) - (["ENERGY"]) Statistics descriptors. Values: ANGLE, BOND, DIHEDRAL, EEL, EEL14, ENERGY, GMAX, HBOND, NAME, NSTEP, NUMBER, RESTRAINT, RMS, VDW14, VDWAALS.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_amber.process.process_minout import process_minout
            prop = {
                'terms' : ['ENERGY','RMS']
            }
            process_minout(input_log_path='/path/to/ambermin.log',
                          output_dat_path='/path/to/newFeature.dat',
                          properties=prop)

    Info:
        * wrapped_software:
            * name: AmberTools process_minout
            * version: >20.9
            * license: LGPL 2.1
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_log_path: str, output_dat_path: str, properties, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.io_dict = {
            'in': { 'input_log_path': input_log_path },
            'out': { 'output_dat_path': output_dat_path }
        }

        # Properties specific for BB
        self.properties = properties
        self.terms = properties.get('terms', ["ENERGY"])

        # Properties common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')
        self.remove_tmp = properties.get('remove_tmp', True)
        self.restart = properties.get('restart', False)

    def check_data_params(self, out_log):
        """ Checks input/output paths correctness """

        # Check input(s)
        self.io_dict["in"]["input_log_path"] = check_input_path(self.io_dict["in"]["input_log_path"], "input_log_path", False, out_log, self.__class__.__name__)

        # Check output(s)
        self.io_dict["out"]["output_dat_path"] = check_output_path(self.io_dict["out"]["output_dat_path"],"output_dat_path", False, out_log, self.__class__.__name__)

    @launchlogger
    def launch(self):
        """Launches the execution of the ProcessMinOut module."""

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # check input/output paths and parameters
        self.check_data_params(out_log)

        # Check the properties
        fu.check_properties(self, self.properties)

        # Restart
        if self.restart:
            # 4. Include here all output file paths
            output_file_list = [self.io_dict['out']['output_dat_path']]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step, out_log, self.global_log)
                return 0

        # Command line
        cmd = ['process_minout.perl ',
               self.io_dict['in']['input_log_path']
               ]
        fu.log('Creating command line with instructions and required arguments', out_log, self.global_log)

        # Launch execution
        returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()

        if len(self.terms) == 1:
           shutil.copy('summary.'+self.terms[0], self.io_dict['out']['output_dat_path'])
        else:
            ene_dict = {}
            for term in self.terms:
                with open("summary."+term) as fp:
                   for line in fp:
                       x = line.split()
                       ene_dict.setdefault(int(x[0]), {})[term] = x[1]

            with open(self.io_dict['out']['output_dat_path'],'w') as fp_out:
                fp_out.write("# TIME ")
                for term in self.terms:
                    fp_out.write(term + " ")
                fp_out.write("\n")
                for key in sorted(ene_dict.keys()):
                    fp_out.write(str(key) + " ")
                    for term in self.terms:
                        fp_out.write(ene_dict[key][term] + " ")
                    fp_out.write("\n")

        # Remove temporary file(s)
        if self.remove_tmp:
            files_to_rm = list(Path().glob('summary.*'))
            fu.rm_file_list(files_to_rm)
            fu.log('Removed: {}'.format(files_to_rm), out_log)

        return returncode

def process_minout(input_log_path: str, output_dat_path: str,
           properties: dict = None, **kwargs) -> int:
    """Create :class:`ProcessMinOut <process.process_mdout.ProcessMinOut>`process.process_mdout.ProcessMinOut class and
    execute :meth:`launch() <process.process_mdout.ProcessMinOut.launch>` method"""

    return ProcessMinOut( input_log_path=input_log_path,
                        output_dat_path=output_dat_path,
                        properties=properties).launch()

def main():
    parser = argparse.ArgumentParser(description='Parses the AMBER (sander) minimization output file (log) and dumps statistics that can then be plotted. Using the process_minout.pl tool from the AmberTools MD package.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_log_path', required=True, help='AMBER (sander) minimization output (log) file. Accepted formats: log, out, txt, o.')
    required_args.add_argument('--output_dat_path', required=True, help='Dat output file containing data from the specified terms along the minimization process. File type: output. Accepted formats: dat, txt, csv.')

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call
    ProcessMinOut(
             input_log_path=args.input_log_path,
             output_pdb_path=args.output_pdb_path,
             properties=properties).launch()

if __name__ == '__main__':
    main()
