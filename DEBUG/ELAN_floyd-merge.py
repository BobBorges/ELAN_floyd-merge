#!/usr/bin/env python3
import contextlib
from datetime import datetime
import functools
import os
from optimize_tier_ids import optimize_ids
from optimize_xml_formatting import optimize_xml
from pydub import AudioSegment
import time
import wave
import welcome
import xml.etree.ElementTree as ET

def get_working_dir():									# This sets the directory containing ELAN projects to merge based on user input
	global working_dir									# ugly but it works
	working_dir = input("Enter the ABSOLUTE PATH of the directory containing the ELAN projects you want to merge : ")


def get_outfile_name():									# This sets the name of the results based on user input
	global outfile										# I do what I want!
	outfile = input("What do you want to call the merged project (no spaces or funny characters pls) : ")

def get_project_dirs():									# This gets the individual project directory names
	global project_dirs_rel
	global project_dirs_abs
	project_dirs_rel = []
	project_dirs_abs = []	
	for x in sorted(os.listdir(working_dir)):
		if os.path.isdir(working_dir+'/'+x): 
			project_dirs_rel.append(x)
			project_dirs_abs.append(working_dir+'/'+x)

def get_wav_durr(wav_file):								# This gets the durration of a .wav file
	global wav_durr
	with contextlib.closing(wave.open(wav_file, 'r')) as f:
		frames = f.getnframes()
		rate = f.getframerate()
		wav_durr = int((frames / float(rate))*1000)

def make_output_dump():									# This makes an output directory
	global dump_loc
	dump_loc = working_dir+'/'+outfile
	os.mkdir(dump_loc)

def join_wav_files():									# This joins the wav files
	global joined_wavs	
	global wavs_to_join
	wavs_to_join = []
	for y in project_dirs_abs:
		for z in os.listdir(y):
			if z.endswith(".wav"):
				wav_to_join = AudioSegment.from_wav(os.path.join(y, z))
				wavs_to_join.append(wav_to_join)	
	joined_wavs = dump_loc+'/'+outfile+'.wav'
	to_join = functools.reduce(lambda x, y: x + y, wavs_to_join)		# Thanks for the lambada, Harald
	to_join.export(joined_wavs, format="wav")

def make_empty_eaf():									# This creates a new eaf file
	new_root = ET.Element("ANNOTATION_DOCUMENT")
	new_root.set('AUTHOR', '')
	new_root.set('DATE', str(datetime.now()))
	new_root.set('FORMAT', '3.0')
	new_root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance') 
	new_root.set('xsi:noNamespaceSchemaLocation', 'http://www.mpi.nl/tools/elan/EAFv3.0.xsd')
	new_root.text = "\n    "
	new_header = ET.SubElement(new_root, 'HEADER')
	new_header.set('MEDIA_FILE', '')
	new_header.set('TIME_UNITS', 'miliseconds')
	new_header.text = "\n        "
	new_header.tail = "\n    "
	new_media_descriptor = ET.SubElement(new_header, 'MEDIA_DESCRIPTOR')
	new_media_descriptor.set('MEDIA_URL', 'file://'+joined_wavs)
	new_media_descriptor.set('MIME_TYPE', 'audio/x-wav')
	new_media_descriptor.set('RELATIVE_MEDIA', '')
	new_media_descriptor.tail = "\n        "
	property_1 = ET.SubElement(new_header, 'PROPERTY')
	property_1.set('NAME', 'URN')
	property_1.text = 'urn:nl-mpi-tools-elan-eaf:2bb01589-bf3d-4141-871d-8f31be10fd9b'
	property_1.tail = "\n        "
	property_2 = ET.SubElement(new_header, 'PROPERTY')
	property_2.set('NAME', 'URN')
	property_2.text = 'urn:nl-mpi-tools-elan-eaf:caa9315e-2d46-4958-af80-606214d37ce7'
	property_2.tail = "\n        "
	property_3 = ET.SubElement(new_header, 'PROPERTY')
	property_3.set('NAME', 'lastUsedAnnotationID')
	property_3.text = "1"
	property_3.tail = "\n    "
	new_time_order = ET.SubElement(new_root, 'TIME_ORDER')
	new_time_order.text = "\n        "
	# TIERS GO HERE #
	new_constraint_1 = ET.SubElement(new_root, 'CONSTRAINT')
	new_constraint_1.set('DESCRIPTION', "Time subdivision of parent annotation's time interval, no time gaps allowed within this interval")
	new_constraint_1.set('STEREOTYPE', 'Time_Subdivision')
	new_constraint_1.tail = "\n    "	
	new_constraint_2 = ET.SubElement(new_root, 'CONSTRAINT')
	new_constraint_2.set('DESCRIPTION', 'Symbolic subdivision of a parent annotation. Annotations refering to the same parent are ordered')
	new_constraint_2.set('STEREOTYPE', 'Symbolic_Subdivision')
	new_constraint_2.tail = "\n    "
	new_constraint_3 = ET.SubElement(new_root, 'CONSTRAINT')
	new_constraint_3.set('DESCRIPTION', '1-1 association with a parent annotation')
	new_constraint_3.set('STEREOTYPE', 'Symbolic_Association')
	new_constraint_3.tail = "\n    "
	new_constraint_4 = ET.SubElement(new_root, 'CONSTRAINT')
	new_constraint_4.set('DESCRIPTION', "Time alignable annotations within the parent annotation's time interval, gaps are allowed")
	new_constraint_4.set('STEREOTYPE', 'Included_In')
	new_constraint_4.tail = "\n"
	globals().update(locals())							# say what you want - I don't care

def parse_elan_xml(eaf_file):							# This parses eaf file and makes elements available in main()
	global eaf_tree
	global eaf_tier
	global eaf_time
	global eaf_time_slots
	global eaf_linguistic_type
	global eaf_alignable_annotation
	TREE = ET.parse(eaf_file)
	eaf_tree = TREE.getroot()	
	eaf_tier = eaf_tree.findall("TIER")
	eaf_time = eaf_tree.findall("TIME_ORDER")	
	eaf_time_slots = eaf_tree.findall("TIME_SLOT")
	eaf_linguistic_type = eaf_tree.findall("LINGUISTIC_TYPE")
	eaf_annotation = eaf_tree.findall("ANNOTATION")

def get_new_eaf_tiers():								# This makes newly created tiers available in main()
	global new_eaf_tiers
	new_eaf_tiers = new_root.findall("TIER")
#
##
###
####
#####
######
#######
########
#########
##########
###############################################################################
##########	|  											|	###################
##########	|	This is the main function of the script	|	###################
##########	|											|	###################
###############################################################################
def main():
	welcome.welcome_msg()												# dep: 0
	get_working_dir()													# dep: 0
	get_outfile_name()													# dep: 0
	start_time = time.time()											# this starts a timer	
	get_project_dirs()													# dep: get_working_dir()
	make_output_dump()													# dep: get_working_dir(), get_outfile_name
	ms_index=0															# sets index for TIME_VALUE in ms
	ts_index=0															# sets index for TIME_SLOT_ID
	join_wav_files()													# dep: make_output_dump()
	make_empty_eaf()													# dep: join_wav_files
	for i, project_dir in enumerate(project_dirs_abs):					# this starts to loop through the project direcories
		wav_path = project_dir+'/'+project_dirs_rel[i]+'.wav'			# defines a path to the waf file in the dir
		eaf_path = project_dir+'/'+project_dirs_rel[i]+'.eaf'			# defines a path to the eaf file in the dir
		get_wav_durr(wav_path)											# dep: get_project_dirs
		print(wav_path+': '+str(wav_durr))				##DEBUG
		print(eaf_path)									##DEBUG
		print("Old ms Index: "+str(ms_index))			##DEBUG
		parse_elan_xml(eaf_path)										# dep: get_working_dir(), get_outfile_name
		for eaf_time_slots in eaf_time:									# This starts to loop through the TIME_ORDER subelements :: vars defined in parse_elan_xml()
			print("Old ts index: "+str(ts_index))		##DEBUG
			for slot in eaf_time_slots:									# This targets each TIME_SLOT element in the TIME_ORDER tier
				ts_ID = slot.get("TIME_SLOT_ID")						# defines a TIME_SLOT_ID var
				time_value = slot.get('TIME_VALUE')						# defines a TIME_VALUE var
				print("Old ts id: "+ts_ID)				##DEBUG
				ts_ID_new = "ts"+str(int(ts_ID[2:])+ts_index)			# increments the TIME_SLOT_ID by the ts_index
				print("New ts id: "+ts_ID_new)			##DEBUG
				new_slot = ET.SubElement(new_time_order, 'TIME_SLOT')	# creates new TIME_SLOT element and appends it to TIME_ORDER in the merged eaf file
				new_slot.set('TIME_SLOT_ID', ts_ID_new)					# sets the TIME_SLOT_ID attr of ^
				new_slot.set('TIME_VALUE', str(int(time_value)+int(ms_index)))	# increments and sets the TIME_VALEU attr of ^
				print(i)								##DEBUG
			if project_dir is project_dirs_abs[0]:						# starts operating on the first elan project
				for tier in eaf_tier:									# iterating down the tiers
					for eaf_annotation in tier:									# iterating
						for eaf_alignable_annotation in eaf_annotation:			# iterating :: "alignable" in the var name is misleading, these are all clild elements of ANNOTATION
							a_id = eaf_alignable_annotation.get("ANNOTATION_ID")		# this gets the uniqe annotation id 
							looped_a_id = a_id+'-'+str(i)								# appends the loop index to the annotation id (necessary for keeping unique ids post merge)
							print(looped_a_id)			##DEBUG
							eaf_alignable_annotation.set("ANNOTATION_ID", looped_a_id)			# this sets the new annotation id in the tier						
							if eaf_alignable_annotation.tag =="REF_ANNOTATION":					# this targets tiers that have a symbolic time association
								r_id = eaf_alignable_annotation.get("ANNOTATION_REF")			# this sets a ref id variable
								looped_r_id = r_id+'-'+str(i)									# appends the loop index to the ref id (necessary for maintaining refs to new annotation ids post merge)
								eaf_alignable_annotation.set("ANNOTATION_REF", looped_r_id)		# this sets the new ref id to the annotation
								print(looped_r_id)		##DEBUG
					new_root.insert(-4, tier)							# this inserts the modified tiers and children of the initial document to the appropriate place in the merged file
				for lingtype in eaf_linguistic_type:					# this gets the linguistic_type teirs from the firsd doc (vars set in parse_elan_xml())
					new_root.insert(-4, lingtype)						# and this appends ^ to the correct place in the merged file
			else:														# this begins operations on the subsequent eaf files
				get_new_eaf_tiers()										# this makes newely added tiers (in the if loop ^) available here
				for tier_idx, tier in enumerate(eaf_tier):				# looping through tiers with indexes
					for eaf_annotation in tier:							# looping through annotations
						for eaf_alignable_annotation in eaf_annotation:		# iterating :: "alignable" in the var name is misleading, these are all clild elements of ANNOTATION
							a_id = eaf_alignable_annotation.get("ANNOTATION_ID")			# this gets the uniqe annotation id 
							looped_a_id = a_id+'-'+str(i)									# this appends the loop index to the id (necessary for keeping unique ids post merge)
							eaf_alignable_annotation.set("ANNOTATION_ID", looped_a_id)		# this sets the new annotation id in the annotation
							if eaf_alignable_annotation.tag =="REF_ANNOTATION":				# this targets tiers that have a symbolic time association
								r_id = eaf_alignable_annotation.get("ANNOTATION_REF")		# this sets the ref id variable
								looped_r_id = r_id+'-'+str(i)								# this appends the loop index to the ref id variable
								eaf_alignable_annotation.set("ANNOTATION_REF", looped_r_id)	# this sets the new ref id to the annotation
								print(looped_r_id)		##DEBUG
							if eaf_alignable_annotation.tag == "ALIGNABLE_ANNOTATION":				# this targets alignable annotations (default in elan
								alignable_time_1 = eaf_alignable_annotation.get("TIME_SLOT_REF1") 	# this gets the first time slot reference	
								alignable_time_2 = eaf_alignable_annotation.get("TIME_SLOT_REF2")	# this gets the second time slot reference
								print(alignable_time_1)	##DEBUG
								print(alignable_time_2)	##DEBUG
								new_alignable_time_1 = "ts"+str(int(alignable_time_1[2:])+int(ts_index)) 	# this increments the first time slot vatiable
								new_alignable_time_2 = "ts"+str(int(alignable_time_2[2:])+ts_index)			# this increments the second time slot vatiable
								eaf_alignable_annotation.set("TIME_SLOT_REF1", new_alignable_time_1)		# this resets the first time slot vatiable
								eaf_alignable_annotation.set("TIME_SLOT_REF2", new_alignable_time_2)		# this resets the second time slot vatiable
						new_eaf_tiers[tier_idx].append(eaf_annotation) 						# this appends the altered annotation to the appropriate tier in the new eaf doc
			ts_index = ts_index + len(eaf_time_slots)										# this increments the time slot index
			print("New ts index: "+str(ts_index))		##DEBUG
		ms_index = ms_index+wav_durr														# this increments the milisecond index
		print("New ms Index: "+str(ms_index))			##DEBUG
	new_eaf = ET.ElementTree(new_root)										# this makes a new element tree from the newly created eaf
	new_eaf_file = dump_loc+'/'+outfile+'.eaf' 								# this sets a location for the new eaf to be written
	new_eaf.write(new_eaf_file, encoding="UTF-8", xml_declaration=True)		# this writes the new eaf to the specified location
	optimize_ids(new_eaf_file)												# this resets the annotation ids and the reference tier ids to a format elan likes.
	optimize_xml(new_eaf_file)
	print("~~~~ Your Elan projects were merged in %s seconds.~~~~ " % (time.time()-start_time))		# this tells you how long it all took

if __name__ == '__main__':
	main()
