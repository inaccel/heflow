import click
import heflow.keys
import joblib
import json
import pathlib


def jsondict(ctx, param, value):
    if isinstance(value, tuple):
        options = value
    else:
        options = (value, )
    d = {}
    for option in options:
        key, value = option.split('=', 1)
        d[key] = json.loads(value)
    return d


@click.command(options_metavar='[options] — HEflow computation key utility')
@click.option(
    '-E',
    help=
    'Specifies the hash algorithm used when displaying key fingerprints.  Valid options are: "md5" and "sha256".  The default is "sha256".',
    default='sha256',
    metavar='fingerprint_hash')
@click.option('-f',
              help='Specifies the filename of the key file.',
              type=pathlib.Path,
              metavar='filename')
@click.option(
    '-l',
    is_flag=True,
    help=
    'Show fingerprint of specified public key file.  For CKKS keys heflow-keygen tries to find the matching public key file and prints its fingerprint.',
    metavar='')
@click.option(
    '-O',
    multiple=True,
    help=
    'Specify a key/value option.  These are specific to the operation that heflow-keygen has been requested to perform.  The -O option may be specified multiple times.',
    callback=jsondict,
    metavar='option')
@click.option('-q', is_flag=True, help='Silence heflow-keygen.', metavar='')
@click.option(
    '-t',
    help=
    'Specifies the type of key to create.  The possible values are "ckks".',
    default='ckks',
    metavar='ckks')
@click.option(
    '-y',
    is_flag=True,
    help=
    'This option will read a private HEflow format file and print an HEflow public key to stdout.',
    metavar='')
@click.pass_context
def command(ctx, e, f, l, o, q, t, y):
    """
    heflow-keygen [-q] [-f output_keyfile] [-O option] [-t ckks]

    heflow-keygen -y [-f input_keyfile]

    heflow-keygen -l [-E fingerprint_hash] [-f input_keyfile]
    """
    if l:
        if not f:
            if t not in ['ckks']:
                click.echo('bad key type', err=True)
                ctx.exit(255)
            f = click.prompt('Enter file in which the key is',
                             f'id_{t}',
                             type=click.Path(path_type=pathlib.Path))
        try:
            key = joblib.load(click.open_file(f, 'rb'))
        except OSError as ose:
            click.echo(f'{f}: {ose.strerror}', err=True)
            ctx.exit(255)
        except Exception:
            click.echo(f'{f} is not a public key file.', err=True)
            ctx.exit(255)
        if isinstance(key, heflow.keys.CKKSKey):
            try:
                click.echo(f'{key.fingerprint(e)} (CKKS)')
            except ValueError:
                click.echo(f'Invalid hash algorithm "{e}"', err=True)
                ctx.exit(255)
        else:
            click.echo(f'{f} is not a public key file.', err=True)
            ctx.exit(255)
    elif y:
        if not f:
            if t not in ['ckks']:
                click.echo('bad key type', err=True)
                ctx.exit(255)
            f = click.prompt('Enter file in which the key is',
                             f'id_{t}',
                             type=click.Path(path_type=pathlib.Path))
        try:
            key = joblib.load(click.open_file(f, 'rb')).public_key()
        except OSError as ose:
            click.echo(f'{f}: {ose.strerror}', err=True)
            ctx.exit(255)
        except Exception:
            click.echo(f'Load key "{f}": error in heflow', err=True)
            ctx.exit(255)
        joblib.dump(key, click.get_binary_stream('stdout'))
    else:
        if t not in ['ckks']:
            click.echo(f'unknown key type {t}', err=True)
            ctx.exit(255)

        if not q:
            click.echo(f'Generating public/private {t} key pair.')
        if t == 'ckks':
            key = heflow.keys.ckks_key(
                coeff_modulus_bit_sizes=o.get('coeff_modulus_bit_sizes',
                                              [52, 52, 52, 52, 52, 52, 52]),
                poly_modulus_degree=o.get('poly_modulus_degree', 16384),
                scale_bit_size=o.get('scale_bit_size', 52))
        if not f:
            f = click.prompt('Enter file in which to save the key',
                             f'id_{t}',
                             type=click.Path(path_type=pathlib.Path))
        if f.exists():
            click.echo(f'{f} already exists.')
            if click.prompt(
                    'Overwrite (y/n)', '', prompt_suffix='? ',
                    show_default=False) != 'y':
                ctx.exit(1)
        try:
            joblib.dump(key, f)
        except OSError as ose:
            click.echo(f'Saving key "{f}" failed: {ose.strerror}', err=True)
            ctx.exit(255)
        if not q:
            click.echo(f'Your identification has been saved in {f}')
        try:
            joblib.dump(key.public_key(), f'{f}.pub')
        except OSError as ose:
            click.echo(f'Unable to save public key to {f}.pub: {ose.strerror}',
                       err=True)
            ctx.exit(255)
        if not q:
            click.echo(f'Your public key has been saved in {f}.pub')
            click.echo('The key fingerprint is:')
            try:
                click.echo(key.fingerprint(e))
            except ValueError:
                click.echo(f'Invalid hash algorithm "{e}"', err=True)
                ctx.exit(255)


if __name__ == '__main__':
    command()
