#!/usr/bin/env python3
"""Select only the active scan created by this plan, never a previous scan."""
import json
import sys
from datetime import datetime


def scan_ids(document):
    return [str(scan['id']) for scan in document['scans']]


def new_scan(document, previous):
    candidates = [scan for scan in document['scans'] if str(scan['id']) not in previous]
    if len(candidates) != 1:
        raise ValueError('expected exactly one new active scan; observed %d' % len(candidates))
    return str(candidates[0]['id'])


def record(document, scan_id):
    matches = [scan for scan in document['scans'] if str(scan['id']) == scan_id]
    if len(matches) != 1:
        raise ValueError('the current plan scan is missing from the API response')
    return matches[0]


def main():
    action, *arguments = sys.argv[1:]
    document = json.load(sys.stdin)
    if not isinstance(document, dict):
        raise ValueError('expected a JSON object')
    if action == 'plan-finished':
        value = document.get('finished')
        if not isinstance(value, str) or 'T' not in value:
            return 1
        completed = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return 0 if completed.tzinfo is not None else 1
    if action == 'plan-errors':
        errors = document['error']
        if not isinstance(errors, list):
            raise ValueError('expected a plan error list')
        print(len(errors))
    elif action == 'ids':
        print(json.dumps(scan_ids(document)))
    elif action == 'new':
        print(new_scan(document, json.loads(arguments[0])))
    elif action == 'record':
        scan = record(document, arguments[0])
        print('|'.join(str(scan.get(key, '')) for key in ('id', 'progress', 'state', 'reqCount')))
    else:
        raise ValueError('unknown scan query')


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, KeyError, TypeError, IndexError) as error:
        print('Scan identity check: ' + str(error), file=sys.stderr)
        sys.exit(1)
