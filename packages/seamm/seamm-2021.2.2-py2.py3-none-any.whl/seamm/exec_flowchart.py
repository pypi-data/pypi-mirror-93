# -*- coding: utf-8 -*-

"""The ExecWorkflow object does what it name implies: it executes, or
runs, a given flowchart.

It provides the environment for running the computational tasks
locally or remotely, using what is commonly called workflow management
system (WMS).  The WMS concept, as used here, means tools that run
given tasks without knowing anything about chemistry. The chemistry
specialization is contained in the Flowchart and the nodes that it
contains."""

import calendar
import logging
import os.path
import string
import sys
import traceback

from molsystem import SystemDB
import reference_handler
import seamm
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __  # noqa: F401

logger = logging.getLogger(__name__)
job = printing.getPrinter()


class ExecFlowchart(object):

    def __init__(self, flowchart=None):
        """Execute a flowchart, providing support for the actual
        execution of codes """
        logger.info('In ExecFlowchart.init()')

        self.flowchart = flowchart

    def run(self, root=None):
        logger.info('In ExecFlowchart.run()')
        if not self.flowchart:
            raise RuntimeError('There is no flowchart to run!')

        # Get the command line options
        parser = seamm.getParser()
        options = parser.get_options()

        # Set the options in each step
        for node in self.flowchart:
            step_type = node.step_type
            logger.info(f'    setting options for {step_type}')
            if step_type in options:
                node._options = options[step_type]
            if 'SEAMM' in options:
                node._global_options = options['SEAMM']

        # Create the global context
        logger.info('Creating global variables space')
        seamm.flowchart_variables = seamm.Variables()

        # And add the printer
        seamm.flowchart_variables.set_variable('printer', job)

        # Setup the citations
        filename = os.path.join(self.flowchart.root_directory, 'references.db')
        references = None
        try:
            references = reference_handler.Reference_Handler(filename)
        except Exception as e:
            job.job('Error with references:')
            job.job(e)

        if references is not None:
            try:
                template = string.Template(
                    """\
                    @misc{seamm,
                          address = {$address},
                          author = {$author},
                          month = {$month},
                          organization = {$organization},
                          title = {$title},
                          url = {$url},
                          version = {$version},
                          year = $year
                    }"""
                )

                version = seamm.__version__
                year, month = version.split('.')[0:2]
                month = calendar.month_abbr[int(month)].lower()
                citation = template.substitute(
                    address='Virginia Tech, Blacksburg, VA, USA',
                    author='Jessica Nash, Eliseo Marin-Rimoldi, Paul Saxe',
                    month=month,
                    organization=(
                        'The Molecular Sciences Software Institute (MolSSI)'
                    ),
                    title=(
                        'SEAMM: Simulation Environment for Atomistic and '
                        'Molecular Modeling'
                    ),
                    url='https://github.com/molssi-seamm/seamm',
                    version=version,
                    year=year
                )

                references.cite(
                    raw=citation,
                    alias='SEAMM',
                    module='seamm',
                    level=1,
                    note='The principle citation for SEAMM.'
                )
            except Exception as e:
                job.job(f'Exception in citation {type(e)}: {e}')
                job.job(traceback.format_exc())

        # Create the system database, default system and configuration
        db = SystemDB(filename='file:seamm.db')
        system = db.system = db.create_system(name='default')
        system.configuration = system.create_configuration(name='default')

        # Put the system database in the global context for access.
        seamm.flowchart_variables.set_variable('_system_db', db)

        self.flowchart.root_directory = root

        # Correctly number the nodes
        self.flowchart.set_ids()

        # Write out an initial summary of the flowchart before doing anything
        # Reset the visited flag for traversal
        self.flowchart.reset_visited()

        # Get the start node
        next_node = self.flowchart.get_node('1')

        # describe ourselves
        job.job(
            (
                '\nDescription of the flowchart'
                '\n----------------------------'
            )
        )

        while next_node:
            # and print the description
            try:
                next_node = next_node.describe()
            except Exception:
                message = (
                    'Error describing the flowchart\n\n' +
                    traceback.format_exc()
                )
                print(message)
                logger.critical(message)
                raise
            except:  # noqa: E722
                message = (
                    'Unexpected error describing the flowchart\n\n' +
                    traceback.format_exc()
                )
                print(message)
                logger.critical(message)
                raise

        job.job('')

        # And actually run it!
        job.job(('Running the flowchart\n' '---------------------'))

        next_node = self.flowchart.get_node('1')
        while next_node is not None:
            try:
                next_node = next_node.run()
            except DeprecationWarning as e:
                print('\nDeprecation warning: ' + str(e))
                traceback.print_exc(file=sys.stderr)
                traceback.print_exc(file=sys.stdout)
            except Exception:
                message = (
                    'Error running the flowchart\n\n' + traceback.format_exc()
                )
                print(message)
                logger.critical(message)
                break
            except:  # noqa: E722
                message = (
                    'Unexpected error running the flowchart\n\n' +
                    traceback.format_exc()
                )
                print(message)
                logger.critical(message)
                raise

        # Write the final structure
        db = seamm.flowchart_variables.get_variable('_system_db')
        configuration = db.system.configuration
        if configuration.n_atoms() > 0:
            # MMCIF file has bonds
            filename = os.path.join(
                self.flowchart.root_directory, 'final_structure.mmcif'
            )
            text = None
            try:
                text = configuration.to_mmcif_text()
            except Exception:
                message = (
                    'Error creating the final mmcif file\n\n' +
                    traceback.format_exc()
                )
                print(message)
                logger.critical(message)

            if text is not None:
                with open(filename, 'w') as fd:
                    print(text, file=fd)
                job.job(
                    "\nWrote the final structure to 'final_structure.mmcif' "
                    'for viewing.'
                )
            # CIF file has cell
            if configuration.periodicity == 3:
                filename = os.path.join(
                    self.flowchart.root_directory, 'final_structure.cif'
                )
                with open(filename, 'w') as fd:
                    print(configuration.to_cif_text(), file=fd)
                job.job(
                    "\nWrote the final structure to 'final_structure.cif' for "
                    'viewing.'
                )

        # And print out the references
        filename = os.path.join(self.flowchart.root_directory, 'references.db')
        try:
            references = reference_handler.Reference_Handler(filename)
        except Exception as e:
            job.job('Error with references:')
            job.job(e)

        if references.total_citations() > 0:
            tmp = {}
            citations = references.dump(fmt='text')
            for citation, text, count, level in citations:
                if level not in tmp:
                    tmp[level] = {}
                tmp[level][citation] = (text, count)

            n = 0
            for level in sorted(tmp.keys()):
                ref_dict = tmp[level]
                if level == 1:
                    job.job('\nPrimary references:\n')
                    n = 0
                elif level == 2:
                    job.job('\nSecondary references:\n')
                    n = 0
                else:
                    job.job('\nLess important references:\n')
                    n = 0

                lines = []
                for citation in sorted(ref_dict.keys()):
                    n += 1
                    text, count = ref_dict[citation]
                    if count == 1:
                        lines.append('({}) {:s}'.format(n, text))
                    else:
                        lines.append(
                            '({}) {:s} (used {:d} times)'.format(
                                n, text, count
                            )
                        )
                job.job(
                    __(
                        '\n\n'.join(lines),
                        indent=4 * ' ',
                        indent_initial=False
                    )
                )
