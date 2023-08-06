'''
Functionality to start words in Plover.
'''

from typing import List
from plover.translation import Translation
from plover.formatting import _Context, _Action

DELIM_ARGS = " | "
ATTACH = "{^}"

prefixes = (
	"“", "-", "¿", "¡", "(", "'", "/", "@", "\"",
	"ante", "anti", "auto", "bi", "des", "dis", "eco", "equi", "extra",
	"hidro", "in", "inter", "macro", "micro", "multi",
	"pre", "pro", "psico", "re",
	"socio", "sub", "super", "tecno", "tiflo",
	"1", "2", "3", "4", "5", "6", "7", "8", "9", "0"
)

cancelPrefixKey = "#"

def initial(context: _Context, args: str) -> _Action:
	'''
	Meta to start a word in Plover.

	:param context: The context of actions in Plover.
	:param args: Arguments provided to the meta as a |-delimited string.
				Piece 1: The string used when prev_attach is False.
				Piece 2: The string used when prev_attach is True.

	:return: The next action for Plover to perform.
	'''

	# Process input
	output = ''
	translations: List[Translation] = context.previous_translations[-1:]
	for translation in translations:
		actions: List[_Action] = reversed(translation.formatting)
		for action in actions:
			try:
				output = output + action.text
			except:
				output = ''

	# Create the new action
	action: _Action = context.new_action()

	if output == '':
		action.text = args.split(DELIM_ARGS)[0].replace(ATTACH, '')
		if args.split(DELIM_ARGS)[0].endswith(ATTACH):
			action.next_attach = True
		return action

	translation = translations[-1]
	stroke = translation.strokes[0]
	if cancelPrefixKey in stroke.steno_keys and not output.isdigit():
		action.text = args.split(DELIM_ARGS)[-1].replace(ATTACH, '')
		if args.split(DELIM_ARGS)[-1].endswith(ATTACH):
			action.next_attach = True
		return action
	for prefix in prefixes:
		if output == prefix:
			action.text = args.split(DELIM_ARGS)[0].replace(ATTACH, '')
			if args.split(DELIM_ARGS)[0].endswith(ATTACH):
				action.next_attach = True
			return action
	if action.prev_attach and action.next_case is None:
		action.text = args.split(DELIM_ARGS)[-1].replace(ATTACH, '')
		if args.split(DELIM_ARGS)[-1].endswith(ATTACH):
			action.next_attach = True
	else:
		action.text = args.split(DELIM_ARGS)[0].replace(ATTACH, '')
		if args.split(DELIM_ARGS)[0].endswith(ATTACH):
			action.next_attach = True
	return action
