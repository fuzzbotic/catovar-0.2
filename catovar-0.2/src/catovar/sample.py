'''
Created on Nov 20, 2013

@author: erik
'''

import csv

class Sample(object):
    '''
    classdocs
    '''


    def __init__(self, info, info_fn):
        '''
        Constructor
        '''
        
        self.info = info
        self.info_fn = info_fn

        self.variants = []
        self.anno = {}
        self.anno_fn = []
            
        try:
            with open(self.info['filename'], 'rb') as multianno_file:
                
                multianno_dr = csv.DictReader(multianno_file)
                self.anno_fn = multianno_dr.fieldnames
                
                for variant in multianno_dr:
                    variant["Chr"] = variant["Chr"].lstrip("chr")
                    
                    if "Otherinfo" in variant.keys():
                        other_info = variant["Otherinfo"].split('\t')
                        vcf_format = dict(zip(other_info[-2].split(":"), \
                        other_info[-1].split(":")))
                        variant["VCFformat"] = vcf_format
                        vcf_info_list = other_info[-3].split(";")
                        vcf_info = {}
                        for e in vcf_info_list:
                            try:
                                e = e.split("=")
                                k = e[0]
                                v = e[1]
                                vcf_info[k] = v
                            except IndexError:
                                continue
                        variant["VCFinfo"] = vcf_info
                    
                    key = []
                    for fn in self.anno_fn[0:5]:
                        key.append(variant[fn])
                    key = tuple(key)
                    self.anno[key] = variant
                    self.variants.append(key)
        except IOError:
            print "Invalid multianno file: " + multianno_file
            raise
    
    def get_info(self):
        return self.info
    
    def get_info_fn(self):
        return self.info_fn
    
    def get_variants(self):
        return self.variants
    
    def get_anno(self, variant):
        return self.anno[variant]
    
    def get_anno_fn(self):
        return self.anno_fn