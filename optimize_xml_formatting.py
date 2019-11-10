#!/usr/bin/env python3

import xml.etree.ElementTree as ET

def optimize_xml(eaf_file):
	TREE = ET.parse(eaf_file)
	tree = TREE.getroot()
	time_order = tree.find("TIME_ORDER")
	nr_of_slots = len(time_order)
	for slot_idx, slot in enumerate(time_order, start=1):
		if slot_idx != nr_of_slots:
			slot.tail = "\n        "
		else:
			slot.tail = "\n    "
	time_order.tail = "\n    "
	tiers = tree.findall("TIER")
	for tier_idx, tier in enumerate(tiers, start=1):
		tier.tail = "\n    "
		tier.text = "\n        "
		for annotation_idx, annotation in enumerate(tier, start=1):
			nr_of_annotations = len(tier)
			if annotation_idx != nr_of_annotations:
				annotation.tail = "\n        "
			else:
				annotation.tail = "\n    "
	tree = ET.ElementTree(tree)
	tree.write(eaf_file, encoding="UTF-8", xml_declaration=True)
		

