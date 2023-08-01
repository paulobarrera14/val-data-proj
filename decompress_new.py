import json
import os
import re
import tarfile
import brotli

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

def decompress(data: dict):
    global keys, uuid_define_regex

    # Convert the data to a string
    text = json.dumps(data)

    for id, key in enumerate(keys):
        text = text.replace(f'"{id}":', f'"{key}":')

    all_uuids = re.findall(uuid_define_regex, text)
    set_uuids = set(all_uuids)
    for id, uuid in enumerate(set_uuids):
        define_id = uuid[1:-1].split("-")[0]  # %xxx
        uuid = "-".join(uuid[1:-1].split("-")[1:])  # xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        text = text.replace(f'"{define_id}-{uuid}"', f'"{uuid}"')
        text = text.replace(f'"{define_id}"', f'"{uuid}"')

    return json.loads(text)

# Set the path for the tar file and the output directory
tar_path = r'/sample_data/20230726000001.tar'  # replace with your actual tar file path
output_dir = r'/sample_data'  # replace with your output directory

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

with tarfile.open(tar_path, 'r:') as tar:
    for member in tar.getmembers():
        if member.isfile() and member.name.endswith('.json.br'):
            # Extract the entire file content
            file_content = tar.extractfile(member).read()

            try:
                # Decompress the file content
                decompressed_content = brotli.decompress(file_content)

                # Load the decompressed content as JSON
                data = json.loads(decompressed_content.decode())

                decompressed_data = decompress(data)

                # Write the decompressed data to a new file in the output directory
                with open(os.path.join(output_dir, os.path.basename(member.name[:-3])), 'w') as outfile:
                    json.dump(decompressed_data, outfile)
            except:
                print(f"Failed to decode file: {member.name}")