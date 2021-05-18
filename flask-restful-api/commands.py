# -*- coding: utf-8 -*-
import click

from __init__ import app, db
from models import User, Resource

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
def forgersc():
    """Generate fake data."""
    db.create_all()

    resources = [
        {'resource_name': 'ad-adlab-hil-1', 'status': 'active', 'description': 'AD Lab Vector HIL rig for VCU1 and AD sensors', 'resource_type': 'HIL'},
        {'resource_name': 'adas-component-hil', 'status': 'active', 'description': 'asdm flc2 flr production rig', 'resource_type': 'HIL'},
        {'resource_name': 'eh-icup-1', 'status': 'active', 'description': 'used for EH 522A and 622A project test', 'resource_type': 'Boxcar'},
        {'resource_name': 'adas-domian-hil-argus2-pds-1', 'status': 'removed', 'description': 'PDS ADAS HIL rig', 'resource_type': 'HIL'},
        {'resource_name': 'steer-component-pscm-cma-pds-2', 'status': 'maintenance', 'description': 'PDS steer bench', 'resource_type': 'Test bench'},
    ]

    for r in resources:
        resource = Resource(resource_name=r['resource_name'], status=r['status'], description=r['description'], resource_type=r['resource_type'])
        db.session.add(resource)

    db.session.commit()
    click.echo('Done.')

@app.cli.command()
@click.option('--email', prompt=True, help='Your company email.')
@click.option('--CDSID', prompt=True, help='CDSID is used to login.')
@click.option('--username', prompt=True, help='Displayed name')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(email, cdsid, username, password):
    """Create admin user."""
    db.create_all()

    click.echo('Creating admin user...')
    user = User(email=email, cdsid=cdsid, username=username, user_type='admin')
    user.set_password(password)
    db.session.add(user)

    db.session.commit()
    click.echo('Done.')
