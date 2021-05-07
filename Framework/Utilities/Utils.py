import yaml
import discord
import asyncio
from discord.ext import commands


# Exception Handling
class YAMLError(Exception):
    def __init__(self, error):
        self.error = error


class YAML:

    @staticmethod
    def PATH(ContainerPath: str):
        try:
            with open(f"Framework/Database/{ContainerPath}.yaml", "r") as f:
                container_ = yaml.safe_load(f)
            return container_
        except Exception as e:
            raise YAMLError(e)


    @staticmethod
    def GET(ContainerPath: str, *Load: str):
        try:
            dict_ = YAML.PATH(ContainerPath)
            new_dict = dict_
            for load in Load:
                new_dict = new_dict[load]

            return new_dict
        except Exception as e:
            raise YAMLError(e)

    @staticmethod
    def TOKEN():
        return YAML.GET("Client", "Token")


class Colour:

    Error = discord.Colour(0x8a2967)

    Orange = discord.Colour(0xff7043)

    Green = discord.Colour(0xa4f1a6)

    Musik = discord.Colour(0x94e9d6)


class Messaging:

    @staticmethod
    async def Universal_send(context: [commands.Context, discord.Message], obj: [discord.Embed, discord.File, str],
                             seconds: float = 8):

        # Embed Check
        if isinstance(obj, discord.Embed):

            if isinstance(context, commands.Context):

                try:
                    await context.message.delete()
                except:
                    pass
                try:
                    m = await context.send(embed=obj)
                except:
                    return
                await asyncio.sleep(seconds)
                try:
                    await m.delete()
                except:
                    return

            elif isinstance(context, discord.Message):

                try:
                    await context.delete()
                except:
                    pass
                try:
                    m = await context.channel.send(embed=obj)
                except:
                    return
                await asyncio.sleep(seconds)
                try:
                    await m.delete()
                except:
                    return

            else:
                raise AttributeError("Context ist nicht: [commands.Context, discord.Message]")

        # Nachricht Check
        elif isinstance(obj, str):

            if isinstance(context, commands.Context):

                try:
                    await context.message.delete()
                except:
                    pass
                try:
                    m = await context.send(obj)
                except:
                    return
                await asyncio.sleep(seconds)
                try:
                    await m.delete()
                except:
                    return

            elif isinstance(context, discord.Message):

                try:
                    await context.delete()
                except:
                    pass
                try:
                    m = await context.channel.send(obj)
                except:
                    return
                await asyncio.sleep(seconds)
                try:
                    await m.delete()
                except:
                    return

            else:
                raise AttributeError("Context ist nicht: [commands.Context, discord.Message]")

        # Datei Check
        elif isinstance(obj, discord.File):

            if isinstance(context, commands.Context):

                try:
                    await context.message.delete()
                except:
                    pass
                try:
                    m = await context.send(file=obj)
                except:
                    return
                await asyncio.sleep(seconds)
                try:
                    await m.delete()
                except:
                    return

            elif isinstance(context, discord.Message):

                try:
                    await context.delete()
                except:
                    pass
                try:
                    m = await context.channel.send(file=obj)
                except:
                    return
                await asyncio.sleep(seconds)
                try:
                    await m.delete()
                except:
                    return

            else:
                raise AttributeError("Context ist nicht: [commands.Context, discord.Message]")

        else:
            raise AttributeError("Objekt ist nicht: [discord.Embed, discord.File, str]")

    @staticmethod
    async def Universal_edit(message_obj, obj: [discord.Embed, discord.File, str], seconds: float = 8):

        # Embed Check
        if isinstance(obj, discord.Embed):

            try:
                await message_obj.edit(embed=obj)
            except:
                return
            try:
                await message_obj.clear_reactions()
            except:
                pass
            await asyncio.sleep(seconds)
            try:
                await message_obj.delete()
            except:
                return

        # Datei Check
        elif isinstance(obj, discord.File):

            try:
                await message_obj.edit(file=obj)
            except:
                return
            try:
                await message_obj.clear_reactions()
            except:
                pass
            await asyncio.sleep(seconds)
            try:
                await message_obj.delete()
            except:
                return

        # Nachricht Check
        elif isinstance(obj, str):

            try:
                await message_obj.edit(obj)
            except:
                return
            try:
                await message_obj.clear_reactions()
            except:
                pass
            await asyncio.sleep(seconds)
            try:
                await message_obj.delete()
            except:
                return

        else:

            raise AttributeError(f"Objekt ist nicht: [discord.Embed, discord.File, str] => {type(obj)}")

    @staticmethod
    async def Paginator(self, ctx, content: list, info: str = None):

        contents = content

        info_ = None

        pages = len(contents)

        cur_page = 0
        try:
            await ctx.message.delete()
        except:
            pass

        message = await ctx.send(embed=contents[cur_page])

        await message.add_reaction("⏪")
        await message.add_reaction("◀️")
        await message.add_reaction("⏹️")
        await message.add_reaction("▶️")
        await message.add_reaction("⏩")
        if info is not None:
            await message.add_reaction("ℹ️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["⏪", "◀️", "⏹️", "▶️", "⏩", "ℹ️"]

        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=120, check=check)

                if str(reaction.emoji) == "▶️":
                    if cur_page != pages - 1:
                        cur_page += 1
                        await message.edit(embed=contents[cur_page])
                        await message.remove_reaction(reaction, user)
                    else:
                        pass

                elif str(reaction.emoji) == "◀️" and cur_page > 0:
                    cur_page -= 1
                    await message.edit(embed=contents[cur_page])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "⏹️":
                    try:
                        await message.delete()
                    except:
                        pass
                    try:
                        await info_.delete()
                    except:
                        pass
                    break

                elif str(reaction.emoji) == "⏪":
                    cur_page = 0
                    await message.edit(embed=contents[cur_page])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "⏩":
                    cur_page = pages - 1
                    await message.edit(embed=contents[cur_page])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "ℹ️":
                    if info_ is None:
                        info_ = await ctx.send(info)
                    else:
                        try:
                            await info_.delete()
                        except:
                            pass
                        info_ = None

                    await message.remove_reaction(reaction, user)


                else:
                    await message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                try:
                    await message.delete()
                except:
                    pass
                try:
                    await info_.delete()
                except:
                    pass
                break