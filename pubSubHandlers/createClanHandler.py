from common.redis import generalPubSubHandler
from common.ripple import userUtils
from common.log import logUtils as log
from common.constants import actions
from helpers import chatHelper as chat
from objects import glob

class handler(generalPubSubHandler.generalPubSubHandler):
	def __init__(self):
		super().__init__()
		self.structure = {
			"clanId": 0
		}

	def handle(self, data):
		try:
			data = super().parseData(data)
			if data is None:
				return
		except:
			return
		clanId = data["clanId"]
		glob.db.fetch("INSERT INTO `bancho_channels` (`id`, `name`, `description`, `public_read`, `public_write`, `status`) VALUES (NULL, '#clan_%s', 'Clan channel', '0', '1', '1')",[clanId])
		glob.channels.addHiddenChannel("#clan_{}".format(clanId))
		users = glob.db.fetchAll("SELECT userid FROM `clan_users` WHERE clanid = %s",[clanId])
		for user in users:
			targetToken = glob.tokens.getTokenFromUserID(user["userid"])
			if targetToken is not None:
				chat.joinChannel(token=targetToken, channel="#clan_{}".format(clanId))