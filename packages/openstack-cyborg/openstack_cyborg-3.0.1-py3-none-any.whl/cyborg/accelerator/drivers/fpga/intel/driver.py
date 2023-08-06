# Copyright 2018 Intel, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


"""
Cyborg Intel FPGA driver implementation.
"""
import subprocess

from oslo_concurrency import processutils
from oslo_log import log as logging

from cyborg.accelerator.drivers.fpga.base import FPGADriver
from cyborg.accelerator.drivers.fpga.intel import sysinfo
from cyborg.common import exception
import cyborg.privsep

LOG = logging.getLogger(__name__)


@cyborg.privsep.sys_admin_pctxt.entrypoint
def _fpga_program_privileged(cmd_args):
    # NOTE(Sundar): If we take cmd as parameter, this function can
    # be abused to run abritrary commands in privileged mode. So
    # only cmd_args are passed in.
    # TODO(Sundar) Do not hardcode fpgaconf.
    # Use right tool based on bitstream type.
    cmd = ["/usr/bin/fpgaconf"]
    cmd.extend(cmd_args)
    # processutils will log the command line.
    return processutils.execute(*cmd)


class IntelFPGADriver(FPGADriver):
    """Base class for FPGA drivers.

       This is just a virtual FPGA drivers interface.
       Vedor should implement their specific drivers.
    """
    VENDOR = "intel"

    def __init__(self, *args, **kwargs):
        pass

    def discover(self):
        return sysinfo.fpga_tree()

    def program(self, device_path, image):
        bdf = ""
        path = sysinfo.find_pf_by_vf(device_path) if sysinfo.is_vf(
            device_path) else device_path
        if sysinfo.is_bdf(device_path):
            bdf = sysinfo.get_pf_bdf(device_path)
        else:
            bdf = sysinfo.get_bdf_by_path(path)
        bdfs = sysinfo.split_bdf(bdf)
        cmd = ["sudo", "/usr/bin/fpgaconf"]
        for i in zip(["--bus", "--device", "--function"], bdfs):
            cmd.extend(i)
        cmd.append(image)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        p.wait()
        return p.returncode

    def program_v2(self, controlpath_id, image_file_path):
        """Program the FPGA with the provided bitstream image.

           TODO(Sundar): Need to handle retries.

           :param: controlpath_id
               Controlpath_id OVO
           :param: image_file_path
               String with the file path
           :returns: True on success, False on failure
        """
        if controlpath_id['cpid_type'] != "PCI":
            raise exception.InvalidType(obj='controlpath_id',
                                        type=controlpath_id['cpid_type'],
                                        expected='PCI')
        cmd_args = []
        bdf_dict = controlpath_id['cpid_info']
        bdf = map(lambda x: bdf_dict[x], ["bus", "device", "function"])
        for i in zip(["--bus", "--device", "--function"], bdf):
            cmd_args.extend(i)
        cmd_args.append(image_file_path)

        try:
            # TODO(Sundar) Check return code if it is retryable
            _fpga_program_privileged(cmd_args)
            return True
        except Exception:
            # NOTE(Sundar): processutils.exec will log the error.
            # TODO(Sundar): If retryable error, try again.
            return False
