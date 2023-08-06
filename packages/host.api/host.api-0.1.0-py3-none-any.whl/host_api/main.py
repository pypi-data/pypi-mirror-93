import os
import sys
import typer
import uvicorn
from fastapi import FastAPI

curdir = os.getcwd()
curpath = sys.path

app = FastAPI(title='host.api web',
              debug=True,
              description='Sistema web para administração de recepção, agenda e financeiro.',
              version='0.1.0')

cliapp = typer.Typer(name='host.api cli')



@app.on_event('startup')
async def into():
    typer.secho(f'Iniciando {app.title} ({app.version})', fg=typer.colors.GREEN)


@app.on_event('shutdown')
async def end():
    typer.secho(f'Finalizando {app.title} ({app.version})', fg=typer.colors.RED)


@app.get('/')
async def root():
    return {'msg': 'Seja bem vindo ao host.api web'}

@cliapp.command('app')
def runapp():
    typer.run(uvicorn.run('main:app', host='127.0.0.1', port=5000, reload=True))



if __name__ == '__main__':
    print(curdir)
    print(curpath)
    uvicorn.run('main:app', host='127.0.0.1', port=5000, reload=True)

