from django.core.management.base import BaseCommand, CommandError
from prodigy.components import db
import json

class Command(BaseCommand):
    help = 'Migrates prodigy annotations to the current database'

    def add_arguments(self, parser):
        parser.add_argument('config', type=str, help='Path to old prodigy.json file')
        parser.add_argument('old_dataset', type=str, help='Name of old prodigy dataset')
        parser.add_argument('dataset', type=str, help='Name of new prodigy dataset to migrate to')
        parser.add_argument('-o', '--overwrite', action='store_true', help='Overwrite new dataset')

    def handle(self, *args, **options):
        with open(options['config']) as config_file:
            config = json.load(config_file)
            db_settings = config.get('db_settings')
            db_id = config.get('db')
            if db_settings is not None:
                if db_id is not None:
                    db_settings = db_settings.get(db_id)
                    if db_settings is None:
                        raise CommandError(f'The "db_settings" field doesn\'t contain the value for the db_id {db_id}')
                else:
                    raise CommandError('Config file doesn\'t contain the required field "db_id"')
            else:
                raise CommandError('Config file doesn\'t contain the required field "db_settings"')

        old_prodigy_db = db.connect(db_id, db_settings)
        examples = old_prodigy_db.get_dataset(options['old_dataset'])
        if examples is None:
            raise CommandError(f'The dataset "{options["old_dataset"]}" cannot be used, it\'s either empty or not created yet')
        db._DB = None # stop prodigy from reusing the saved _DB
        new_prodigy_db = db.connect()
        if options['overwrite']:
            if options['dataset'] in new_prodigy_db.datasets:
                num_examples = new_prodigy_db.count_dataset(options["dataset"])
                new_prodigy_db.drop_dataset(name=options['dataset'])
                self.stderr.write(self.style.WARNING(f'Dropped {num_examples} annotations from "{options["dataset"]}"'))
            else:
                self.stderr.write(self.style.WARNING(f'Skipping overwrite, {options["dataset"]} is not created '))
            new_prodigy_db.add_dataset(options['dataset'])
        new_prodigy_db.add_examples(examples, datasets=[options['dataset']])
        
        self.stdout.write(self.style.SUCCESS(f'Successfully migrated {len(examples)} examples from "{options["old_dataset"]}" to "{options["dataset"]}"'))
