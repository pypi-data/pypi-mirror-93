#!/usr/bin/env python3

#
# NOSA HEADER START
#
# The contents of this file are subject to the terms of the NASA Open
# Source Agreement (NOSA), Version 1.3 only (the "Agreement").  You may
# not use this file except in compliance with the Agreement.
#
# You can obtain a copy of the agreement at
#   docs/NASA_Open_Source_Agreement_1.3.txt
# or
#   https://cdaweb.gsfc.nasa.gov/WebServices/NASA_Open_Source_Agreement_1.3.txt.
#
# See the Agreement for the specific language governing permissions
# and limitations under the Agreement.
#
# When distributing Covered Code, include this NOSA HEADER in each
# file and include the Agreement file at
# docs/NASA_Open_Source_Agreement_1.3.txt.  If applicable, add the
# following below this NOSA HEADER, with the fields enclosed by
# brackets "[]" replaced with your own identifying information:
# Portions Copyright [yyyy] [name of copyright owner]
#
# NOSA HEADER END
#
# Copyright (c) 2018-2020 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#

"""
Example Coordinate Data Analysis System (CDAS) web service client.
Includes example calls to most of the web services.

Copyright &copy; 2018-2020 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

import sys
import getopt
import json
import logging
import logging.config
from typing import List
import urllib3
#import matplotlib.pyplot as plt
from cdasws import CdasWs
from cdasws.timeinterval import TimeInterval
from cdasws.datarequest import GraphOptions, ImageFormat, Overplot


logging.basicConfig()
LOGGING_CONFIG_FILE = 'logging_config.json'
try:
    with open(LOGGING_CONFIG_FILE, 'r') as fd:
        logging.config.dictConfig(json.load(fd))
except BaseException as exc:    # pylint: disable=broad-except
    if not isinstance(exc, FileNotFoundError):
        print('Logging configuration failed')
        print('Exception: ', exc)
        print('Ignoring failure')
        print()


ENDPOINT = 'https://cdaweb.gsfc.nasa.gov/WS/cdasr/1/dataviews/sp_phys/'
#CA_CERTS = '/etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt'


def print_usage(
        name: str
    ) -> None:
    """
    Prints program usage information to stdout.

    Parameters
    ----------
    name
        name of this program

    Returns
    -------
    None
    """
    print('USAGE: {name} [-e url][-d][-c cacerts][-h]'.format(name=name))
    print('WHERE: url = CDAS web service endpoint URL')
    print('       -d disables TLS server certificate validation')
    print('       cacerts = CA certificate filename')


def example(
        argv: List[str]
    ) -> None: # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    """
    Example Coordinate Data Analysis System (CDAS) web service client.
    Includes example calls to most of the web services.

    Parameters
    ----------
    argv
        Command-line arguments.<br>
        -e url or --endpoint=url where url is the cdas web service endpoint
            URL to use.<br>
        -c url or --cacerts=filename where filename is the name of the file
            containing the CA certificates to use.<br>
        -d or --disable-cert-check to disable verification of the server's
            certificate
        -h or --help prints help information.
    """

    try:
        opts = getopt.getopt(argv[1:], 'he:c:d',
                             ['help', 'endpoint=', 'cacerts=',
                              'disable-cert-check'])[0]
    except getopt.GetoptError:
        print('ERROR: invalid option')
        print_usage(argv[0])
        sys.exit(2)

#    logger = logging.getLogger(__name__)

    endpoint = ENDPOINT
    ca_certs = None
    disable_ssl_certificate_validation = False

    for opt, arg in opts:
        if opt in ('-e', '--endpoint'):
            endpoint = arg
        elif opt in ('-c', '--cacerts'):
            ca_certs = arg
        elif opt in ('-d', '--disable-cert-check'):
            disable_ssl_certificate_validation = True
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        elif opt in ('-h', '--help'):
            print_usage(argv[0])
            sys.exit()

    cdas = CdasWs(endpoint=endpoint, ca_certs=ca_certs,
                  disable_ssl_certificate_validation=
                  disable_ssl_certificate_validation)

    print(cdas.get_observatory_groups(
        instrumentType='Magnetic Fields (Balloon)'))
    print(cdas.get_instrument_types(observatory='AC'))
    print(cdas.get_instruments(observatory='AC'))
    print(cdas.get_observatories(
        instrumentType='Magnetic Fields (space)'))
    print(cdas.get_observatory_groups_and_instruments(\
                   instrumentType='Magnetic Fields (space)'))
    datasets = cdas.get_datasets(observatoryGroup=['ACE'],
                                 instrumentType='Magnetic Fields (space)')
    print('Datasets:')
    for dataset in datasets:
        print('  ', dataset['Id'], dataset['Label'])

    mms_brst_inventory = cdas.get_inventory('MMS1_FPI_BRST_L2_DES-MOMS',
                                            timeInterval=TimeInterval(
                                                '2018-08-30T08:09:53Z',
                                                '2018-08-30T08:52:00Z'))
    print('MMS1_FPI_BRST_L2_DES-MOMS inventory:')
    for interval in mms_brst_inventory:
        print('    ' + str(interval))

    doi_inventory = cdas.get_inventory('10.21978/P8T923')
    print('10.21978/P8T923 inventory:')
    for interval in doi_inventory:
        print('    ' + str(interval))

    variables = cdas.get_variables('AC_H0_MFI')
    if variables is not None:
        print('Variable Names:')
        for variable in variables:
            print('    ' + variable['Name'])

    try:

        while True:  # status == 503 and Retry-After header
            status, data = \
                cdas.get_data('AC_H1_MFI', ['Magnitude', 'BGSEc'],
                              '2009-06-01T00:00:00Z', '2009-12-01T00:10:00Z'
                              #'2009-06-01T00:00:00Z', '2009-06-01T00:10:00Z'
                              #binData={
                              #    'interval': 60.0,
                              #    'interpolateMissingValues': True,
                              #    'sigmaMultiplier': 4,
                              #    'overrideDefaultBinning': True
                              #}
                              )
#                cdas.get_data('10.21978/P8PG8V', ['BT'],
#                              '1987-09-24T00:00:00Z', '1987-09-24T01:00:00Z'
            if status['http']['status_code'] != 503:
                break

        if status['http']['status_code'] == 200:
            print(data)
            #print(data.attrs)
            #plt.plot(data['Epoch'], data['Magnitude'])
            #plt.xlabel(data['Epoch'].attrs['LABLAXIS'])
            #plt.ylabel(data['Magnitude'].attrs['LABLAXIS'] + ' ' +
            #           data['Magnitude'].attrs['UNITS'])
            #plt.show()
        else:
            print('Request failed with status = ', status)
    except ImportError:
        print('-----------------------------------------------------------')
        print('Skipping the get_data() method because it requires spacepy.')
        print('To use get_data(), install spacepy and re-run this example.')
        print('That is, do the following:')
        print('pip install spacepy')
        print('-----------------------------------------------------------')

    status, result = \
        cdas.get_graph('AC_H1_MFI', ['Magnitude', 'BGSEc'],
                       '2009-06-01T00:00:00Z', '2009-06-01T00:10:00Z',
                       GraphOptions(coarse_noise_filter=True,
                                    y_axis_height_factor=2,
                                    combine=True,
                                    overplot=Overplot.VECTOR_COMPONENTS),
                       [ImageFormat.PDF]
                       #binData={
                       #    'interval': 60.0,
                       #    'interpolateMissingValues': True,
                       #    'sigmaMultiplier': 4
                       #}
                       )

    if status == 200:
        print(result)
    else:
        print('Request failed with status = ', status)


    status, result = \
        cdas.get_graph('IM_K0_EUV', ['IMAGE'],
                       '2005-01-01T00:00:00Z', '2005-01-02T00:00:00Z')

    if status == 200:
        print(result)

        thumbnail_id = result['FileDescription'][0].get('ThumbnailId', None)
        if thumbnail_id is not None:
            thumbnail = result['FileDescription'][0]['ThumbnailDescription']['NumFrames'] // 2
            status, result = \
                cdas.get_thumbnail('IM_K0_EUV', ['IMAGE'],
                                   '2005-01-01T00:00:00Z',
                                   '2005-01-02T00:00:00Z',
                                   thumbnail_id, thumbnail)
        if status == 200:
            print(result)
        else:
            print('Request failed with status = ', status)
    else:
        print('Request failed with status = ', status)


    status, result = \
        cdas.get_text('AC_H1_MFI', ['Magnitude', 'BGSEc'],
                      '2009-06-01T00:00:00Z', '2009-06-01T00:10:00Z',
                      #binData={
                      #    'interval': 60.0,
                      #    'interpolateMissingValues': True,
                      #    'sigmaMultiplier': 4
                      #}
                      )

    if status == 200:
        print(result)
    else:
        print('Request failed with status = ', status)


    status, result = \
        cdas.get_audio('AC_H1_MFI', ['Magnitude', 'BGSEc'],
                       '2009-06-01T00:00:00Z', '2009-06-01T00:10:00Z',
                       #binData={
                       #    'interval': 60.0,
                       #    'interpolateMissingValues': True,
                       #    'sigmaMultiplier': 4
                       #}
                       )

    if status == 200:
        print(result)
    else:
        print('Request failed with status = ', status)


if __name__ == '__main__':
    example(sys.argv)
