# IMPORTING:
from gwf import Workflow
from variables import *

def ldsc_format(trait):
    '''
    A dummy job to just flag that the same job for different inputs have been done
    '''
    inputs  = []
    
    outputs = ['{ldsc_formatted}/{trait}_ldsc_format'.format(trait = trait, ldsc_formatted=ldsc_formatted)]
    
    options = {'memory'  : '5g', 
               'walltime': '10:00:00', 
               'account' : 'alzheimersproject'}
    
    spec    = '''
    awk -v OFS='\t' 'BEGIN {{ print "SNP", "CHR", "BP", "A1", "A2", "FREQ", "P", "N", "Z" }} NR!=1 {{ print $1, $2, $3, $4, $5, $9, $7, $8, $6 }}' {formatted}/{trait}_formatted > {ldsc_formatted}/{trait}_ldsc_format
    '''.format(trait=trait, formatted=formatted, ldsc_formatted=ldsc_formatted)
    return inputs, outputs, options, spec

def hm3_merge(trait):
    '''
    A dummy job to just flag that the same job for different inputs have been done
    '''
    inputs  = []
    outputs = ['{ldsc_hm3}/{trait}_hm3'.format(trait = trait, ldsc_hm3=ldsc_hm3)]
    options = {'memory'  : '5g', 
               'walltime': '10:00:00', 
               'account' : 'alzheimersproject'}
    spec    = '''
    awk 'BEGIN{{FS=OFS="\t"}} FNR==NR{{arr[$1,$2,$3];next}} (($1,$4,$5) in arr)' w_hm3.snplist {ldsc_formatted}/{trait}_ldsc_form > {ldsc_hm3}/{trait}_hm3
    '''.format(trait=trait, ldsc_formatted=ldsc_formatted, ldsc_hm3=ldsc_hm3)
    return inputs, outputs, options, spec

def h2(trait):
    '''
    A dummy job to just flag that the same job for different inputs have been done
    '''
    inputs  = ['{ldsc_hm3}/{trait}_hm3'.format(trait = trait, ldsc_hm3=ldsc_hm3)]
    outputs = ['{ldsc_h2_results}/{trait}_h2'.format(trait = trait, ldsc_h2_results=ldsc_h2_results)]
    options = {'memory'  : '5g', 
               'walltime': '10:00:00', 
               'account' : 'alzheimersproject'}
    spec    = '''
    source /home/leko/.bashrc 
    source activate ldsc
    python ~/alzheimersproject/raw_GWAS/ldsc/ldsc.py --h2 {ldsc_hm3}/{trait}_hm3 --ref-ld-chr eur_w_ld_chr/ --w-ld-chr eur_w_ld_chr/ --out {ldsc_h2_results}/{trait}_h2
    '''.format(trait=trait, ldsc_hm3=ldsc_hm3, ldsc_h2_results=ldsc_h2_results)
    return inputs, outputs, options, spec

def rg(trait):
    '''
    A dummy job to just flag that the same job for different inputs have been done
    '''
    inputs  = ['{ldsc_hm3}/{trait}_hm3'.format(trait = trait, ldsc_hm3=ldsc_hm3)]
    outputs = ['{ldsc_rg_results}/ad_{trait}'.format(trait = trait, ldsc_rg_results=ldsc_rg_results)]
    options = {'memory'  : '5g', 
               'walltime': '10:00:00', 
               'account' : 'alzheimersproject'}
    spec    = '''
    source /home/leko/.bashrc 
    source activate ldsc
    python ~/alzheimersproject/raw_GWAS/ldsc/ldsc.py --rg {ldsc_hm3}/alzheimer_hm3,{ldsc_hm3}/{trait}_hm3 --ref-ld-chr eur_w_ld_chr/ --w-ld-chr eur_w_ld_chr/ --out {ldsc_rg_results}/ad_{trait}
    '''.format(trait=trait, ldsc_hm3=ldsc_hm3, ldsc_rg_results=ldsc_rg_results)
    return inputs, outputs, options, spec
    
def apoe(trait):
    '''
    A dummy job to just flag that the same job for different inputs have been done
    '''
    inputs  = []
    outputs = ['{gsmr_apoe}/{trait}_apoe'.format(trait = trait, gsmr_apoe=gsmr_apoe)]
    options = {'memory'  : '5g', 
               'walltime': '10:00:00', 
               'account' : 'alzheimersproject'}
    spec    = '''
    awk -v OFS='\t' 'NR>1 && ($3 < 45409039) || $3 > (45412650)' {formatted}/{trait}_formatted > {gsmr_apoe}/{trait}_apoe
    '''.format(trait=trait, formatted=formatted, gsmr_apoe=gsmr_apoe)
    return inputs, outputs, options, spec

def chr19(trait):
    '''
    A dummy job to just flag that the same job for different inputs have been done
    '''
    inputs  = []
    
    outputs = ['{gsmr_chr19}/{trait}_chr19'.format(trait = trait, gsmr_chr19=gsmr_chr19)]
    
    options = {'memory'  : '5g', 
               'walltime': '10:00:00', 
               'account' : 'alzheimersproject'}
    
    spec    = '''
    awk '$2 != 19' {formatted}/{trait}_formatted > {gsmr_chr19}/{trait}_chr19    
    '''.format(trait=trait, formatted=formatted, gsmr_chr19=gsmr_chr19)
    return inputs, outputs, options, spec

def gsmr_format(trait):
    '''
    A dummy job to just flag that the same job for different inputs have been done
    '''
    inputs  = ['{gsmr_apoe}/{trait}_apoe'.format(trait = trait, gsmr_apoe=gsmr_apoe), 
               '{gsmr_chr19}/{trait}_chr19'.format(trait = trait, gsmr_chr19=gsmr_chr19)]
    
    outputs = ['{gsmr_formatted}/{trait}_gsmr_format_apoe'.format(trait = trait, gsmr_formatted=gsmr_formatted),
              '{gsmr_formatted}/{trait}_gsmr_format_chr19'.format(trait = trait, gsmr_formatted=gsmr_formatted)]
    
    options = {'memory'  : '5g', 
               'walltime': '10:00:00', 
               'account' : 'alzheimersproject'}
    
    spec    = '''
    awk -v OFS='\t' 'BEGIN {{ print "SNP", "A1", "A2", "freq", "b", "se", "p", "N" }} NR!=1 {{ print $1, $4, $5, $9, $10, $11, $7, $8 }}' {gsmr_apoe}/{trait}_apoe > {gsmr_formatted}/{trait}_gsmr_format_apoe
    
    awk -v OFS='\t' 'BEGIN {{ print "SNP", "A1", "A2", "freq", "b", "se", "p", "N" }} NR!=1 {{ print $1, $4, $5, $9, $10, $11, $7, $8 }}' {gsmr_chr19}/{trait}_chr19 > {gsmr_formatted}/{trait}_gsmr_format_chr19
    '''.format(trait=trait, gsmr_apoe=gsmr_apoe, gsmr_chr19=gsmr_chr19, gsmr_formatted=gsmr_formatted)
    return inputs, outputs, options, spec

def gsmr_text(trait):
    '''
    A dummy job to just flag that the same job for different inputs have been done
    '''
    inputs  = ['{gsmr_formatted}/{trait}_gsmr_format_apoe'.format(trait = trait, gsmr_formatted=gsmr_formatted),
              '{gsmr_formatted}/{trait}_gsmr_format_chr19'.format(trait = trait, gsmr_formatted=gsmr_formatted)]
    
    outputs = ['{gsmr_txt}/{trait}_apoe.txt'.format(trait = trait, gsmr_txt=gsmr_txt),
               '{gsmr_txt}/{trait}_chr19.txt'.format(trait=trait, gsmr_txt=gsmr_txt)]
    
    options = {'memory'  : '5g', 
               'walltime': '10:00:00', 
               'account' : 'alzheimersproject'}
    
    spec    = '''
    echo {trait} {gsmr_formatted}/{trait}_gsmr_format_apoe > {gsmr_txt}/{trait}_apoe.txt
    echo {trait} {gsmr_formatted}/{trait}_gsmr_format_chr19 > {gsmr_txt}/{trait}_chr19.txt
    '''.format(trait=trait, gsmr_formatted=gsmr_formatted, gsmr_txt=gsmr_txt)
    return inputs, outputs, options, spec

def gsmr(trait):
    '''
    A dummy job to just flag that the same job for different inputs have been done
    '''
    inputs  = ['{gsmr_txt}/{trait}_apoe.txt'.format(trait = trait, gsmr_txt=gsmr_txt),
               '{gsmr_txt}/{trait}_chr19.txt'.format(trait=trait, gsmr_txt=gsmr_txt)]
    
    outputs = ['{gsmr_results}/{trait}_ad_apoe_default_gsmr'.format(trait = trait, gsmr_results=gsmr_results),
              '{gsmr_results}/{trait}_ad_apoe_stringent_gsmr'.format(trait = trait, gsmr_results=gsmr_results),
              '{gsmr_results}/{trait}_ad_chr19_default_gsmr'.format(trait = trait, gsmr_results=gsmr_results),
              '{gsmr_results}/{trait}_ad_chr19_stringent_gsmr'.format(trait = trait, gsmr_results=gsmr_results)]
    
    options = {'memory'  : '50g', 
               'walltime': '10:00:00', 
               'account' : 'alzheimersproject'}
    
    spec    = '''
    {gcta_package}/gcta-1.94.1 --bfile g1000_eur --gsmr-file {gsmr_txt}/{trait}_apoe.txt {gsmr_txt}/alzheimer_apoe.txt --gsmr-direction 2 --effect-plot --clump-r2 0.05 --heidi-thresh 0.01 --gsmr-snp-min 5 --out {gsmr_results}/{trait}_ad_apoe_default_gsmr
    
    {gcta_package}/gcta-1.94.1 --bfile g1000_eur --gsmr-file {gsmr_txt}/{trait}_apoe.txt {gsmr_txt}/alzheimer_apoe.txt --gsmr-direction 2 --effect-plot --clump-r2 0.01 --heidi-thresh 0.01 --gsmr-snp-min 5 --out {gsmr_results}/{trait}_ad_apoe_stringent_gsmr
    
    {gcta_package}/gcta-1.94.1 --bfile g1000_eur --gsmr-file {gsmr_txt}/{trait}_chr19.txt {gsmr_txt}/alzheimer_chr19.txt --gsmr-direction 2 --effect-plot --clump-r2 0.05 --heidi-thresh 0.01 --gsmr-snp-min 5 --out {gsmr_results}/{trait}_ad_chr19_default_gsmr
    
    {gcta_package}/gcta-1.94.1 --bfile g1000_eur --gsmr-file {gsmr_txt}/{trait}_chr19.txt {gsmr_txt}/alzheimer_chr19.txt --gsmr-direction 2 --effect-plot --clump-r2 0.01 --heidi-thresh 0.01 --gsmr-snp-min 5 --out {gsmr_results}/{trait}_ad_chr19_stringent_gsmr
    '''.format(trait=trait, gcta_package=gcta_package, gsmr_txt=gsmr_txt, gsmr_results=gsmr_results)
    return inputs, outputs, options, spec
