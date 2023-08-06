import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import time

import utils.constants
import wynncraft


def run_cache(id, function, *args):
    if CacheManager.call_request(id):
        exec(f"x = {function}{args}", globals(), globals())
        res = x
    else:
        res = None

    return CacheManager.search_cache(id, res)


class CacheManager:
    try:
        os.chdir(os.path.abspath(os.getcwd()) + "/.cache")
    except FileNotFoundError:
        os.mkdir(os.path.abspath(os.getcwd()) + "/.cache")
        os.chdir(os.path.abspath(os.getcwd()) + "/.cache")

    def read_cache():
        try:
            open(".cache.json")
        except FileNotFoundError:
            open(".cache.json", "w")
            return json.loads("{}")
        else:
            with open(".cache.json", "r") as c:
                try:
                    return json.loads(c.read())
                except json.decoder.JSONDecodeError:
                    return json.loads("{}")


    def write_cache(data):
        cache = {}
        try:
            cache = json.loads(open(".cache.json").read())
        except (FileNotFoundError,json.decoder.JSONDecodeError):
            cache = {}
        finally:
            with open(".cache.json", "w") as c:
                cache.update(data)
                json.dump(cache, c)

    def read_cache_table():
        try:
            open(".cache-table.json")
        except FileNotFoundError:
            open(".cache-table.json", "w")
            return json.loads("{}")
        else:
            with open(".cache-table.json", "r") as c:
                try:
                    return json.loads(c.read())
                except json.decoder.JSONDecodeError:
                    return json.loads("{}")

    def write_cache_table(data):
        cache = {}
        try:
            cache = json.loads(open(".cache-table.json").read())
        except (FileNotFoundError,json.decoder.JSONDecodeError):
            cache = {}
        finally:
            with open(".cache-table.json", "w") as c:
                cache.update(data)
                json.dump(cache, c)

    def delete_cache():
        for f in [".cache.json", ".cache-table.json"]:
            try:
                os.remove(f)
            except FileNotFoundError:
                continue

    def search_cache(id, res):
        if res:
            CacheManager.write_cache({id: res})
            CacheManager.write_cache_table({id: int(time.time()) + utils.constants.CACHE_TIME})
            return res
        else:
            return CacheManager.read_cache()[id]
    
    def call_request(id):
        cache_table = CacheManager.read_cache_table()
        return ((not cache_table) or (id not in cache_table) or (cache_table[id] < int(time.time())))

    
class Guild:
    def list():
        return run_cache("guild_list", "wynncraft.Guild.list")

    def stats(name):
        return run_cache("guild_stats", "wynncraft.Guild.stats", name)


class Ingredient:
    def get(name):
        return run_cache(f"ingredient_get_{name}", "wynncraft.Ingredient.get", name)

    def list():
        return run_cache(f"ingredient_list", "wynncraft.Ingredient.list")

    def search(query, arg):
        return run_cache(f"ingredient_search_{query}_{arg}", "wynncraft.Ingredient.search", query, arg)

    def search_name(arg):
        return Ingredient.search("name", arg)
    
    def search_tier(arg):
        return Ingredient.search("tier", arg)

    def search_level(arg):
        return Ingredient.search("level", arg)

    def search_skills(arg):
        return Ingredient.search("skills", arg)

    def search_sprite(arg):
        return Ingredient.search("sprite", arg)
    
    def search_identifications(arg):
        return Ingredient.search("identifications", arg)

    def search_item_only_ids(arg):
        return Ingredient.search("itemOnlyIDs", arg)

    def search_consumable_only_ids(arg):
        return Ingredient.search("consumableOnlyIDs", arg)


class Item:
    def database_category(category):
        return run_cache(f"item_db_category_{category}", "wynncraft.Item.database_category", category)

    def database_search(name):
        return run_cache(f"item_db_search_{name}", "wynncraft.Item.database_search", name)


class Leaderboard:
    def guild(timeframe):
        return run_cache(f"leaderboard_guild_{timeframe}", "wynncraft.Leaderboard.guild", timeframe)

    def player(timeframe):
        return run_cache(f"leaderboard_player_{timeframe}", "wynncraft.Leaderboard.player", timeframe)

    def pvp(timeframe):
        return run_cache(f"leaderboard_pvp_{timeframe}", "wynncraft.Leaderboard.pvp", timeframe)


class Network:
    def server_list():
        return run_cache("server_list", "wynncraft.Network.server_list")

    def player_sum():
        return run_cache("player_sum", "wynncraft.Network.player_sum")


class Player:
    def stats(player):
        return run_cache("player_stats", "wynncraft.Player.stats", player)

    def uuid(username):
        return run_cache("player_uuid", "wynncraft.Player.uuid", username)


class Recipe:
    def get(name):
        return run_cache(f"recipe_get_{name}", "wynncraft.Recipe.get", name)

    def list():
        return run_cache("recipe_list", "wynncraft.Recipe.list")

    def search(query, arg):
        return run_cache(f"recipe_search_{query}_{arg}", "wynncraft.Recipe.search", query, arg)

    def search_type(arg):
        return Recipe.search("type", arg)
    
    def search_skill(arg):
        return Recipe.search("skill", arg)

    def search_level(arg):
        return Recipe.search("level", arg)
    
    def search_durability(arg):
        return Recipe.search("durability", arg)

    def search_healthOrDamage(arg):
        return Recipe.search("healthOrDamage", arg)

    def search_duration(arg):
        return Recipe.search("duration", arg)

    def search_basicDuration(arg):
        return Recipe.search("basicDuration", arg)


class Search:
    def name(name):
        return run_cache(f"search_{name}", "wynncraft.Search.name", name)


class Territory:
    def list():
        return run_cache("territory_list", "wynncraft.Territory.list")
