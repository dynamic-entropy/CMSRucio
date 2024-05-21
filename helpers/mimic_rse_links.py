from rucio.client import Client
from rucio.common.exception import Duplicate
import argparse


def mimic_rse_links(client, rse_to_mimic, rse_to_set, dry_run=False):

    rses = client.list_rses()

    for rse in rses:
        # get distance for reference rse
        a = client.get_distance(rse['rse'], rse_to_mimic)
        b = client.get_distance(rse_to_mimic, rse['rse'])

        # Add same distances for rse in concern
        if len(a) != 0:
            a = a[0]
            try:
                print(f"Setting distance from {rse['rse']} to {rse_to_set} to {a['distance']}")
                if not dry_run:
                    client.add_distance(rse['rse'], rse_to_set, {'distance': a['distance']})
            except Duplicate:
                print(f"Distance from {rse['rse']} to {rse_to_set} already exists")
                client.update_distance(rse['rse'], rse_to_set, {'distance': a['distance']})
            except Exception as e:
                print(f"Failed to set distance from {rse['rse']} to {rse_to_set}", e)
        # else:
        #     print(f"Distance from {rse['rse']} to {rse_to_mimic} does not exists")

        if len(b) != 0:
            b = b[0]
            try:
                print(f"Setting distance from {rse_to_set} to {rse['rse']} to {b['distance']}")
                client.add_distance(rse_to_set, rse['rse'], {'distance': b['distance']})
            except Duplicate:
                print(f"Distance from {rse_to_set} to {rse['rse']} already exists")
                client.update_distance(rse_to_set, rse['rse'], {'distance': b['distance']})
            except Exception as e:
                print(f"Failed to set distance from {rse_to_set} to {rse['rse']}", e)
        # else:
        #     print(f"Distance from {rse_to_mimic} to {rse['rse']} does not exists")

# Verfify successful operation


def verify_rse_links(client, rse_to_mimic, rse_to_set):
    for rse in client.list_rses():
        a1 = client.get_distance(rse['rse'], rse_to_set)[0] if len(client.get_distance(rse['rse'], rse_to_set)) !=0 else None
        b1 = client.get_distance(rse_to_set, rse['rse'])[0] if len(client.get_distance(rse_to_set, rse['rse'])) !=0 else None

        a2 = client.get_distance(rse['rse'], rse_to_mimic)[0] if len(client.get_distance(rse['rse'], rse_to_mimic)) !=0 else None
        b2 = client.get_distance(rse_to_mimic, rse['rse'])[0] if len(client.get_distance(rse_to_mimic, rse['rse'])) !=0 else None

        try:
            assert a1['distance'] == a2['distance']
            assert b1['distance'] == b2['distance']
        except IndexError:
            print('Index error for %s' % rse['rse'])
        except Exception as e:
            print(f"Failed to verify distance for rse {rse['rse']}", e)


def set_link_with_rse_to_mimic(client, rse_to_mimic, rse_to_set, dry_run=False):
    try:
        print(f"Setting distance from {rse_to_mimic} to {rse_to_set} to 1")
        if not dry_run:
            client.add_distance(rse_to_mimic, rse_to_set, {'distance': 1})
    except Duplicate:
        print(f"Distance from {rse_to_mimic} to {rse_to_set} already exists")
        client.update_distance(rse_to_mimic, rse_to_set, {'distance': 1})
    except Exception as e:
        print(f"Failed to set distance from {rse_to_mimic} to {rse_to_set}", e)

    try:
        print(f"Setting distance from {rse_to_set} to {rse_to_mimic} to 1")
        if not dry_run:
            client.add_distance(rse_to_set, rse_to_mimic, {'distance': 1})
    except Duplicate:
        print(f"Distance from {rse_to_set} to {rse_to_mimic} already exists")
        client.update_distance(rse_to_set, rse_to_mimic, {'distance': 1})
    except Exception as e:
        print(f"Failed to set distance from {rse_to_set} to {rse_to_mimic}", e)


if __name__ == '__main__':
    # Take RSE to mimic and RSE to set as arguments

    parser = argparse.ArgumentParser(description='Mimic RSE links')
    parser.add_argument('rse_to_mimic', type=str, help='RSE to mimic')
    parser.add_argument('rse_to_set', type=str, help='RSE to set')
    parser.add_argument('--dry-run', action='store_true', help='Dry run')
    args = parser.parse_args()

    client = Client()
    mimic_rse_links(client, args.rse_to_mimic, args.rse_to_set, args.dry_run)
