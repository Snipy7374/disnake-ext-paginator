# disnake-ext-paginator

#### **disnake-ext-paginator** is a Python library to easily create embed paginators.

## Supported Versions

Required dependencies [requirements.txt](https://github.com/Snipy7374/disnake-ext-paginator/blob/main/requirements.txt)
```py
python >=3.8, <= 3.10
disnake >= 2.4.0    #(it's really recommended to use 2.6.0)
```

## Installation

Using git
```
git clone https://github.com/Snipy7374/disnake-ext-paginator
```


## Usage

### Quickstart
```python
from disnake_ext_paginator import Paginator
import disnake
from disnake.ext import commands

bot = commands.Bot(
    command_prefix=commands.when_mentioned,
    intents=disnake.Intents.default()
)

@bot.slash_command()
async def test_command(inter: disnake.ApplicationCommandInteraction) -> None:

    # Create a list of embeds to paginate.
    embeds = [
        disnake.Embed(
            title="First embed"
        ),
        disnake.Embe(
            title="Second embed"
        ),
        disnake.Embed(
            title="Third embed"
        ),
    ]
    await Paginator().start(inter, pages=embeds)

bot.run('TOKEN')
```

### Advanced

##### To use custom buttons, pass in the corresponding argument when you initiate the paginator.

```python
from disnake_ext_paginator import Paginator
import disnake
from disnake.ext import commands

bot = commands.Bot(
    command_prefix=commands.when_mentioned,
    intents=disnake.Intents.default()
)

@bot.slash_command()
async def test_command(inter: disnake.ApplicationCommandInteraction) -> None:

    # Create a list of embeds to paginate.
    embeds = [
        disnake.Embed(
            title="First embed"
        ),
        disnake.Embe(
            title="Second embed"
        ),
        disnake.Embed(
            title="Third embed"
        ),
    ]
    paginator = Paginator(
        timeout=400,
        previous_button=disnake.ui.Button(...),
        next_button=disnake.ui.Button(...),
        trash_button=disnake.ui.Button(...),
        page_counter_separator="-",
        page_counter_style=disnake.ButtonStyle.danger,
        initial_page=1,
        on_timeout_message="Paginator expired",
        interaction_check=False # this will allow all users to interact with the paginator
    )
    await paginator.start(inter, pages=embeds)

bot.run('TOKEN')
```
## Documentation
-----
## `class disnake_ext_paginator.Paginator(...)`
```python
class disnake_ext_paginator.Paginator(
    timeout: Union[int, float] = 60,
    previous_button: disnake.ui.Button = disnake.ui.Button(...),
    next_button: disnake.ui.Button = disnake.ui.Button(...),
    trash_button: disnake.ui.Button = disnake.ui.Button(...),
    page_counter_separator: str = "/",
    page_counter_style: disnake.ButtonStyle = disnake.ButtonStyle.grey,
    initial_page: int = 0,
    on_timeout_message: Optional[str] = None,
    interaction_check: bool = True,
    interaction_check_message = Union[disnake.Embed, str] = disnake.Embed(...),
    ephemeral: bool = False
)
```

**timeout: `int`**
    
- How long the Paginator should timeout in, after the last interaction. (In seconds) (Overrides default of 60)


**previous_button: `disnake.ui.Button`**
    
- Overrides default previous button.


**next_button: `disnake.ui.Button`**
- Overrides default next button.


**trash_button: `disnake.ui.Button`**
- Overrides default trash Button.

**page_counter_separator: `str`**

- The separator between page numbers.

**page_counter_style: `disnake.ButtonStyle`**
- Overrides default page counter style.


**initial_page: `int`**
- Page to start the pagination on.


**on_timeout_message: `Optional[str]`**

- Overrides default `on_timeout` str set as embed footer. 
If `None` no message will appear `on_timeout`.


**interaction_check: `bool`**
- Check whether the users interacting with the paginator are the onwer 
of the command or not. Default set to `True`.


**interaction_check_message: `Union[disnake.Embed, str]`**
- The message to send when an `interaction_check` fails e.g a user
who is not the command owner attempeted to interact with the paginator.
This feature can be disabled setting `interaction_check` to `False`.
-----
## `def disnake_ext_paginator.Paginator.start(...)`
```python
def disnake_ext_paginator.Paginator.start(
    interaction: disnake.ApplicationCommandInteraction,
    pages: list[disnake.Embed]
)
```

**interaction: `disnake.ApplicationCommandInteraction`**

- The slash command interaction.

**pages: `list[disnake.Embed]`**

- A list of `disnake.Embed` objects.
-----
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

-----
## Licenses
[MIT](https://choosealicense.com/licenses/mit/) - ([Snipy7374/disnake-ext-paginator](https://github.com/Snipy7374/disnake-ext-paginator))

[MIT](https://choosealicense.com/licenses/mit/) - ([soosBot-com/Pagination](https://github.com/soosBot-com/Pagination))