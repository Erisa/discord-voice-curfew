# https://discord.com/developers/applications
token = 'TOKEN_GOES_HERE'

# Maps a time to a message to be to send in the text channel
warnings = {
    "22:45": "15 minute warning message here",
    "22:50": "10 minute warning message here",
    "22:55": "5 minute warning message here"
}

# The times to lock the channel and unlock the channel
lock_time_str = "23:00"
unlock_time_str = "06:0"

# The messages to send when locking or unlocking
# These are optional, you can leave them as "" to not send any message when this happens.
lock_message = ""
unlock_message = ""

# The person who is allowed to use !lock and !unlock
owner = 228574821590499329

# The ID of the voice channel to lock/unlock
voicechannel_id = 876726997554966598

# The ID of the text channel to send messages in
textchannel_id = 742840934714179627
