from __future__ import annotations

import os
import logging
import inspect

import disnake


__all__ = ("Paginator",)


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
    page_counter_separator: str
        The custom separator between the pages numbers
        in the page_counter button.
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
    ephemeral: bool
        Whether the paginator should only be visible to the command invokator or
        to anyone else.
    """

    __running_interaction_ids: list[int] = []

    __slots__ = (
        "timeout",
        "previous_button",
        "next_button",
        "trash_button",
        "page_counter_separator",
        "page_counter_style",
        "initial_page",
        "on_timeout_message",
        "interaction_check_message",
        "ephemeral",
        "_interaction_check",
        "pages",
        "total_page_count",
        "interaction",
        "bot",
        "current_page",
        "original_message_deleted",
        "page_counter",
        "persistent",
    )

    def __init__(
        self,
        *,
        timeout: int | float | None = 60,
        previous_button: disnake.ui.Button | None = None,
        next_button: disnake.ui.Button | None = None,
        trash_button: disnake.ui.Button | None = None,
        page_counter_separator: str = "/",
        page_counter_style: disnake.ButtonStyle = disnake.ButtonStyle.grey,
        initial_page: int = 0,
        on_timeout_message: str | None = None,
        interaction_check: bool = True,
        interaction_check_message: disnake.Embed | str = disnake.Embed(
            description="You cannot control this pagination because you did not execute it.",
            color=disnake.Color.red(),
        ),
        ephemeral: bool = False,
        persistent: bool = False,
    ) -> None:

        # TODO:
        # implement custom_id generation to use low_level_components instead of
        # permanent views
        #  button.custom_id = "<button_name>:<user_id>:<interaction_id>" could be a valid
        # custom_id format

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
        self.persistent = persistent

        self.logger = logging.getLogger("disnake")
        self.logger.setLevel(logging.WARNING)
        self.handler = logging.StreamHandler()
        self.logger.addHandler(self.handler)

        if self.persistent and timeout:
            raise ValueError(f"To create a persistent Paginator the timeout must be None, not {timeout.__class__!r}")

        super().__init__(timeout=timeout)

    async def start(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        pages: list[disnake.Embed],
    ) -> None:
        """
        Starts the Paginator object.

        Parameters:
        ----------
        interaction: disnake.ApplicationCommandInteraction
            The command interaction.
        pages: List[disnake.Embed]
            A list of embeds wich compose the Paginator contents to send.

        Raises:
        ----------
        RuntimeError:
            If the user is attempting to starts two paginators in the same command function body
            or if the user is attempting to use the same Paginator object to start a paginator twice.

        """
        if self.previous_button is None:
            self.previous_button = disnake.ui.Button(
                emoji=disnake.PartialEmoji(name="\U000025c0"),
                custom_id=f"PREV_BTN:{interaction.id}:{interaction.author.id}",
            )
        if self.next_button is None:
            self.next_button = disnake.ui.Button(
                emoji=disnake.PartialEmoji(name="\U000025b6"),
                custom_id=f"NEXT_BTN:{interaction.id}:{interaction.author.id}",
            )
        if self.trash_button is None:
            self.trash_button = disnake.ui.Button(
                emoji=disnake.PartialEmoji(name="\U0001f5d1"),
                style=disnake.ButtonStyle.danger,
                custom_id=f"TRASH_BTN:{interaction.id}:{interaction.author.id}",
            )
        # Checks if a user is trying to use a Paginator instance
        # in the same command function and raise a RuntimeError
        # this is needed because in the same command the interaction
        # is the same so the Paginator can't work correctly with two instances.
        # Note: This error is not raised on __init__ method so you can create two Paginator instances
        # but you can't start the Paginator with the start method.
        # Note: this error is raised when trying to call the started method
        # twice or more on the same Paginator object
        # or when you're trying to start different Paginator object on the same command
        self._current_instance_location = (
            f"{interaction.application_command.cog_name or os.path.abspath(inspect.getfile(interaction.application_command.callback))}"
            f":{interaction.application_command.name}"
        )
        if interaction.id in Paginator.__running_interaction_ids:
            raise RuntimeError(
                f"You can have only one Paginator instance per command! Check your '{self._current_instance_location}' command."
            )

        Paginator.__running_interaction_ids.append(interaction.id)
        self.pages = pages
        self.total_page_count = len(pages)
        self.interaction = interaction
        self.bot = interaction.bot
        self.current_page = self.initial_page
        self.original_message_deleted = False
        self.next_button.disabled = self.previous_button.disabled = self.trash_button.disabled = False

        self.previous_button.callback = self.__previous_button_callback
        self.next_button.callback = self.__next_button_callback
        self.trash_button.callback = self.__trash_button_callback

        self.page_counter: disnake.ui.Button = disnake.ui.Button(
            label=f"{self.initial_page + 1} {self.page_counter_separator} {self.total_page_count}",
            style=self.page_counter_style,
            disabled=True,
        )

        if self.persistent and not all((self.previous_button.custom_id, self.next_button.custom_id, self.trash_button.custom_id)):
            raise ValueError("You need to set the custom ID of buttons to make the Paginator persistent.")

        self.add_item(self.previous_button)
        self.add_item(self.page_counter)
        self.add_item(self.next_button)
        self.add_item(self.trash_button)

        await interaction.send(
            embed=self.pages[self.initial_page], view=self, ephemeral=self.ephemeral
        )

    async def on_timeout(self) -> None:
        if not self.original_message_deleted:
            self.previous_button.disabled = self.next_button.disabled = self.trash_button.disabled = True # type: ignore
            embed = self.pages[self.current_page]
            if self.on_timeout_message:
                embed.set_footer(text=self.on_timeout_message)
            await self.interaction.edit_original_message(embed=embed, view=self)
        
        Paginator.__running_interaction_ids.remove(self.interaction.id)

    async def interaction_check(self, interaction: disnake.MessageInteraction) -> bool:
        if isinstance(self._interaction_check, bool) and self._interaction_check:
            if interaction.author.id != self.interaction.author.id:
                if isinstance(self.interaction_check_message, disnake.Embed):
                    await interaction.response.send_message(
                        embed=self.interaction_check_message, ephemeral=True
                    )
                elif isinstance(self.interaction_check_message, str):
                    await interaction.response.send_message(
                        self.interaction_check_message, ephemeral=True
                    )
                return False
            return True
        else:
            return False

    async def __previous(self, interaction: disnake.MessageInteraction) -> None:
        if self.current_page == 0:
            self.current_page = self.total_page_count - 1
        else:
            self.current_page -= 1

        self.page_counter.label = f"{self.current_page + 1} {self.page_counter_separator} {self.total_page_count}"
        await interaction.response.edit_message(
            embed=self.pages[self.current_page], view=self
        )

    async def __next(self, interaction: disnake.MessageInteraction) -> None:
        if self.current_page == self.total_page_count - 1:
            self.current_page = 0
        else:
            self.current_page += 1

        self.page_counter.label = f"{self.current_page + 1} {self.page_counter_separator} {self.total_page_count}"
        await interaction.response.edit_message(
            embed=self.pages[self.current_page], view=self
        )
    async def __next_button_callback(
        self, interaction: disnake.MessageInteraction
    ) -> None:
        await self.__next(interaction)

    async def __previous_button_callback(
        self, interaction: disnake.MessageInteraction
    ) -> None:
        await self.__previous(interaction)

    async def __trash_button_callback(
        self, interaction: disnake.MessageInteraction
    ) -> None:
        self.original_message_deleted = True
        await interaction.response.defer()
        await interaction.delete_original_message()
