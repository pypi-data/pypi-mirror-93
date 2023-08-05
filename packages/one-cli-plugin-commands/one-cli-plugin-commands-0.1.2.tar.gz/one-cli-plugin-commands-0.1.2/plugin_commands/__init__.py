import click
import yaml
from one.__init__ import CONFIG_FILE
from one.docker.container import Container
from one.docker.image import Image
from one.utils.environment.aws import EnvironmentAws
from one.one import cli


container = Container()
image = Image()
environment = EnvironmentAws()
SHELL_IMAGE = image.get_image('shell')


def make_callback(image, command, ports, entrypoint, volumes, environment):
    def callback():
        container.create(
            image=image,
            command=command,
            ports=ports,
            entrypoint=entrypoint,
            volumes=volumes,
            environment=environment
        )
    return callback


def __init__():

    try:
        with open(CONFIG_FILE) as file:
            docs = yaml.load(file, Loader=yaml.FullLoader)

        for cmd in docs['commands']:
            envs = cmd.get('environment', [])
            environment = {}
            for env in envs:
                environment[list(env.keys())[0]] = list(env.values())[0]
            func = make_callback(
                image=cmd.get('image', SHELL_IMAGE),
                command=cmd.get('command', None),
                ports=cmd.get('ports', []),
                entrypoint=cmd.get('entrypoint', None),
                volumes=cmd.get('volumes', []),
                environment=environment
            )

            command = click.Command(
                name=cmd.get('name', ''),
                help=cmd.get('help', ''),
                callback=func
            )

            cli.add_command(command)
    except KeyError:
        pass
    except TypeError:
        pass
    except AttributeError:
        click.echo(
            click.style('WARN ', fg='yellow') +
            'Commands block declared but empty.\n'
        )
    except Exception:
        pass
