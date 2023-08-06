import typer
import asyncio
from enum import Enum
from datetime import datetime
from typing import Optional


app = typer.Typer(name='Keygen.api')

class GenderEnum(int, Enum):
    undefined = 0
    male = 1
    female = 2
    trans_male = 3
    trans_female = 4


async def generate_key_for_person(fullname:str,
                            birthdate: datetime = typer.Argument(..., formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y"]),
                            gender: Optional[GenderEnum] = GenderEnum.undefined,
                            prefix: Optional[str] = typer.Argument(None),
                            suffix: Optional[str] = typer.Argument(None)) -> str:
    async def get_from_fullname():
        typer.secho(f'O nome completo é {fullname.title()}', fg=typer.colors.YELLOW)
        words = fullname.strip().split()
        typer.secho(f'As palavras são {words}', fg=typer.colors.YELLOW)
        result = f'{words[0][0]}{words[-1][0]}'.upper()
        typer.secho(f'O resultado é {result}', fg=typer.colors.YELLOW)
        return result
    async def get_from_birthdate():
        typer.secho(f'A data de nascimento é {birthdate}', fg=typer.colors.CYAN)
        day = f'{birthdate.day}' if birthdate.day > 9 else f'0{birthdate.day}'
        month = f'{birthdate.month}' if birthdate.month > 9 else f'0{birthdate.month}'
        result = f'{birthdate.year}{month}{day}'
        typer.secho(f'O resultado é {result}', fg=typer.colors.CYAN)
        return result
    async def get_from_gender():
        result: str = ''
        if gender:
            if gender.value == 0: result = 'UN'
            elif gender.value == 1: result = 'MA'
            elif gender.value == 2: result = 'FE'
            elif gender.value == 3: result = 'TM'
            elif gender.value == 4: result = 'TF'
        return result
    async def get_from_prefix():
        if prefix:
            return prefix.upper()
        return ''
    async def get_from_suffix():
        if suffix:
            return suffix.upper()
        return ''
    return f'{await get_from_prefix()}{await get_from_birthdate()}{await get_from_fullname()}{await get_from_gender()}{await get_from_suffix()}'


@app.command('for-person')
def for_person(
        fullname:str,
        birthdate: datetime = typer.Argument(..., formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y"]),
        gender: Optional[GenderEnum] = GenderEnum.undefined,
        prefix: Optional[str] = typer.Argument(None),
        suffix: Optional[str] = typer.Argument(None)):
    key = asyncio.run(generate_key_for_person(fullname=fullname, gender=gender, birthdate=birthdate, prefix=prefix, suffix=suffix))
    typer.secho(f'A key final é {key}')
    return key