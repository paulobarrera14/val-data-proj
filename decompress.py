import os
import re
import sys

keys = [
    "queueId",
    "playerTitle",
    "players",
    "x",
    "roundsWon",
    "playerStats",
    "playerLocations",
    "seasonId",
    "score",
    "ultimateEffects",
    "defuseRoundTime",
    "armor",
    "characterId",
    "customGameName",
    "winningTeam",
    "headshots",
    "victim",
    "damage",
    "remaining",
    "defuseLocation",
    "plantSite",
    "ability2Effects",
    "assistants",
    "provisioningFlowId",
    "victimLocation",
    "numPoints",
    "killer",
    "isCompleted",
    "loadoutValue",
    "puuid",
    "gameMode",
    "plantRoundTime",
    "spent",
    "stats",
    "receiver",
    "ability2Casts",
    "matchId",
    "isRanked",
    "bombPlanter",
    "ability1Casts",
    "plantPlayerLocations",
    "bombDefuser",
    "gameVersion",
    "abilityCasts",
    "ability",
    "damageType",
    "isSecondaryFireMode",
    "plantLocation",
    "assists",
    "roundsPlayed",
    "coaches",
    "viewRadians",
    "location",
    "competitiveTier",
    "partyId",
    "playerCard",
    "roundResults",
    "defusePlayerLocations",
    "ability1Effects",
    "finishingDamage",
    "y",
    "mapId",
    "gameName",
    "gameStartMillis",
    "roundResult",
    "economy",
    "teamId",
    "weapon",
    "gameLengthMillis",
    "roundNum",
    "legshots",
    "tagLine",
    "won",
    "kills",
    "grenadeCasts",
    "roundResultCode",
    "grenadeEffects",
    "teams",
    "deaths",
    "bodyshots",
    "playtimeMillis",
    "damageItem",
    "roundCeremony",
    "ultimateCasts",
    "timeSinceGameStartMillis",
    "timeSinceRoundStartMillis",
    "matchInfo",
]
keys.sort()

uuid_define_regex = (
    r'"%[0-9]+-'
    r'[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}"'
)


def decompress(text: str) -> str:
    global keys, uuid_define_regex

    for id, key in enumerate(keys):
        text = text.replace(f'"{id}":', f'"{key}":')

    all_uuids = re.findall(uuid_define_regex, text)
    set_uuids = set(all_uuids)
    for id, uuid in enumerate(set_uuids):
        define_id = uuid[1:-1].split("-")[0]  # %xxx
        uuid = "-".join(uuid[1:-1].split("-")[1:])  # xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        text = text.replace(f'"{define_id}-{uuid}"', f'"{uuid}"')
        text = text.replace(f'"{define_id}"', f'"{uuid}"')
    return text


if __name__ == "__main__":
    file_name = sys.argv[1]
    with open(file_name) as f:
        text = f.read()
    text = decompress(text)
    os.makedirs("decompressed", exist_ok=True)
    file_name = os.path.join("decompressed", os.path.basename(file_name))
    with open(file_name, "w") as f:
        f.write(text)