from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

base = 'Console'

executables = [
    Executable('batchprocessor.py', base=base, targetName = 'PostNLFix')
]

setup(name='PostNLInterfaceFix',
      version = '1.0',
      description = 'PostNL Interface File Fixer',
      options = dict(build_exe = buildOptions),
      executables = executables)
