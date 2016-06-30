#!/usr/bin/env python

import urlparse
import urllib
import time

import click
import requests


@click.command()
@click.option('-t', '--auth-token', prompt='Auth token')
@click.argument('urls', nargs=-1)
def find_and_reprocess(auth_token, urls):
    """Pass multiple SuperSearch URLS. It can be the URL from a web
    search or from a API."""
    if not urls:
        click.echo('Must have at least 1 url')
        raise click.Abort

    base_url = None
    scheme = None
    for url in urls:
        if base_url is None:
            base_url = urlparse.urlparse(url).netloc
            scheme = urlparse.urlparse(url).scheme
        elif urlparse.urlparse(url).netloc != base_url:
            click.echo('Every URL must have the same base hostname')
            raise click.Abort

    crash_ids = []
    for url in urls:
        find_crash_ids(url, auth_token, crash_ids)

    click.echo(
        'Found {} Crash IDs. ({} unique/distinct)'.format(
            len(crash_ids),
            len(set(crash_ids)),
        )
    )
    click.confirm('Want to send them in for reprocessing now?', abort=True)
    click.echo('')
    click.echo("Here we go! Please don't restart your computer now.")

    url = scheme + '://' + base_url + '/api/Reprocessing/'

    sleep = 1
    size = 50
    crash_ids = list(set(crash_ids))
    groups = [
        crash_ids[i:i + size] for i in range(0, len(crash_ids), size)
    ]

    for i, group in enumerate(groups):
        print i * size, 'to', (i + 1) * size
        response = requests.post(urlm, data={'crash_ids': group}, headers={
            'Auth-Token': auth_token
        })
        assert response.status_code==200, response.status_code
        click.echo(
            'Sleeping {} {}'.format(
                sleep,
                'seconds' if sleep > 1 else 'second'
            )
        )
        time.sleep(sleep)

    click.echo('Hurray!! You did it!')


def find_crash_ids(url, auth_token, store, limit=500, offset=0):
    split = urlparse.urlsplit(url)
    query = urlparse.parse_qs(split.query)
    # remove things we don't need
    meta_keys = [x for x in query if x.startswith('_')]
    for key in meta_keys:
        if key in query:
            del query[key]
    query['_columns'] = ['uuid']
    query['_results_number'] = limit
    query['_results_offset'] = offset
    split = split._replace(fragment=None)
    split = split._replace(query=urllib.urlencode(query, True))
    split = split._replace(path='/api/SuperSearch/')
    url = split.geturl()
    query = split.query
    click.echo(
        'Page {} {}'.format(
            str(offset / limit + 1).ljust(2),
            query[:100] + '...' if len(query) > 100 else query
        )
    )
    response = requests.get(url, headers={'Auth-Token': auth_token})
    assert response.status_code == 200, response.status_code
    results = response.json()
    total = results['total']
    for hit in results['hits']:
        store.append(hit['uuid'])
    # Do we need to go to the next page?
    if total > offset + len(results['hits']):
        find_crash_ids(
            url,
            auth_token,
            store,
            limit=limit,
            offset=offset + limit,
        )


if __name__ == '__main__':
    find_and_reprocess()
