# Run tests
`uv run pytest`

# Run the app
 ```
❯ uv run litestar run
sqlite+aiosqlite:///db.sqlite3
Traceback (most recent call last):
  File "/Users/till/Repositories/litestar-test/.venv/bin/litestar", line 8, in <module>
    sys.exit(run_cli())
             ^^^^^^^^^
  File "/Users/till/Repositories/tddbfhm/.venv/lib/python3.11/site-packages/litestar/__main__.py", line 6, in run_cli
    litestar_group()
  File "/Users/till/Repositories/tddbfhm/.venv/lib/python3.11/site-packages/rich_click/rich_command.py", line 367, in __call__
    return super().__call__(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/till/Repositories/tddbfhm/.venv/lib/python3.11/site-packages/click/core.py", line 1157, in __call__
    return self.main(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/till/Repositories/tddbfhm/.venv/lib/python3.11/site-packages/rich_click/rich_command.py", line 151, in main
    with self.make_context(prog_name, args, **extra) as ctx:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/till/Repositories/tddbfhm/.venv/lib/python3.11/site-packages/litestar/cli/_utils.py", line 224, in make_context
    self._prepare(ctx)
  File "/Users/till/Repositories/tddbfhm/.venv/lib/python3.11/site-packages/litestar/cli/_utils.py", line 206, in _prepare
    env = ctx.obj = LitestarEnv.from_env(ctx.params.get("app_path"), ctx.params.get("app_dir"))
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/till/Repositories/tddbfhm/.venv/lib/python3.11/site-packages/litestar/cli/_utils.py", line 114, in from_env
    loaded_app = _autodiscover_app(cwd)
                 ^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/till/Repositories/tddbfhm/.venv/lib/python3.11/site-packages/litestar/cli/_utils.py", line 340, in _autodiscover_app
    get_type_hints(value, include_extras=True).get("return") if hasattr(value, "__annotations__") else None
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/till/Repositories/tddbfhm/.venv/lib/python3.11/site-packages/typing_extensions.py", line 1230, in get_type_hints
    hint = typing.get_type_hints(
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/till/.local/share/uv/python/cpython-3.11.10-macos-aarch64-none/lib/python3.11/typing.py", line 2377, in get_type_hints
    value = _eval_type(value, base_globals, base_locals)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/till/.local/share/uv/python/cpython-3.11.10-macos-aarch64-none/lib/python3.11/typing.py", line 395, in _eval_type
    return t._evaluate(globalns, localns, recursive_guard)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/till/.local/share/uv/python/cpython-3.11.10-macos-aarch64-none/lib/python3.11/typing.py", line 905, in _evaluate
    eval(self.__forward_code__, globalns, localns),
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 1, in <module>
NameError: name 'EmptyType' is not defined
```
