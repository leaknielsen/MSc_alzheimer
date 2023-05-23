# IMPORTING

from templates import *
from variables import *

gwf = Workflow()

for trait in all_traits:
    gwf.target_from_template("ldsc_format_{trait}".format(trait=trait),ldsc_format(trait))

for trait in all_traits:
    gwf.target_from_template("hm3_{trait}".format(trait=trait),hm3_merge(trait))

for trait in all_traits:
    gwf.target_from_template("h2_{trait}".format(trait=trait),h2(trait))
    
for trait in some_traits:
    gwf.target_from_template("rg_ad_{trait}".format(trait=trait),rg(trait))
   
for trait in all_traits:
    gwf.target_from_template("apoe_{trait}".format(trait=trait),apoe(trait))

for trait in all_traits:
    gwf.target_from_template("chr19_{trait}".format(trait=trait),chr19(trait))

for trait in all_traits:
    gwf.target_from_template("gsmr_format_{trait}".format(trait=trait),gsmr_format(trait))
    
for trait in all_traits:
    gwf.target_from_template("txt_{trait}".format(trait=trait),gsmr_text(trait))
    
for trait in some_traits:
    gwf.target_from_template("gsmr_{trait}".format(trait=trait),gsmr(trait))

