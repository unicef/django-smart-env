# Extra

### storage

We do have the possibility to use env.storage to unpack a variable (better if an environment variable) similarly to how django-environ db_url works (https://django-environ.readthedocs.io/en/latest/types.html#environ-env-db-url).

example:

FILE_STORAGE_STATIC=storages.backends.azure_storage.AzureStorage?account_name=account&account_key=key==&azure_container=static&overwrite_files=True&expiration_secs=30

env.storage("FILE_STORAGE_STATIC")

{
  'BACKEND': 'storages.backends.azure_storage.AzureStorage',
  'OPTIONS': {
    'account_name': 'account',
    'account_key': 'key==',
    'azure_container': 'static',
    'overwrite_files': 'True',
    'expiration_secs': 30
  }
}
