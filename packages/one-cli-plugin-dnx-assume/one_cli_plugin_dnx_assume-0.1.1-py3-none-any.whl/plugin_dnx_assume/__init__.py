import click
from one.one import cli
from one.utils.environment.aws import EnvironmentAws
from one.utils.environment.common import create_secrets
from one.__init__ import CLI_ROOT
from one.utils.config import get_config_value


def __init__():
    cli.add_command(dnx_assume)


@click.command(name='dnx-assume', help='DNX assume wrap command entry.')
@click.option('-r', '--aws-role', 'aws_role', default=None, type=str, help='AWS role to assume.')
@click.option('-i', '--aws-account-id', 'aws_account_id', default=None, type=str, help='AWS account id to assume.')
def dnx_assume(aws_role, aws_account_id):
    aws_role = aws_role or get_config_value('plugins.dnx-assume.parameters.aws_role')
    aws_account_id = aws_account_id or get_config_value('plugins.dnx-assume.parameters.aws_account_id')

    credentials = EnvironmentAws().build(
        aws_role=aws_role,
        aws_account_id=aws_account_id,
        aws_assume_role='true'
    ).get_env()

    create_secrets(credentials, CLI_ROOT + '/secrets')
