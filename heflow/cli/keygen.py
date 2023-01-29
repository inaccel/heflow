import click
import joblib
import json
import pathlib
import tenseal


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


@click.command(options_metavar='[options] — HEflow authentication key utility')
@click.option('-f',
              help='Specifies the filename of the key file.',
              type=pathlib.Path,
              metavar='filename')
@click.option(
    '-O',
    multiple=True,
    help=
    'Specify a key/value option.  These are specific to the operation that heflow-keygen has been requested to perform.  The -O option may be specified multiple times.',
    callback=jsondict,
    metavar='option')
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
    default=False,
    metavar='')
@click.option('-q', help='Silence heflow-keygen.', default=False, metavar='')
@click.pass_context
def command(ctx, f, o, t, y, q):
    """
    heflow-keygen [-b bits] [-f output_keyfile] [-O option] [-t ckks]

    heflow-keygen -y [-f input_keyfile]
    """
    if y:
        if not f:
            f = click.prompt('Enter file in which the key is',
                             'id_ckks',
                             type=click.Path(path_type=pathlib.Path))
        try:
            context = tenseal.context_from(
                joblib.load(click.open_file(f, 'rb')))
        except OSError as ose:
            click.echo(f'{f}: {ose.strerror}', err=True)
            ctx.exit(255)
        joblib.dump(context.serialize(), click.get_binary_stream('stdout'))
    elif t == 'ckks':
        if not q:
            click.echo(f'Generating public/private {t} key pair.')
        context = tenseal.context(tenseal.SCHEME_TYPE.CKKS,
                                  o.get('poly_modulus_degree', 16384),
                                  coeff_mod_bit_sizes=o.get(
                                      'coeff_modulus_bit_sizes',
                                      [52, 52, 52, 52, 52, 52, 52]))
        context.global_scale = 2**o.get('scale_bit_size', 52)
        context.generate_galois_keys()
        if not f:
            f = click.prompt('Enter file in which to save the key',
                             'id_ckks',
                             type=click.Path(path_type=pathlib.Path))
        if f.exists():
            click.echo(f'{f} already exists.')
            if click.prompt(
                    'Overwrite (y/n)', '', prompt_suffix='? ',
                    show_default=False) != 'y':
                ctx.exit(1)
        try:
            joblib.dump(context.serialize(save_secret_key=True), f)
        except OSError as ose:
            click.echo(f'Saving key "{f}" failed: {ose.strerror}', err=True)
            ctx.exit(255)
        if not q:
            click.echo(f'Your identification has been saved in {f}')
        try:
            joblib.dump(context.serialize(), f'{f}.pub')
        except OSError as ose:
            click.echo(f'Unable to save public key to {f}.pub: {ose.strerror}',
                       err=True)
            ctx.exit(255)
        if not q:
            click.echo(f'Your public key has been saved in {f}.pub')
    else:
        click.echo(f'unknown key type {t}', err=True)


if __name__ == '__main__':
    command()
