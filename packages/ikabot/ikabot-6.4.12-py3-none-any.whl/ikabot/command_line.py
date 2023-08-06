#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import gettext
import multiprocessing
from ikabot.config import *
from ikabot.web.session import *
from ikabot.helpers.gui import *
from ikabot.function.donate import donate
from ikabot.function.update import update
from ikabot.helpers.pedirInfo import read
from ikabot.function.getStatus import getStatus
from ikabot.function.donationBot import donationBot
from ikabot.helpers.botComm import updateTelegramData, telegramDataIsValid
from ikabot.helpers.process import updateProcessList
from ikabot.function.constructionList import constructionList
from ikabot.function.searchForIslandSpaces import searchForIslandSpaces
from ikabot.function.alertAttacks import alertAttacks
from ikabot.function.vacationMode import vacationMode
from ikabot.function.activateMiracle import activateMiracle
from ikabot.function.trainArmy import trainArmy
from ikabot.function.sellResources import sellResources
from ikabot.function.checkForUpdate import checkForUpdate
from ikabot.function.distributeResources import distributeResources
from ikabot.function.alertLowWine import alertLowWine
from ikabot.function.buyResources import buyResources
from ikabot.function.loginDaily import loginDaily
from ikabot.function.sendResources import sendResources
from ikabot.function.constructBuilding import constructBuilding
from ikabot.function.shipMovements import shipMovements
from ikabot.function.importExportCookie import importExportCookie
from ikabot.function.autoPirate import autoPirate
from ikabot.function.investigate import investigate
from ikabot.function.attackBarbarians import attackBarbarians
from ikabot.function.proxyConf import proxyConf, show_proxy

t = gettext.translation('command_line',
                        localedir,
                        languages=languages,
                        fallback=True)
_ = t.gettext

def menu(session, checkUpdate=True):
	"""
	Parameters
	----------
	session : ikabot.web.session.Session
	checkUpdate : bool
	"""
	if checkUpdate:
		checkForUpdate()

	show_proxy(session)

	banner()

	process_list = updateProcessList(session)
	if len(process_list) > 0:
		print(_('Running tasks:'))
		for process in process_list:
			print(_('- pid: {} task: {}').format(process['pid'], process['action']))
		print('')

	menu_actions = [
					constructionList,
					sendResources,
					distributeResources,
					getStatus,
					donate,
					searchForIslandSpaces,
					loginDaily,
					alertAttacks,
					donationBot,
					alertLowWine,
					buyResources,
					sellResources,
					vacationMode,
					activateMiracle,
					trainArmy,
					shipMovements,
					constructBuilding,
					update,
					importExportCookie,
					autoPirate,
					investigate,
					attackBarbarians,
					proxyConf,
					updateTelegramData
					]

	print(_('(0)  Exit'))
	print(_('(1)  Construction list'))
	print(_('(2)  Send resources'))
	print(_('(3)  Distribute resources'))
	print(_('(4)  Account status'))
	print(_('(5)  Donate'))
	print(_('(6)  Search for new spaces'))
	print(_('(7)  Login daily'))
	print(_('(8)  Alert attacks'))
	print(_('(9)  Donate automatically'))
	print(_('(10) Alert wine running out'))
	print(_('(11) Buy resources'))
	print(_('(12) Sell resources'))
	print(_('(13) Activate vacation mode'))
	print(_('(14) Activate miracle'))
	print(_('(15) Train army'))
	print(_('(16) See movements'))
	print(_('(17) Construct building'))
	print(_('(18) Update Ikabot'))
	print(_('(19) Import / Export cookie'))
	print(_('(20) Auto-Pirate'))
	print(_('(21) Investigate'))
	print(_('(22) Attack barbarians'))
	print(_('(23) Configure Proxy'))
	if telegramDataIsValid(session):
		print(_('(24) Change the Telegram data'))
	else:
		print(_('(24) Enter the Telegram data'))

	total_options = len(menu_actions)
	selected = read(min=0, max=total_options)
	if selected != 0:
		try:
			selected -= 1
			event = multiprocessing.Event() #creates a new event
			process = multiprocessing.Process(target=menu_actions[selected], args=(session, event, sys.stdin.fileno()), name=menu_actions[selected].__name__)
			process.start()
			process_list.append({'pid': process.pid, 'action': menu_actions[selected].__name__ })
			updateProcessList(session, programprocesslist=process_list)
			event.wait() #waits for the process to fire the event that's been given to it. When it does  this process gets back control of the command line and asks user for more input
		except KeyboardInterrupt:
			pass
		menu(session, checkUpdate=False)
	else:
		if isWindows:
			# in unix, you can exit ikabot and close the terminal and the processes will continue to execute
			# in windows, you can exit ikabot but if you close the terminal, the processes will die
			print(_('Closing this console will kill the processes.'))
			enter()
		clear()
		os._exit(0) #kills the process which executes this statement, but it does not kill it's child processes

def init():
	home = 'USERPROFILE' if isWindows else 'HOME'
	os.chdir(os.getenv(home))
	if not os.path.isfile(ikaFile):
		open(ikaFile, 'w')
		os.chmod(ikaFile, 0o600)

def start():
	init()
	session = Session()
	try:
		menu(session)
	finally:
		clear()
		session.logout()

def main():
	try:
		start()
	except KeyboardInterrupt:
		clear()

if __name__ == '__main__':
	if sys.platform.startswith('win'):
	# On Windows calling this function is necessary.
		multiprocessing.freeze_support()
	main()
