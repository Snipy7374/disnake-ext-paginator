# disnake-ext-paginator

#### **disnake-ext-paginator** is a Python library to easily create embed paginators.
---
## Supported Versions

Required dependencies [requirements.txt](https://github.com/Snipy7374/disnake-ext-paginator/blob/main/requirements.txt)
```py
python >=3.8, <= 3.10
disnake >= 2.4.0    #(it's really recommended to use 2.6.0)
```

To install the required dependencies you can run:

- with bash
```
pip install -r requirements.txt
```

- with poetry
```
poetry install
```
---
## Installation

- Using git
```
git clone https://github.com/Snipy7374/disnake-ext-paginator
```

---
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
    timeout: Union[int, float, None] = 60,
    previous_button: Optional[disnake.ui.Button] = None,
    next_button: Optional[disnake.ui.Button] = None,
    trash_button: Optional[disnake.ui.Button] = None,
    page_counter_separator: str = "/",
    page_counter_style: disnake.ButtonStyle = disnake.ButtonStyle.grey,
    initial_page: int = 0,
    on_timeout_message: Optional[str] = None,
    interaction_check: bool = True,
    interaction_check_message = Union[disnake.Embed, str] = disnake.Embed(...),
    ephemeral: bool = False,
    persistent: bool = False
)
```

**timeout: `int`**
    
- How long the Paginator should timeout in, after the last interaction. (In seconds) (Overrides default of 60)

> ## Note
> If you're using a persistent paginator then this must be setted to `None`.


**previous_button: `disnake.ui.Button`**
    
- Overrides default previous button. If not provided or `None` a default button will be used.


**next_button: `disnake.ui.Button`**
- Overrides default next button. If not provided or `None` a default button will be used.


**trash_button: `disnake.ui.Button`**
- Overrides default trash Button. If not provided or `None` a default button will be used.

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

**ephemeral: `bool`**
- Whether the paginator should only be visible to the command invokator or
to anyone else.

**persistent: `bool`**
- Makes the `Paginator` pesistent.

> ## Warning
> The use of persistent paginators is not recommended as the paginator needs to be cahed in memory. (Soon there'll be an update to use `low_level_components` to save memory)

> ## Warning
> You must pay attention while using persistent paginators, if used in a normal with several command invokations the memory could be filled completely causing the Bot to crash. This should be used only for single paginators instances e.g. persistent panels that can't be generated by users with a command invokation.

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

### **raises RuntimeError**:
- If the user is attempting to starts two paginators in the same command function body or if the user is attempting to use the same `Paginator` object to start a paginator twice.


-----
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

-----
# Contacts & Support
[Discord - Snipy#7374](https://www.discordapp.com/users/710570210159099984)

-----
## Licenses
[MIT](https://choosealicense.com/licenses/mit/) - ([Snipy7374/disnake-ext-paginator](https://github.com/Snipy7374/disnake-ext-paginator))

[MIT](https://choosealicense.com/licenses/mit/) - ([soosBot-com/Pagination](https://github.com/soosBot-com/Pagination))