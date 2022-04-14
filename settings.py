import environ
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

env = environ.Env(
    POSTGRES_URL=(str, 'postgres://dev:dev@localhost:5432/fitness'),
    DEBUG=(bool, False)
)


TORTOISE_ORM = {
    'connections': {
        'default': env('POSTGRES_URL')
    },
    'apps': {
        'models': {
            'models': ['models', 'aerich.models'],
            'default_connection': 'default',
        }
    }
}

DEBUG = env('DEBUG')
