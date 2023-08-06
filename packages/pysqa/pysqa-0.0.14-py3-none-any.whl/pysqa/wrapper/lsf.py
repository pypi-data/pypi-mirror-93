# coding: utf-8
# Copyright (c) Max-Planck-Institut für Eisenforschung GmbH - Computational Materials Design (CM) Department
# Distributed under the terms of "New BSD License", see the LICENSE file.

__author__ = "Jan Janssen"
__copyright__ = (
    "Copyright 2019, Max-Planck-Institut für Eisenforschung GmbH - "
    "Computational Materials Design (CM) Department"
)
__version__ = "1.0"
__maintainer__ = "Jan Janssen"
__email__ = "janssen@mpie.de"
__status__ = "development"
__date__ = "Feb 9, 2019"


class LsfCommands(object):
    @property
    def submit_job_command(self):
        return ["bsub", "-terse"]

    @property
    def delete_job_command(self):
        return ["bkill"]

    @property
    def enable_reservation_command(self):
        raise NotImplementedError()

    @property
    def get_queue_status_command(self):
        return ["qstat", "-x"]

    @staticmethod
    def get_job_id_from_output(queue_submit_output):
        raise NotImplementedError()

    @staticmethod
    def convert_queue_status(queue_status_output):
        raise NotImplementedError()
