#!/usr/bin/env python
"""Command Line Interface similar to CopasiSE

This module acts as command line interface to the Python COPASI API similar, to
how the compiled CopasiSE works. The same command line switches are supported.

Additionally, the module has a convenience function `copasi_se` that takes the same
options and can be executed interactively:

    Execute a copasi file
    >>> copasi_se('brusselator.cps')

Commandline Options:

    -s, --save (string) This option is used to specify the name file where COPASI
                        should store a model. This is useful if you intend to convert
                        some SBML files to COPASI files in a batch job. This also makes
                        sense only for the commandline version and will be ignored by
                        the GUI version.

    -i, --importSBML (string) This options lets you specify an SBML file that COPASI shall import.

    -e, --exportSBML (string) With this option you can specify a name for the SBML file COPASI
                              should export. This is useful if you want to export some COPASI
                              files to SBML in a batch job. This only makes sense for the
                              commandline version and it will be ignored by the GUI version.

    --SBMLSchema (L1V2, L2V1, L2V2, L2V3, L2V4, L3V1) This switch works in combination with the
                              --exportSBML switch and determines which SBML level and version is
                              going to be used for SBML export. Currently the following schemas are
                              supported SBML Level 1 Version 2 (L1V2), SBML Level 2 Version 1 (L2V1),
                              SBML Level 2 Version 2 (L2V2), SBML Level 2 Version 3 (L2V3),
                              SBML Level 2 Version 4 (L2V4), and SBML Level 3 Version 1 (L3V1).

                              If no schema is given, the export creates SBML Level 2 Version 4 files.

    --importSEDML (string)    This options lets you specify an SEDML file that COPASI shall import.

    --exportSEDML (string)    With this option you can specify a name for the SEDML file COPASI should export.

    --importCA (string)       This options lets you specify a COMBINE archive file that COPASI shall import.

    --exportCA (string)  With this option you can specify a name for the COMBINE archive file COPASI should export.

    --exportBerkeleyMadonna (string) With this option you can specify a name for the Berkeley Madonna file
                              COPASI should export. This is useful if you want to export some COPASI files to
                              Berkeley Madonna file format in a batch job. This only makes sense for the
                              commandline version and it will be ignored by the GUI version.

    --exportC (string)        With this option you can specify a name for the C source file COPASI should export.
                              This is useful if you want to export some COPASI files to C source code in a batch job.
                              This only makes sense for the commandline version and it will be ignored by the
                              GUI version.

    --exportXPPAUT (string)   With this option you can specify a name for the XPPAUT file COPASI should export. This
                              is useful if you want to export some COPASI files to XPPAUTs ODE file format in a batch
                              job. This only makes sense for the commandline version and it will be ignored by the
                              GUI version.

    -c, --copasidir (string)  This specifies the directory where COPASI has been installed. It is needed to find e.g.
                              help files. On Windows and Mac OS X this is set automatically. On Linux it has to be
                              specified if you want to use certain features. The GUI version of COPASI will issue a
                              warning on startup if this has not been set. The commandline version does not need
                              this directory to be specified and therefore ignores this option.

    --exportIni (string)      export the parameterization of the model as INI file for use with the
                              --reparameterize option.

    -r, --reparameterize (string) Before any task is run, the model is reparameterized with the values specified in
                              the provided INI file.

    --configdir (string)      This can be used to specify the directory where COPASI stores its configuration files.
                              Normally this is called .copasi and is located in the users home directory. But if you
                              want COPASI to use a different one, you can specify it with this switch.

    --configfile (string)     This can be used to specify the filename where COPASI loads and stores its configuration.
                              Normally this is called COPASI and is located in the directory specified with --configdir.
                              But if you want COPASI to use a different filename, you can specify it with this switch.

    --home (string)           This can be used to tell COPASI where your home directory is located. Normally you don't
                              have to use this.

    -t, --tmp (string)        This option can be used to specify a temporary directory where COPASI will auto-save some
                              data periodically. Normally COPASI uses the systems temporary directory (e.g. /tmp/ under
                              Linux).

    --report-file (string)    Override report file name to be used except for the one defined in the scheduled task.

    --scheduled-task (string) Override the task marked as executable.

    --convert-to-irreversible Converts reversible reactions to irreversible ones before running Task.

    --maxTime (seconds)       The maximal time CopasiSE may run in seconds.

    --license                 With this commandline option, COPASI will print its license and exit.

    --nologo                  This option suppresses the output of the "Logo" when CopasiSE is run. The "Logo" usually
                              consist of the version of COPASI and some license statement.

    --validate                This commandline option can be used to validate the given file. The file can either be
                              a COPASI file or an SBML file.

    --verbose                 This commandline option tells COPASI to print more output on what it is doing to std::out.

"""

import COPASI
import getopt
import sys
import os
import logging
import signal

_LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=_LOGLEVEL)


def _print_logo():
    """This function prints the current copasi version."""
    version = COPASI.CVersion.VERSION
    assert (isinstance(version, COPASI.CVersion))

    print("""COPASI {0}.{1} (Build {2})
The use of this software indicates the acceptance of the attached license.
To view the license please use the option: --license""".format(
        version.getVersionMajor(),
        version.getVersionMinor(),
        version.getVersionDevel()
    ))


def _print_usage():
    """This function prints the available parameter switches"""
    print("""Usage: pyCopasiSE [options] [file]
  
  --SBMLSchema schema           The Schema of the SBML file to export.
  --configdir dir               The configuration directory for copasi. The
                                default is .copasi in the home directory.
  --configfile file             The configuration file for copasi. The
                                default is copasi in the ConfigDir.
  --convert-to-irreversible     Converts reversible reactions to irreversible
                                ones before running Task.
  --exportBerkeleyMadonna file  The Berkeley Madonna file to export.
  --exportC file                The C code file to export.
  --exportCA file               The COMBINE archive file to export.
  --exportIni file              export the parameterization of the model as
                                INI file for use with the --reparameterize
                                option.
  --exportSEDML file            The SEDML file to export.
  --exportXPPAUT file           The XPPAUT file to export.
  --home dir                    Your home directory.
  --importCA file               A COMBINE archive file to import.
  --importSEDML file            A SEDML file to import.
  --license                     Display the license.
  --maxTime seconds             The maximal time CopasiSE may run in
                                seconds.
  --nologo                      Supresses the startup message.
  --report-file file            Override report file name to be used except
                                for the one defined in the scheduled task.
  --scheduled-task taskName     Override the task marked as executable.
  --validate                    Only validate the given input file (COPASI,
                                Gepasi, or SBML) without performing any
                                calculations.
  --verbose                     Enable output of messages during runtime to
                                std::error.
  -c, --copasidir dir           The COPASI installation directory.
  -e, --exportSBML file         The SBML file to export.
  -i, --importSBML file         A SBML file to import.
  -r, --reparameterize file     Before any task is run, the model is
                                reparameterized with the values specified
                                in the provided INI file.
  -s, --save file               The file the model is saved to after work.
  -t, --tmp dir                 The temp directory used for autosave.""")


def _convert_opts(opts):
    """Convert list of tuples to dictionary"""
    result = {}
    for k, v in opts:
        if k.startswith('--'):
            k = k[2:]
        if k.startswith('-'):
            k = k[1:]

        k = k.replace('-', '_')
        result[k] = v
    return result


def _parse_args():
    """Parses the arguments, if unsupported options are used, all options are ignored"""
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "t:r:s:c:e:i:s:",
                                   [
                                       "save=", "importSBML=", "exportSBML=", "SBMLSchema=", "importSEDML=",
                                       "exportSEDML=",
                                       "importCA=", "exportCA=", "exportBerkeleyMadonna=", "exportC=", "exportXPPAUT=",
                                       "copasidir=", "exportIni=", "reparameterize=", "configdir=", "configfile=",
                                       "home=", "tmp=", "report-file=", "scheduled-task=", "convert-to-irreversible",
                                       "maxTime=", "license", "nologo", "validate", "verbose"
                                   ])
    except getopt.GetoptError:
        opts = []
        args = []

    opts = _convert_opts(opts)
    return opts, args


_OPTIONS, _FILES = _parse_args()
_dm = COPASI.CRootContainer.addDatamodel()
assert (isinstance(_dm, COPASI.CDataModel))


class _PythonProgress(COPASI.CProcessReport):
    """Helper class, to register ctrl-c handler for stopping long running operations"""
    def __init__(self, max_time=0):
        super(_PythonProgress, self).__init__(max_time)
        if max_time:
            logging.debug('creating process handler with max time: {0}'.format(max_time))
        self.shouldProceed = True

    def progressItem(self, handle):
        return super(_PythonProgress, self).progressItem(handle) and self.shouldProceed

    def proceed(self):
        return super(_PythonProgress, self).proceed() and self.shouldProceed

    def ask_to_stop(self):
        logging.debug('task interrupted stopping soon ...')
        self.shouldProceed = False


_progress = _PythonProgress(int(_OPTIONS.get('maxTime', '0')))


# now setup a handler to ask to stop the processing
def _sigint_handler(signum, frame):
    global _progress
    _progress.ask_to_stop()


signal.signal(signal.SIGINT, _sigint_handler)


def _run_command(function, heading, *args):
    """Convenience function, running the given function

    Args:
        function: the function to run
        heading: heading to print in case an error (or exception occurs)
        *args: function arguments

    Returns: boolean indicating success (True) or failure

    """
    logging.debug('starting: ' + heading + ' with: ' + repr(args))
    try:
        if not function(*args):
            logging.error(heading)
            logging.error(COPASI.CCopasiMessage.getAllMessageText())
            return False
    except COPASI.CCopasiException:
        logging.error(heading)
        logging.error(COPASI.CCopasiMessage.getAllMessageText())
        return False

    return True


def _import_file():
    """Imports a file into copasi, file can be either sbml, sedml or combine archive"""
    global _dm

    if 'i' in _OPTIONS and not _run_command(_dm.importSBML,
                                            "SBML Import File: " + _OPTIONS['i'],
                                            _OPTIONS['i']):
        return False

    if 'importSBML' in _OPTIONS and not _run_command(_dm.importSBML,
                                                     "SBML Import File: " + _OPTIONS['importSBML'],
                                                     _OPTIONS['importSBML']):
        return False

    if 'importSEDML' in _OPTIONS and not _run_command(_dm.importSEDML,
                                                      "SED-ML Import File: " + _OPTIONS['importSEDML'],
                                                      _OPTIONS['importSEDML']):
        return False

    if 'importCA' in _OPTIONS and not _run_command(_dm.openCombineArchive,
                                                   "CombineArchive Import File: " + _OPTIONS['importCA'],
                                                   _OPTIONS['importCA']):
        return False

    return True


def _validate():
    """Checks whether scheduled tasks can be initialized and run"""
    logging.debug('running validation')
    result = 0
    for task in _dm.getTaskList():
        if task.isScheduled():
            try:
                success = task.initializeRaw(COPASI.CCopasiTask.OUTPUT_SE)
                if COPASI.CCopasiMessage.checkForMessage(5000 + 3300 + 5) and \
                   (not task.isUpdateModel() or 's' not in _OPTIONS or 'save' not in _OPTIONS):
                    success = False
            except COPASI.CCopasiException:
                success = False

            if not success:
                logging.error('File: ' + _dm.getFileName())
                logging.error('Task: ' + task.getObjectName())
                logging.error(COPASI.CCopasiMessage.getAllMessageText())
                result = 1

            _dm.finish()

        return result


def _get_sbml_level_version():
    """

    Returns: SBML Level and Version selected

    """
    schema = _OPTIONS.get('SBMLSchema', 'L3V1')
    lv = {
        'L1V2': (1, 2),
        'L2V1': (2, 1),
        'L2V2': (2, 2),
        'L2V3': (2, 3),
        'L2V4': (2, 4),
        'L2V5': (2, 5),
        'L3V1': (3, 1),
        'L3V2': (3, 2),
    }
    return lv.get(schema, (3, 1))


def _export_file():
    """Exports the current model to SBML, SED-ML, Combine Archive, Berkeley Madonna, C or XPP"""
    global _dm
    level, version = _get_sbml_level_version()
    if 'e' in _OPTIONS and not _run_command(_dm.exportSBML,
                                            "SBML Export File: " + _OPTIONS['e'],
                                            _OPTIONS['e'], True, level, version):
        return False

    if 'exportSBML' in _OPTIONS and not _run_command(_dm.exportSBML,
                                                     "SBML Export File: " + _OPTIONS['exportSBML'],
                                                     _OPTIONS['exportSEDML'], True, level, version):
        return False

    if 'exportSEDML' in _OPTIONS and not _run_command(_dm.exportSEDML,
                                                      "SED-ML Export File: " + _OPTIONS['exportSEDML'],
                                                      _OPTIONS['exportSEDML'], True, 1, 3):
        return False

    if 'exportCA' in _OPTIONS and not _run_command(_dm.exportCombineArchive,
                                                   "Combine Archive Export File: " + _OPTIONS['exportCA'],
                                                   _OPTIONS['exportCA'], True, True, True, True, True):
        return False

    if 'exportBerkeleyMadonna' in _OPTIONS and not _run_command(_dm.exportMathModel,
                                                                "Berkeley Madonna File: " +
                                                                _OPTIONS['exportBerkeleyMadonna'],
                                                                _OPTIONS['exportBerkeleyMadonna'], None,
                                                                "Berkeley Madonna Files (*.mmd)", True):
        return False

    if 'exportC' in _OPTIONS and not _run_command(_dm.exportMathModel,
                                                  "C File: " +
                                                  _OPTIONS['exportC'],
                                                  _OPTIONS['exportC'], None,
                                                  "C Files (*.c)", True):
        return False

    if 'exportXPPAUT' in _OPTIONS and not _run_command(_dm.exportMathModel,
                                                       "XPPAUT File: " +
                                                       _OPTIONS['exportXPPAUT'],
                                                       _OPTIONS['exportXPPAUT'], None,
                                                       "XPPAUT (*.ode)", True):
        return False

    return True


def _get_scheduled_task():
    """Returns the first scheduled task"""
    for task in _dm.getTaskList():
        if task.isScheduled():
            return task
    return None


def _run_scheduled_task():
    """Runs the first scheduled task"""
    task = _get_scheduled_task()
    if task is None:
        logging.debug('no task scheduled')
        return False

    if 's' in _OPTIONS or 'save' in _OPTIONS:
        task.setUpdateModel(True)

    logging.debug('set callback')
    task.setCallBack(_progress)

    logging.debug('initialize task: ' + task.getObjectName())
    task.initializeRaw(COPASI.CCopasiTask.OUTPUT_UI)

    if COPASI.CCopasiMessage.checkForMessage(5000 + 3300 + 5) and \
            (not task.isUpdateModel() or 's' not in _OPTIONS or 'save' not in _OPTIONS):
        # skip running model that has no report, and is not saved
        logging.debug('task has no report and update model is not specified')
        task.setCallBack(None)
        return False

    logging.debug('processing task')
    if not task.processRaw(True):
        logging.error('File: ' + _dm.getFileName())
        logging.error('Task: ' + task.getObjectName())
        logging.error(COPASI.CCopasiMessage.getAllMessageText())
        task.setCallBack(None)
        return False

    task.setCallBack(None)
    _dm.finish()


def _set_scheduled_task(task_name):
    """Sets the scheduled task to the given one"""
    logging.debug('setting scheduled task to: ' + task_name)
    for task in _dm.getTaskList():
        task.setScheduled(task.getObjectName() == task_name)


def _process_model():
    """Runs the model with selected options"""
    if 'scheduled_task' in _OPTIONS:
        _set_scheduled_task(_OPTIONS['scheduled_task'])

    task = _get_scheduled_task()
    if task and 'report_file' in _OPTIONS:
        logging.debug('change report target to: ' + _OPTIONS['report_file'])
        task.getReport().setTarget(_OPTIONS['report_file'])

    if 'validate' in _OPTIONS:
        return _validate()  # COPASI SE quits after validation

    if 'convert_to_irreversible' in _OPTIONS:
        logging.debug('converting to irreversible')
        _dm.getModel().convert2NonReversible()
        _dm.getModel().compileIfNecessary()

    if 'reparameterize' in _OPTIONS:
        logging.debug('reparameterize from file: ' + _OPTIONS['reparameterize'])
        _dm.reparameterizeFromIniFile(_OPTIONS['reparameterize'])

    _export_file()

    _run_scheduled_task()

    if 's' in _OPTIONS:
        logging.debug('saving to: ' + _OPTIONS['s'])
        _dm.saveModel(_OPTIONS['s'], True)

    if 'save' in _OPTIONS:
        logging.debug('saving to: ' + _OPTIONS['save'])
        _dm.saveModel(_OPTIONS['save'], True)

    return True


def _main():
    if 'nologo' not in _OPTIONS:
        _print_logo()

    if 'license' in _OPTIONS:
        print(COPASI.CRootContainer.getLicenseTxt())
        return 0

    logging.debug('OPTIONS: ' + repr(_OPTIONS))
    logging.debug('FILES: ' + repr(_FILES))

    have_import = 'i' in _OPTIONS or 'importSBML' in _OPTIONS or \
                  'importSEDML' in _OPTIONS or 'importCA' in _OPTIONS

    if not _FILES and not have_import:
        _print_usage()
        return 1

    if have_import:
        if not _import_file():
            return 1

        return _process_model()

    for file in _FILES:
        if not _dm.loadModel(file):
            logging.error("File: " + file)
            logging.error(COPASI.CCopasiMessage.getAllMessageText())
            return 1

        if not _process_model():
            break


def copasi_se(*args, **kwargs):
    """Executes files as COPASI SE would.

    Examples:

        To execude the scheduled task of a COPASI file, you would just run:
        >>> copasi_se('brusselator.cps')

        To change the active task to 'Time-Course' and the report file to be created to
        'data.txt' you'd use:
        >>> copasi_se('brusselator.cps', scheduled_task='Time-Course', report_file='data.txt')

        To Export a COPASI file to SBML:
        >>> copasi_se('brusselator.cps', exportSBML='brusselator.xml')

        To Import an SBML file and save it as COPASI file:
        >>> copasi_se(importSBML='brusselator.xml', save='brusselator.cps')

    Args:
        *args: copasi files to execute
        **kwargs: all the options listed the beginning of the module (without leading dashes, and dashes
                  replaced by underscores), so for '--report-file' will become 'report_file'

    Returns: status code (0, all ok otherwise an error occurred)

    """
    global _OPTIONS, _FILES
    _OPTIONS = kwargs
    _FILES = args

    if 'maxTime' in _OPTIONS:
        global _progress
        _progress = _PythonProgress(int(_OPTIONS.get('maxTime', '0')))

    return _main()


if __name__ == "__main__":
    sys.exit(_main())
