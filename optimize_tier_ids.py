#!/usr/bin/env python3

import xml.etree.ElementTree as ET

def optimize_ids(eaf_file):						# This is supposed to reset the annotation ids and references, but it doesn't work yet
	TREE = ET.parse(eaf_file)
	tree = TREE.getroot()
	tiers = tree.findall("TIER")
	ann_idx_step=0
	opt_key = {}
	for tier in tiers:
		anns = tier.findall("ANNOTATION")
		for ann_idx, ann in enumerate(anns, start=1):		
			new_ann_idx = ann_idx + ann_idx_step
			for ann_child in ann:
				ann_id = ann_child.get("ANNOTATION_ID")
				opt_key[ann_id] = "a"+str(new_ann_idx)
				ann_child.set("ANNOTATION_ID", "a"+str(new_ann_idx))
		ann_idx_step = ann_idx_step+len(anns)
	for tier in tiers:
		anns = tier.findall("ANNOTATION")
		for ann in anns:
			for ann_child in ann:
				if ann_child.tag == "REF_ANNOTATION":
					ref = ann_child.get("ANNOTATION_REF")
					ann_child.set("ANNOTATION_REF", opt_key.get(ref))
	tree = ET.ElementTree(tree)
	tree.write(eaf_file, encoding="UTF-8", xml_declaration=True)

