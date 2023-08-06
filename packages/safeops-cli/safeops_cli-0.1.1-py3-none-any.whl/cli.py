#!/usr/bin/env python

import click
import requests
import time

@click.group()
def process():
    pass

@click.command()
@click.option('-host', '-h', 'host', default='https://api.safeops.io/',help='Safeops Host url')
@click.option('--apikey', '-a', 'api_key', required=True, help='API key to the safeops account')
@click.option('--scan', '-s', 'scans',
              type=click.Choice(['app', 'repos', 'cloud']),
              default=['app', 'repos', 'cloud'],
              help='Scan to run, by default it runs all scans',
              multiple=True)
def start_scans(host, api_key, scans):
    header = {'Authorization': 'Api-Key ' + api_key}
    data = {'scans': list(scans)}
    if host.endswith('/'):
        host_url = host
    else:
        host_url = host + '/'

    res = requests.post(host_url + 'scan/start-scans', json=data, headers=header)
    if res.status_code == 200:
        data = res.json()
        click.echo(data.get('message'))
    elif res.status_code == 401:
        click.echo('Invalid api key', err=True)
    else:
        click.echo('something went wrong', err=True)


@click.command()
@click.option('-host', '-h', 'host', default='https://api.safeops.io/', help='Safeops Host url')
@click.option('--apikey', '-a', 'api_key', required=True, help='API key to the safeops account')
@click.option('--timeout', '-t', 'timeout', default=3000, help='time to wait for the results to be ready in seconds')
def get_results(host, api_key, timeout):
    start = time.time()
    wait  = True
    header = { 'Authorization': 'Api-Key ' + api_key }
    if host.endswith('/'):
        host_url = host
    else:
        host_url = host + '/'
    while wait:
        res = requests.get(host_url + 'scan/scan-results', headers=header)
        result = res.json()
        if result.get('status') == 'COMPLETE':
            if result.get('critical_fail'):
                click.echo("FAIL", err=True)
                return 1
            elif result.get('fails', 0) > 0:
                click.echo("FAIL", err=True)
                return 1
            elif result.get('generail_score_fail', True):
                click.echo("FAIL", err=True)
                return 1
            else:
                click.echo("SUCCESS")
                return 0

        if time.time() - start >= timeout:
            return click.echo('process timeout', err=True)

        time.sleep(10)

process.add_command(start_scans)
process.add_command(get_results)

if __name__ =='__main__':
    process()
