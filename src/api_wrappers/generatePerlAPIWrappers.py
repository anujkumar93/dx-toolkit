#!/usr/bin/env python

import sys, json

preamble = '''# Do not modify this file by hand.
#
# It is automatically generated by src/api_wrappers/generatePerlAPIWrappers.py.
# (Run make api_wrappers to update it.)

package DNAnexus::API;

use strict;
use Exporter;
use DNAnexus qw(DXHTTPRequest);
'''

postscript = '''
our @ISA = "Exporter";
our @EXPORT_OK = qw({all_method_names});
'''

class_method_template = '''
sub {method_name}(;$%) {{
    my ($input_params, %kwargs) = @_;
    %kwargs = () unless %kwargs;
    return DXHTTPRequest('{route}', $input_params, %kwargs);
}}
'''

object_method_template = '''
sub {method_name}($;$%) {{
    my ($object_id, $input_params, %kwargs) = @_;
    %kwargs = () unless %kwargs;
    return DXHTTPRequest('/'.$object_id.'/{method_route}', $input_params, %kwargs);
}}
'''

app_object_method_template = '''
sub {method_name}($;$%) {{
    my ($app_id_or_name, $input_params, %kwargs) = @_;
    %kwargs = () unless %kwargs;
    return DXHTTPRequest('/'.$app_id_or_name.'/{method_route}', $input_params, %kwargs);
}}

sub {method_name}WithAlias($;$%) {{
    my ($app_name, $app_alias, $input_params, %kwargs) = @_;
    %kwargs = () unless %kwargs;
    return {method_name}($app_name.'/'.$app_alias, $input_params, %kwargs);
}}
'''

print preamble

all_method_names = []

for method in json.loads(sys.stdin.read()):
    route, signature, opts = method
    method_name = signature.split("(")[0]
    if (opts['objectMethod']):
        root, oid_route, method_route = route.split("/")
        if oid_route == 'app-xxxx':
            print app_object_method_template.format(method_name=method_name, method_route=method_route)
        else:
            print object_method_template.format(method_name=method_name, method_route=method_route)
    else:
        print class_method_template.format(method_name=method_name, route=route)
    all_method_names.append(method_name)

print postscript.format(all_method_names=" ".join(all_method_names))
