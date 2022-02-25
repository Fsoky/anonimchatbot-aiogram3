from environs import Env

env = Env()
env.read_env()

TOKEN = env.str("TOKEN")
MONGODB_LINK = env.str("MONGODB_LINK")
