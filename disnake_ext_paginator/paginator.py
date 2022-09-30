from __future__ import annotations
import disnake


class Paginator(disnake.ui.View):
    """
    Embed Paginator.

    Parameters:
    ----------
    timeout: int
        How long the Paginator should timeout in, after the last interaction. (In seconds) (Overrides default of 60)
    previous_button: disnake.ui.Button
        Overrides default previous button.
    next_button: disnake.ui.Button
        Overrides default next button.
    trash_button: disnake.ui.Button.
        Overrides default trash Button.
    page_counter_style: disnake.ButtonStyle
        Overrides default page counter style.
    initial_page: int
        Page to start the pagination on.
    on_timeout_message: Optional[str]
        Overrides default `on_timeout` str set as embed footer.
        If `None` no message will appear `on_timeout`.
    interaction_check: bool
        Check whether the users interacting with the paginator are the onwer 
        of the command or not. Default set to `True`.
    interaction_check_message: Union[disnake.Embed, str]
        The message to send when an `interaction_check` fails e.g a user
        who is not the command owner attempeted to interact with the paginator.
        This feature can be disabled setting `interaction_check` to `False`.
    """

    def __init__(
        self,
        *,
        timeout: int | float = 60,
        previous_button: disnake.ui.Button["Paginator"] = disnake.ui.Button(
            emoji=disnake.PartialEmoji(name="\U000025c0")
            ),
        next_button: disnake.ui.Button["Paginator"] = disnake.ui.Button(
            emoji=disnake.PartialEmoji(name="\U000025b6")
            ),
        trash_button: disnake.ui.Button["Paginator"] = disnake.ui.Button(
            emoji=disnake.PartialEmoji(name="\U0001f5d1"),
            style=disnake.ButtonStyle.danger,
        ),
        page_counter_separator: str = "/",
        page_counter_style: disnake.ButtonStyle = disnake.ButtonStyle.grey,
        initial_page: int = 0,
        on_timeout_message: str | None  = None,
        interaction_check: bool = True,
        interaction_check_message: disnake.Embed | str = disnake.Embed(
            description="You cannot control this pagination because you did not execute it.",
            color=disnake.Color.red()
        ),
        ephemeral: bool = False
    ) -> None:

        self.previous_button = previous_button
        self.next_button = next_button
        self.trash_button = trash_button
        self.page_counter_separator = page_counter_separator
        self.page_counter_style = page_counter_style
        self.initial_page = initial_page

        self.ephemeral = ephemeral
        self.original_message_deleted: bool = False
        self.on_timeout_message = on_timeout_message
        self._interaction_check = interaction_check
        self.interaction_check_message = interaction_check_message

        super().__init__(timeout=timeout)


    async def start(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        pages: list[disnake.Embed]
    ) -> None:

        self.pages = pages
        self.total_page_count = len(pages)
        self.interaction = interaction
        self.bot = interaction.bot
        self.current_page = self.initial_page
        self.original_message_deleted = False

        self.next_button.disabled, self.previous_button.disabled, self.trash_button.disabled = False, False, False

        self.previous_button.callback = self.__previous_button_callback
        self.next_button.callback = self.__next_button_callback
        self.trash_button.callback = self.__trash_button_callback

        self.page_counter: disnake.ui.Button["Paginator"] = disnake.ui.Button(
            label=f"{self.initial_page + 1} {self.page_counter_separator} {self.total_page_count}",
            style=self.page_counter_style,
            disabled=True
        )

        self.add_item(self.previous_button)
        self.add_item(self.page_counter)
        self.add_item(self.next_button)
        self.add_item(self.trash_button)

        await interaction.send(embed=self.pages[self.initial_page], view=self, ephemeral=self.ephemeral)
    
    async def on_timeout(self) -> None:
        if not self.original_message_deleted:
            self.previous_button.disabled, self.next_button.disabled, self.trash_button.disabled = True, True, True
            embed = self.pages[self.current_page]
            if self.on_timeout_message:
                embed.set_footer(
                    text=self.on_timeout_message
                )
            await self.interaction.edit_original_message(embed=embed, view=self)
    
    async def interaction_check(self, interaction: disnake.MessageInteraction) -> bool:
        if isinstance(self._interaction_check, bool) and self._interaction_check:
            if interaction.author.id != self.interaction.author.id:
                if isinstance(self.interaction_check_message, disnake.Embed):
                    await interaction.response.send_message(embed=self.interaction_check_message, ephemeral=True)
                elif isinstance(self.interaction_check_message, str):
                    await interaction.response.send_message(self.interaction_check_message, ephemeral=True)
                return False
            return True
        else:
            return False

    async def __previous(self) -> None:
        if self.current_page == 0:
            self.current_page = self.total_page_count - 1
        else:
            self.current_page -= 1

        self.page_counter.label = f"{self.current_page + 1} {self.page_counter_separator} {self.total_page_count}"
        await self.interaction.edit_original_message(embed=self.pages[self.current_page], view=self)

    async def __next(self) -> None:
        if self.current_page == self.total_page_count - 1:
            self.current_page = 0
        else:
            self.current_page += 1

        self.page_counter.label = f"{self.current_page + 1} {self.page_counter_separator} {self.total_page_count}"
        await self.interaction.edit_original_message(embed=self.pages[self.current_page], view=self)

    async def __next_button_callback(self, interaction: disnake.MessageInteraction) -> None:
        await self.__next()
        await interaction.response.defer()

    async def __previous_button_callback(self, interaction: disnake.MessageInteraction) -> None:
        await self.__previous()
        await interaction.response.defer()
    
    async def __trash_button_callback(self, interaction: disnake.MessageInteraction) -> None:
        self.original_message_deleted = True
        await self.interaction.delete_original_message()
