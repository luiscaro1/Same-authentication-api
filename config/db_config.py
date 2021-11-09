
import os

pg_config = {
    'username' : 'ggbkaydjcwmolt',
    'password' : '1c44cb1e643943ae64c701c1e91ba0db3a9b0969b35e4f324c760492855c6ba9',
    'dbname' : 'dfkm1pao39k887',
    'host' : 'ec2-54-196-65-186.compute-1.amazonaws.com'
} if os.getenv('PYTHON_ENV') != 'development' else{
    'username' : 'postgres',
    'password' : 'postgres',
    'dbname' : 'postgres',
    'host' : 'db'
}
