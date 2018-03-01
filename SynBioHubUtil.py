'''
	This is a utility module containing classes with constant variables used for querying SynBioHub information
	
	author(s) : Nicholas Roehner 
				Tramy Nguyen
'''
class SBOLConstants():
	CIRCULAR = "http://identifiers.org/so/SO:0000988"
	DNA_REGION = "http://www.biopax.org/release/biopax-level3.owl#DnaRegion"
	EFFECTOR = "http://identifiers.org/chebi/CHEBI:35224"
	SMALL_MOLECULE = "<http://www.biopax.org/release/biopax-level3.owl#SmallMolecule>"

	SBOL_NS = "http://sbols.org/v2#"

class SBHConstants():
	SD2_SERVER = "http://hub-api.sd2e.org:80/sparql"
	BBN_SERVER = "https://synbiohub.bbn.com/"
	BBN_YEASTGATES_COLLECTION = "<https://synbiohub.bbn.com/user/tramyn/BBN_YEAST_GATES/BBN_YEAST_GATES_collection/1>"
	BBN_RULE30_COLLECTION = '<https://synbiohub.bbn.com/user/tramyn/transcriptic_rule_30_q0_1_09242017/transcriptic_rule_30_q0_1_09242017_collection/1>'
	RULE_30_COLLECTION = '<https://hub.sd2e.org/user/sd2e/rule_30/rule_30/1>'
