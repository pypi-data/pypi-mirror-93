from functools import lru_cache


@lru_cache()
def get_app():
    import typer
    from threedi_cmd_statistics.commands.app_definitions import registry
    main_app = typer.Typer()
    for app_name, app_meta in registry.apps.items():
        main_app.add_typer(app_meta.app, name=app_meta.name, help=app_meta.help)
    return main_app


if __name__ == '__main__':
    app = get_app()
    app()
