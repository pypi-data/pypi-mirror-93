# See LICENSE.incore for details
"""Console script for riscof."""

import logging
import importlib
from datetime import datetime
import os
import sys
import pytz
import shutil
import configparser
import distutils.dir_util

from jinja2 import Template

#from riscof.log import *
from riscof.__init__ import __version__
import riscv_config.checker as riscv_config
import riscof.framework.main as framework
import riscof.framework.test as test_routines
import riscof.dbgen as dbgen
import riscof.utils as utils
import riscof.constants as constants
from riscv_config.errors import ValidationError
import riscv_isac.coverage as isac


def execute():
    '''
        Entry point for riscof. This function sets up the models and
        calls the :py:mod:`riscv_config` and :py:mod:`framework` modules with
        appropriate arguments.
    '''
    # Set up the parser
    parser = utils.riscof_cmdline_args()
    args = parser.parse_args()
    if len(sys.argv)<2:
        parser.print_help()
        raise SystemExit

    # Set up the logger
    utils.setup_logging(args.verbose)
    logger = logging.getLogger()
    logger.handlers = []
    ch = logging.StreamHandler()
    ch.setFormatter(utils.ColoredFormatter())
    logger.addHandler(ch)


    if (args.version):
        print('RISCOF: RISC-V Compliance Framework')
        print('Version: '+ __version__)
        return 0
    elif (args.command=='setup'):
        logger.info("Setting up sample plugin requirements [Old files will \
be overwritten]")
        try:
            cwd = os.getcwd()
            logger.info("Creating sample Plugin directory for [DUT]: " +\
                    args.dutname + ' [Ref]: '+args.refname)
            dutname = args.dutname
            src = os.path.join(constants.root, "Templates/setup/model/")
            dest = os.path.join(cwd, dutname)
            distutils.dir_util.copy_tree(src, dest)
            os.rename(cwd+'/'+args.dutname+'/model_isa.yaml',
                    cwd+'/'+args.dutname+'/'+args.dutname+'_isa.yaml')
            os.rename(cwd+'/'+args.dutname+'/model_platform.yaml',
                    cwd+'/'+args.dutname+'/'+args.dutname+'_platform.yaml')
            os.rename(cwd+'/'+args.dutname+'/riscof_model.py',
                    cwd+'/'+args.dutname+'/riscof_'+args.dutname+'.py')
            logger.info("Creating Sample Config File")
            configfile = open('config.ini','w')
            configfile.write(constants.config_temp.format(args.refname, \
                    cwd+'/'+args.refname, args.dutname,cwd+'/'+args.dutname))
            logger.info('**NOTE**: Please update the paths of the reference \
and DUT plugins in the config.ini file')
            configfile.close()
            return 0
        except FileExistsError as err:
            logger.error(err)
            return 1
    else:
        work_dir = constants.work_dir
        #Creating work directory
        if not os.path.exists(work_dir):
            logger.debug('Creating new work directory: ' + work_dir)
            os.mkdir(work_dir)
        else:
            logger.debug('Removing old work directory: ' + work_dir)
            shutil.rmtree(work_dir)
            logger.debug('Creating new work directory: ' + work_dir)
            os.mkdir(work_dir)

    if args.command=='gendb':
        if args.suite is None:
            dbgen.generate_standard()
            logger.info('Database File Generated: '+constants.framework_db)

    if (args.command=='run' or args.command=='testlist' or \
            args.command=='validateyaml' or args.command == 'coverage'):
        config = configparser.ConfigParser()
        logger.info("Reading configuration from: "+args.config)
        try:
            config.read(args.config)
        except FileNotFoundError as err:
            logger.error(err)
            return 1
        riscof_config = config['RISCOF']
        logger.info("Preparing Models")

        config_dir = os.path.dirname(os.path.abspath(args.config))

        # Gathering Models
        dut_model = riscof_config['DUTPlugin']
        dut_model_path = utils.absolute_path(config_dir, riscof_config['DUTPluginPath'])

        base_model = riscof_config['ReferencePlugin']
        base_model_path = utils.absolute_path(config_dir, riscof_config['ReferencePluginPath'])

        logger.debug("Importing " + dut_model + " plugin from: "+str(dut_model_path))
        sys.path.append(dut_model_path)
        try:
            dut_plugin = importlib.import_module("riscof_" + dut_model)
        except ImportError as msg:
            logger.error("Error while importing "+dut_model+".\n"+str(msg))
            raise SystemExit
        dut_class = getattr(dut_plugin, dut_model)
        if dut_model in config:
            dut = dut_class(name="DUT", config=config[dut_model], config_dir=config_dir)
        else:
            dut = dut_class(name="DUT")

        logger.debug("Importing " + base_model + " plugin from: "+str(base_model_path))
        sys.path.append(base_model_path)
        try:
            base_plugin = importlib.import_module("riscof_" + base_model)
        except ImportError as msg:
            logger.error("Error while importing "+base_model+".\n"+str(msg))
            raise SystemExit
        base_class = getattr(base_plugin, base_model)
        if base_model in config:
            base = base_class(name="Reference", config=config[base_model], config_dir=config_dir)
        else:
            base = base_class(name="Reference")

        #Run riscv_config on inputs
        isa_file = dut.isa_spec
        platform_file = dut.platform_spec


        try:
            isa_file = riscv_config.check_isa_specs( isa_file, work_dir, True)
            platform_file = riscv_config.check_platform_specs( platform_file, work_dir, True)
        except ValidationError as msg:
            logger.error(msg)
            return 1

        isa_specs = utils.load_yaml(isa_file)['hart0']
        platform_specs = utils.load_yaml(platform_file)

    if args.command=='gendb' or args.command=='run' or \
            args.command=='testlist' or args.command == 'coverage' :
        if args.suite is not None:
            logger.info("Generating database for custom suite.")
            work_dir = constants.work_dir
            constants.suite = args.suite
            constants.framework_db = os.path.join(work_dir,"database.yaml")
            logger.debug('Suite used: '+constants.suite)
            dbgen.generate()
            logger.info('Database File Generated: '+constants.framework_db)
            constants.env = os.path.join(args.suite,"env/")
            logger.info('Env path set to'+constants.env)

    if args.command == 'testlist':
        test_routines.generate_test_pool(isa_specs, platform_specs)

    if args.command == 'coverage':
        logger.info('Will collect Coverage using RISCV-ISAC')
        if args.cgf is None:
            cgf_file = constants.cgf_file
        else:
            cgf_file = args.cgf
        logger.info('CGF file being used : ' + str(cgf_file))

        with open(isa_file, "r") as isafile:
            ispecs = isafile.read()

        with open(platform_file, "r") as platfile:
            pspecs = platfile.read()
        report, for_html, test_stats, coverpoints = framework.run_coverage(base, isa_file, platform_file,
                cgf_file)
        report_file = open(constants.work_dir+'/suite_coverage.rpt','w')
        report_file.write(report)
        report_file.close()

        report_objects = {}
        report_objects['date'] = (datetime.now(
            pytz.timezone('GMT'))).strftime("%Y-%m-%d %H:%M GMT")
        report_objects['version'] = __version__
        report_objects['reference'] = (base.__model__).replace("_", " ")

        report_objects['isa'] = isa_specs['ISA']
        report_objects['usv'] = isa_specs['User_Spec_Version']
        report_objects['psv'] = isa_specs['Privilege_Spec_Version']
        report_objects['isa_yaml'] = isa_file
        report_objects['platform_yaml'] = platform_file
        report_objects['isa_specs'] = ispecs
        report_objects['platform_specs'] = pspecs
        report_objects['results'] = for_html
        report_objects['results1'] = test_stats
        report_objects['coverpoints'] = coverpoints
        #report_objects['results'] = framework.run(dut, base, isa_file,
        #                                          platform_file)
        with open(constants.coverage_template, "r") as report_template:
            template = Template(report_template.read())

        output = template.render(report_objects)

        reportfile = os.path.join(constants.work_dir, "coverage.html")
        with open(reportfile, "w") as report:
            report.write(output)

        shutil.copyfile(constants.css,
                        os.path.join(constants.work_dir, "style.css"))

        logger.info("Test report generated at "+reportfile+".")
        if not args.no_browser:
            try:
                import webbrowser
                logger.info("Openning test report in web-browser")
                webbrowser.open(reportfile)
            except:
                return 1
        return 0

    if args.command=='run':
        with open(isa_file, "r") as isafile:
            ispecs = isafile.read()

        with open(platform_file, "r") as platfile:
            pspecs = platfile.read()

        report_objects = {}
        report_objects['date'] = (datetime.now(
            pytz.timezone('GMT'))).strftime("%Y-%m-%d %H:%M GMT")
        report_objects['version'] = __version__
        report_objects['dut'] = (dut.__model__).replace("_", " ")
        report_objects['reference'] = (base.__model__).replace("_", " ")

        report_objects['isa'] = isa_specs['ISA']
        report_objects['usv'] = isa_specs['User_Spec_Version']
        report_objects['psv'] = isa_specs['Privilege_Spec_Version']
        report_objects['isa_yaml'] = isa_file
        report_objects['platform_yaml'] = platform_file
        report_objects['isa_specs'] = ispecs
        report_objects['platform_specs'] = pspecs

        report_objects['results'] = framework.run(dut, base, isa_file,
                                                  platform_file)

        report_objects['num_passed'] = 0
        report_objects['num_failed'] = 0

        for entry in report_objects['results']:
            if entry['res'] == "Passed":
                report_objects['num_passed'] += 1
            else:
                report_objects['num_failed'] += 1

        with open(constants.html_template, "r") as report_template:
            template = Template(report_template.read())

        output = template.render(report_objects)

        reportfile = os.path.join(constants.work_dir, "report.html")
        with open(reportfile, "w") as report:
            report.write(output)

        shutil.copyfile(constants.css,
                        os.path.join(constants.work_dir, "style.css"))

        logger.info("Test report generated at "+reportfile+".")
        if not args.no_browser:
            try:
                import webbrowser
                logger.info("Openning test report in web-browser")
                webbrowser.open(reportfile)
            except:
                return 1


if __name__ == "__main__":
    exit(execute())
